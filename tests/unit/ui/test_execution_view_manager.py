from unittest.mock import MagicMock

import pytest

from py_teststand.ui.execution_view_manager import ExecutionViewManager, StepGroupMode


class MockCOM(MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.Execution = MagicMock()

        self.Thread = MagicMock()

        self.SequenceContext = MagicMock()

        self.RunState = 1

        self.TerminationState = 1

        self.StepGroupMode = 1

        self.SelectedSteps = MagicMock()

        self.Connections = MagicMock()


@pytest.fixture
def mock_engine():

    return MagicMock()


@pytest.fixture
def execution_view_manager(mock_engine):

    return ExecutionViewManager(MockCOM(), mock_engine)


def test_execution_access(execution_view_manager):

    assert execution_view_manager.execution is not None

    execution_view_manager.execution = None

    assert execution_view_manager._com_obj.Execution is None


def test_step_group_mode(execution_view_manager):

    assert execution_view_manager.step_group_mode == StepGroupMode.OneGroup

    execution_view_manager.step_group_mode = StepGroupMode.AllGroups

    assert execution_view_manager._com_obj.StepGroupMode == 2


def test_control_methods(execution_view_manager):

    execution_view_manager.abort_execution()

    execution_view_manager.break_execution()

    execution_view_manager.resume_execution()

    execution_view_manager.terminate_execution()

    execution_view_manager.restart_execution()

    execution_view_manager.refresh()
