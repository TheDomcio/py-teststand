"""Stress the headless UI-message path on a live engine; run as a subprocess.

Builds a MainSequence with 150 Statement steps, each posting one custom UI
message whose numeric payload is the step's index. Every tenth post is
synchronous, so the execution can only finish if the handler keeps
acknowledging under load. The assertions prove the mechanics end to end:
nothing lost, single-poster FIFO order preserved (GetUIMessage returns the
next message from the queue), payloads intact, and the execution completed.

Run by tests/integration/test_ui_messages.py in a subprocess because a process
that ran an execution can still abort during final COM teardown; the test
judges success by the OK marker printed before exit.
"""

from __future__ import annotations

from py_teststand import AdapterKeyName, Engine, StepGroup, UIMessageCode

MESSAGE_CODE = int(UIMessageCode.UserMessageBase) + 7
MESSAGE_COUNT = 150


def main() -> None:
    received: list[tuple[float, str, bool]] = []

    with Engine() as engine:
        sequence_file = engine.new_sequence_file()
        main_sequence = sequence_file.get_sequence_by_name("MainSequence")
        for index in range(MESSAGE_COUNT):
            synchronous = "True" if index % 10 == 0 else "False"
            step = engine.new_step(AdapterKeyName.NoneAdapterKeyName, "Statement")
            step.name = f"Post {index}"
            step.as_property_object()["TS.PostExpr"] = (
                f"RunState.Thread.PostUIMessageEx({MESSAGE_CODE}, {index}, "
                f'"payload-{index}", Nothing, {synchronous})'
            )
            main_sequence.insert_step(step, main_sequence.get_num_steps(), StepGroup.Main)

        engine.ui_handler.on(
            MESSAGE_CODE,
            lambda m: received.append((m.numeric_data, m.string_data, m.is_synchronous)),
        )
        with engine.new_execution(sequence_file, "MainSequence") as execution:
            ended = engine.ui_handler.wait_for_execution(execution, timeout_seconds=120)

    assert ended, "execution did not end (a synchronous post was likely never acknowledged)"
    assert len(received) == MESSAGE_COUNT, f"lost messages: got {len(received)}/{MESSAGE_COUNT}"
    numerics = [int(n) for n, _, _ in received]
    assert numerics == list(range(MESSAGE_COUNT)), "single-poster FIFO order violated"
    assert all(s == f"payload-{int(n)}" for n, s, _ in received), "string payload corrupted"
    assert all(sync == (int(n) % 10 == 0) for n, _, sync in received), "synchronous flag wrong"
    print(f"STRESS OK count={len(received)} ordered=True")


if __name__ == "__main__":
    main()
