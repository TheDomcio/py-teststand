"""Receive UI messages from a running sequence with no GUI attached.

A sequence tells its host application what is happening by posting UI messages:
stage descriptions, progress values, step results. A GUI receives them through
the TestStand UI controls; a headless host (server, CI runner) polls the
engine's message queue instead. Engine.ui_handler wraps that polling: register
a callback per event code, then let wait_for_execution pump the queue on the
engine's own thread while the sequence runs.

The sequence posts two custom messages (codes above UserMessageBase) from
Statement steps in MainSequence:

- Per execution: RunState.Engine.PostUIMessage(RunState.Execution, ...) tags the
  message with the posting execution. Posted synchronously, so the sequence
  blocks until the handler acknowledges it (the handler acknowledges every
  message after its callbacks run).
- Per thread: RunState.Thread.PostUIMessageEx(...) tags the message with the
  posting thread. Posted asynchronously, so the sequence moves on immediately.

Each message carries a numeric and a string payload; the callbacks read both
plus the execution id that identifies who posted.
"""

from __future__ import annotations

from py_teststand import AdapterKeyName, Engine, StepGroup, UIMessageCode

STAGE_MESSAGE = int(UIMessageCode.UserMessageBase) + 1
PROGRESS_MESSAGE = int(UIMessageCode.UserMessageBase) + 2

POST_FOR_EXECUTION = (
    f"RunState.Engine.PostUIMessage(RunState.Execution, RunState.Thread, {STAGE_MESSAGE}, "
    f'1, "stage: configuring instruments", Nothing, True)'
)
POST_FOR_THREAD = (
    f'RunState.Thread.PostUIMessageEx({PROGRESS_MESSAGE}, 50, "progress: halfway", Nothing, False)'
)


def _add_statement_step(engine, sequence, name, expression):
    """Append a Statement step whose expression runs when the step executes."""
    step = engine.new_step(AdapterKeyName.NoneAdapterKeyName, "Statement")
    step.name = name
    step.as_property_object()["TS.PostExpr"] = expression
    sequence.insert_step(step, sequence.get_num_steps(), StepGroup.Main)


def main() -> None:
    received = []

    def on_stage(message) -> None:
        execution = message.execution
        received.append(
            f"stage message    (execution {execution.id if execution else '?'}): "
            f"numeric={message.numeric_data} string={message.string_data!r} "
            f"synchronous={message.is_synchronous}"
        )

    def on_progress(message) -> None:
        received.append(
            f"progress message (thread-posted): "
            f"numeric={message.numeric_data} string={message.string_data!r} "
            f"synchronous={message.is_synchronous}"
        )

    with Engine() as engine:
        sequence_file = engine.new_sequence_file()
        main_sequence = sequence_file.get_sequence_by_name("MainSequence")
        _add_statement_step(engine, main_sequence, "Report Stage", POST_FOR_EXECUTION)
        _add_statement_step(engine, main_sequence, "Report Progress", POST_FOR_THREAD)

        engine.ui_handler.on(STAGE_MESSAGE, on_stage)
        engine.ui_handler.on(PROGRESS_MESSAGE, on_progress)

        with engine.new_execution(sequence_file, "MainSequence") as execution:
            ended = engine.ui_handler.wait_for_execution(execution, timeout_seconds=60)

    print("Messages received headless:")
    for line in received:
        print(f"  {line}")
    assert ended, "execution did not end in time"
    assert len(received) == 2, f"expected 2 UI messages, got {len(received)}: {received}"
    print("\nBoth custom UI messages arrived; the synchronous one was acknowledged.")


if __name__ == "__main__":
    main()
