from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from py_teststand.execution.execution import Execution
from py_teststand.sequence.sequence_file import SequenceFile
from py_teststand.ui.sequence_file_view_manager import SequenceFileViewManager


@pytest.fixture
def mock_engine():
    return MagicMock()


def test_sequence_file_getter_wraps_com_object(mock_engine):
    com = MagicMock()
    inner = MagicMock()
    com.SequenceFile = inner

    manager = SequenceFileViewManager(com, mock_engine)
    sequence_file = manager.sequence_file

    assert isinstance(sequence_file, SequenceFile)
    assert sequence_file._com_obj is inner


def test_sequence_file_getter_returns_none_when_unset(mock_engine):
    com = MagicMock()
    com.SequenceFile = None

    manager = SequenceFileViewManager(com, mock_engine)

    assert manager.sequence_file is None


def test_sequence_file_setter_writes_raw_com_object(mock_engine):
    com = MagicMock()
    manager = SequenceFileViewManager(com, mock_engine)

    manager.sequence_file = None
    assert com.SequenceFile is None


def test_step_group_getter_is_int_and_setter_writes(mock_engine):
    com = MagicMock()
    com.StepGroup = 2
    manager = SequenceFileViewManager(com, mock_engine)

    assert manager.step_group == 2
    assert isinstance(manager.step_group, int)

    manager.step_group = 1
    assert com.StepGroup == 1


def test_loop_on_selected_steps_calls_com_and_wraps_execution(mock_engine):
    com = MagicMock()
    inner = MagicMock()
    com.LoopOnSelectedSteps.return_value = inner
    manager = SequenceFileViewManager(com, mock_engine)

    execution = manager.loop_on_selected_steps()

    com.LoopOnSelectedSteps.assert_called_once_with(None)
    assert isinstance(execution, Execution)
    assert execution._com_obj is inner


def test_refresh_calls_com_member(mock_engine):
    com = MagicMock()
    manager = SequenceFileViewManager(com, mock_engine)

    manager.refresh()

    com.Refresh.assert_called_once_with()
