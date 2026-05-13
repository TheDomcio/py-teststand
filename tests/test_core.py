from __future__ import annotations

from pathlib import Path

import pytest

from py_teststand import Engine, Execution, SequenceFile, TestStandError
from py_teststand.core.engine import RTEOption
from py_teststand.execution.execution import ExecutionRunState


@pytest.mark.live_com
def test_engine_initialization(engine) -> None:

    assert engine is not None

    assert engine.application_version_string is None or isinstance(
        engine.application_version_string, str
    )

    assert isinstance(engine.is_64bit, bool)


@pytest.mark.live_com
def test_engine_context_manager() -> None:

    with Engine() as eng:
        assert eng is not None

        opts = eng.station_options

        opts.rte_option = RTEOption.Abort

        assert opts.rte_option == RTEOption.Abort


@pytest.mark.live_com
def test_load_sequence_file(engine) -> None:

    import tempfile

    with tempfile.TemporaryDirectory() as tmp_dir:
        path = str(Path(tmp_dir) / "test.seq")

        engine.new_sequence_file().save(path)

        seq_file = engine.get_sequence_file(path)

        assert isinstance(seq_file, SequenceFile)

        assert seq_file.path == path


@pytest.mark.live_com
def test_start_execution(engine) -> None:

    import tempfile

    with tempfile.TemporaryDirectory() as tmp_dir:
        path = str(Path(tmp_dir) / "test.seq")

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

        assert execution.get_states()[0] in (
            ExecutionRunState.Running,
            ExecutionRunState.Stopped,
        )


@pytest.mark.live_com
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

    with pytest.raises(TestStandError) as excinfo:
        err_engine.get_sequence_file("non_existent.seq")

    assert "0x80042708" in str(excinfo.value) or "File not found" in str(excinfo.value)
