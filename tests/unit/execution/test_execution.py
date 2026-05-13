from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from py_teststand.core.exceptions import SequenceAbortedError
from py_teststand.execution.execution import (
    Execution,
    ExecutionRunState,
    ExecutionTerminationState,
)


class DummyComError(Exception):
    def __init__(self, hresult, desc):
        self.hresult = hresult
        super().__init__(desc)


def test_execution_context_manager_normal(engine):
    mock_com = MagicMock()
    exec_obj = Execution(mock_com, engine)
    with exec_obj as e:
        assert e is exec_obj
    mock_com.Abort.assert_not_called()
    assert not hasattr(exec_obj, "_com_obj") or exec_obj._com_obj is None


def test_execution_context_manager_exception(engine):
    mock_com = MagicMock()
    exec_obj = Execution(mock_com, engine)

    class DummyError(Exception):
        pass

    with pytest.raises(DummyError):
        with exec_obj:
            raise DummyError("Fail")
    mock_com.Abort.assert_called_once()
    assert not hasattr(exec_obj, "_com_obj") or exec_obj._com_obj is None


def test_execution_contract_wait_for_end_ex(engine):
    import pythoncom

    mock_com = MagicMock()
    mock_com.WaitForEndEx.return_value = (True,)
    exec_obj = Execution(mock_com, engine)
    res = exec_obj.wait_for_end_ex(timeout_ms=5000, process_windows_msgs=False)
    assert res is True
    mock_com.WaitForEndEx.assert_called_once_with(5000, False, pythoncom.Missing, pythoncom.Missing)


def test_execution_enum_casting_get_states(engine):
    mock_com = MagicMock()
    mock_com.GetStates.return_value = (3, 1)
    exec_obj = Execution(mock_com, engine)
    run_state, term_state = exec_obj.get_states()
    assert isinstance(run_state, ExecutionRunState)
    assert run_state == ExecutionRunState.Stopped
    assert isinstance(term_state, ExecutionTerminationState)
    assert term_state == ExecutionTerminationState.Normal
    mock_com.GetStates.assert_called_once_with(0, 0)


def test_execution_exception_translation(engine):
    mock_com = MagicMock()

    class ComError(Exception):
        hresult: int

    def mock_abort(*_args, **_kwargs):
        error = ComError("COM Error")
        error.hresult = -17602
        raise error

    mock_com.Abort.side_effect = mock_abort
    exec_obj = Execution(mock_com, engine)
    with pytest.raises(SequenceAbortedError) as exc_info:
        exec_obj.abort()
    assert exc_info.value.hresult == -17602
