from unittest.mock import MagicMock

import pytest

from py_teststand.adapters.activex import ActiveXAdapter


@pytest.fixture
def mock_engine():

    return MagicMock()


@pytest.fixture
def activex_adapter(mock_engine):

    return ActiveXAdapter(MagicMock(), mock_engine)


def test_update_automation_ids(activex_adapter):

    mock_seq_file = MagicMock()

    mock_seq_file._com_obj = "mock_seq_file_com"

    activex_adapter._com_obj.UpdateAutomationIDs.return_value = (10, 2, "Some error")

    result = activex_adapter.update_automation_ids(mock_seq_file)

    assert result.num_steps_modified == 10

    assert result.num_step_updates_failed == 2

    assert result.error_description == "Some error"

    activex_adapter._com_obj.UpdateAutomationIDs.assert_called_once_with("mock_seq_file_com")
