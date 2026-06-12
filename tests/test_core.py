from __future__ import annotations

from pathlib import Path

import pytest

from py_teststand import Engine, Error, SequenceFile
from py_teststand.core.engine import RTEOption


@pytest.mark.teststand_engine
def test_engine_initialization(engine) -> None:

    assert engine is not None

    assert engine.application_version_string is None or isinstance(
        engine.application_version_string,
        str,
    )

    assert isinstance(engine.is_64bit, bool)


@pytest.mark.teststand_engine
def test_engine_context_manager() -> None:

    with Engine() as eng:
        assert eng is not None

        opts = eng.station_options

        opts.rte_option = RTEOption.Abort

        assert opts.rte_option == RTEOption.Abort


@pytest.mark.teststand_engine
def test_load_sequence_file(engine) -> None:

    import tempfile

    with tempfile.TemporaryDirectory() as tmp_dir:
        path = str(Path(tmp_dir) / "test.seq")

        engine.new_sequence_file().save(path)

        seq_file = engine.get_sequence_file(path)

        assert isinstance(seq_file, SequenceFile)

        assert seq_file.path == path


@pytest.mark.teststand_engine
def test_start_execution() -> None:
    # Runs in a subprocess: a process that ran an execution can abort during
    # final COM teardown (after the work completed), so isolation keeps that
    # from taking down the test session. Success is judged by the marker.
    import subprocess
    import sys
    import textwrap

    script = textwrap.dedent(
        """
        import tempfile
        from pathlib import Path
        from py_teststand import Engine, Execution
        from py_teststand.execution.execution import ExecutionRunState

        with tempfile.TemporaryDirectory() as tmp_dir:
            path = str(Path(tmp_dir) / "test.seq")
            with Engine() as engine:
                engine.new_sequence_file().save(path)
                seq_file = engine.get_sequence_file(path)
                execution = engine.new_execution(
                    sequence_file=seq_file,
                    sequence_name="MainSequence",
                    process_model=None,
                    break_at_first=False,
                    exec_type_mask=0,
                )
                assert isinstance(execution, Execution)
                state = execution.get_states()[0]
                assert state in (ExecutionRunState.Running, ExecutionRunState.Stopped)
                print("EXECUTION OK state=", state)
        """
    )
    completed = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert "EXECUTION OK" in completed.stdout, completed.stdout + completed.stderr


@pytest.mark.teststand_engine
def test_exception_translation() -> None:

    from unittest.mock import MagicMock

    import pythoncom

    mock_com = MagicMock()

    mock_com.GetSequenceFile.side_effect = pythoncom.com_error(
        -2147211512,
        "File not found",
        (0, "TestStand", "File not found", None, 0, -2147211512),
        None,
    )

    err_engine = Engine(com_obj=mock_com)

    with pytest.raises(Error) as excinfo:
        err_engine.get_sequence_file("non_existent.seq")

    assert "0x80042708" in str(excinfo.value) or "File not found" in str(excinfo.value)
