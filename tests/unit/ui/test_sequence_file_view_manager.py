from unittest.mock import MagicMock

import pytest

from py_teststand.ui.sequence_file_view_manager import SequenceFileViewManager


class MockCOM(MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.SequenceFile = MagicMock()

        self.Sequence = MagicMock()

        self.StepGroup = 0

        self.StepGroupMode = 1

        self.SelectedSteps = MagicMock()

        self.Connections = MagicMock()

        self.UndoStack = MagicMock()

    def LoopOnSelectedSteps(self, _interactive_args=None):  # noqa: N802

        return MagicMock()


@pytest.fixture
def mock_engine():

    return MagicMock()


@pytest.fixture
def sequence_file_view_manager(mock_engine):

    return SequenceFileViewManager(MockCOM(), mock_engine)


def test_sequence_file_access(sequence_file_view_manager):

    assert sequence_file_view_manager.sequence_file is not None

    sequence_file_view_manager.sequence_file = None

    assert sequence_file_view_manager._com_obj.SequenceFile is None


def test_step_group(sequence_file_view_manager):

    assert sequence_file_view_manager.step_group == 0

    sequence_file_view_manager.step_group = 1

    assert sequence_file_view_manager._com_obj.StepGroup == 1


def test_control_methods(sequence_file_view_manager):

    sequence_file_view_manager.loop_on_selected_steps()

    sequence_file_view_manager.refresh()
