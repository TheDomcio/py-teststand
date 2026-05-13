from __future__ import annotations

from unittest.mock import MagicMock, PropertyMock

from py_teststand import SequenceFile


def test_sequence_file_properties():

    mock_sequence_file_com = MagicMock()

    type(mock_sequence_file_com).Path = PropertyMock(return_value="mock.sequence")

    type(mock_sequence_file_com).NumSequences = PropertyMock(return_value=2)

    sequence_file = SequenceFile(mock_sequence_file_com, None)

    assert sequence_file.path == "mock.sequence"

    assert sequence_file.num_sequences == 2


def test_sequence_file_save():

    mock_sequence_file_com = MagicMock()

    sequence_file = SequenceFile(mock_sequence_file_com, None)

    sequence_file.save()

    assert mock_sequence_file_com.Save.called or mock_sequence_file_com.WriteFile.called


def test_sequence_file_save_with_path():

    mock_sequence_file_com = MagicMock()

    sequence_file = SequenceFile(mock_sequence_file_com, None)

    sequence_file.save("other.sequence")

    mock_sequence_file_com.Save.assert_called_once_with("other.sequence")


def test_sequence_file_save_with_new_path():

    mock_sequence_file_com = MagicMock()

    sequence_file = SequenceFile(mock_sequence_file_com, None)

    sequence_file.save("new_mock.sequence")

    mock_sequence_file_com.Save.assert_called_once_with("new_mock.sequence")


def test_sequence_file_release():

    mock_sequence_file_com = MagicMock()

    sequence_file = SequenceFile(mock_sequence_file_com, None)

    sequence_file.release()

    assert sequence_file._com_obj is None
