from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from py_teststand.execution.execution import Execution
from py_teststand.sequence.step_group import StepGroupMode
from py_teststand.ui.execution_view_manager import ExecutionViewManager


@pytest.fixture
def mock_engine():
    return MagicMock()


def test_execution_getter_wraps_com_execution(mock_engine):
    com = MagicMock()
    inner = MagicMock()
    com.Execution = inner

    manager = ExecutionViewManager(com, mock_engine)
    execution = manager.execution

    assert isinstance(execution, Execution)
    assert execution._com_obj is inner


def test_execution_getter_returns_none_when_unset(mock_engine):
    com = MagicMock()
    com.Execution = None

    manager = ExecutionViewManager(com, mock_engine)

    assert manager.execution is None


def test_execution_setter_writes_raw_com_object(mock_engine):
    com = MagicMock()
    inner = MagicMock()
    manager = ExecutionViewManager(com, mock_engine)

    manager.execution = Execution(inner, mock_engine)
    assert com.Execution is inner

    manager.execution = None
    assert com.Execution is None


def test_step_group_mode_casts_enum_and_setter_writes_int(mock_engine):
    com = MagicMock()
    com.StepGroupMode = int(StepGroupMode.OneGroup)
    manager = ExecutionViewManager(com, mock_engine)

    assert manager.step_group_mode == StepGroupMode.OneGroup

    manager.step_group_mode = StepGroupMode.AllGroups
    assert com.StepGroupMode == int(StepGroupMode.AllGroups)


@pytest.mark.parametrize(
    ("method_name", "com_member"),
    [
        ("abort_execution", "AbortExecution"),
        ("break_execution", "BreakExecution"),
        ("resume_execution", "ResumeExecution"),
        ("terminate_execution", "TerminateExecution"),
        ("restart_execution", "RestartExecution"),
        ("refresh", "Refresh"),
    ],
)
def test_control_method_calls_exact_com_member(mock_engine, method_name, com_member):
    # Each control method must invoke its specific COM member with no arguments;
    # a renamed or wrong member makes this fail instead of silently passing.
    com = MagicMock()
    manager = ExecutionViewManager(com, mock_engine)

    getattr(manager, method_name)()

    getattr(com, com_member).assert_called_once_with()
