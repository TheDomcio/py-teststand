from __future__ import annotations

import gc

import pytest

from py_teststand import Engine


@pytest.mark.teststand_engine
@pytest.mark.integration
def test_engine_teardown_loop():

    for _ in range(5):
        engine = Engine()

        assert engine.version_string is not None

        engine.release()

        del engine

        gc.collect()


@pytest.mark.teststand_engine
@pytest.mark.integration
def test_child_object_weakref_to_engine():

    engine = Engine()

    ws = engine.new_workspace_file()

    root = ws.root_workspace_object

    assert root.engine is engine

    del engine

    gc.collect()

    assert root.engine is None

    assert ws.engine is None


@pytest.mark.teststand_engine
@pytest.mark.integration
def test_multiple_release_idempotency():

    engine = Engine()

    engine.release()

    engine.release()

    engine.release()


@pytest.mark.teststand_engine
@pytest.mark.integration
def test_no_interface_leak_across_wrapper_cycles():
    # Real-COM leak detection: repeatedly create and release wrappers and assert
    # the live COM interface count does not grow in proportion to the loop count.
    import pythoncom

    # Private pywin32 debug counter; not in the type stubs, so resolve at runtime.
    interface_count = getattr(pythoncom, "_GetInterfaceCount", None)
    if interface_count is None:
        return  # debug counter not present in this pywin32 build; nothing to check

    engine = Engine()
    try:
        # Warm up: the first cycle may cache type info, so it is not the baseline.
        warm = engine.new_sequence_file()
        warm.get_sequence_by_name("MainSequence")
        warm.release()
        gc.collect()
        pythoncom.PumpWaitingMessages()

        baseline = interface_count()
        cycles = 15
        for _ in range(cycles):
            sequence_file = engine.new_sequence_file()
            sequence = sequence_file.get_sequence_by_name("MainSequence")
            sequence.get_num_steps()
            del sequence
            sequence_file.release()
            del sequence_file
            gc.collect()

        pythoncom.PumpWaitingMessages()
        gc.collect()
        growth = interface_count() - baseline

        # A true per-cycle leak would grow ~cycles; allow a small constant slack.
        assert growth <= 10, f"COM interface count grew by {growth} over {cycles} cycles"
    finally:
        engine.shutdown()
        engine.release()
