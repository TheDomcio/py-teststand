from __future__ import annotations

from unittest.mock import MagicMock, PropertyMock

from py_teststand.sequence.sequence import Sequence
from py_teststand.sequence.step import Step
from py_teststand.sequence.step_group import StepGroup


def test_sequence_name():

    mock_com_obj = MagicMock()

    type(mock_com_obj).Name = PropertyMock(return_value="TestSequence")

    sequence = Sequence(mock_com_obj, None)

    assert sequence.name == "TestSequence"


def test_sequence_disable_results():

    mock_com_obj = MagicMock()

    type(mock_com_obj).DisableResults = PropertyMock(return_value=True)

    sequence = Sequence(mock_com_obj, None)

    assert sequence.disable_results is True


def test_sequence_get_step():

    mock_com_obj = MagicMock()

    mock_step = MagicMock()

    mock_com_obj.GetStep.return_value = mock_step

    sequence = Sequence(mock_com_obj, None)

    result = sequence.get_step(0)

    assert isinstance(result, Step)

    mock_com_obj.GetStep.assert_called_with(0, StepGroup.Main)


def test_sequence_get_step_with_group():

    mock_com_obj = MagicMock()

    mock_step = MagicMock()

    mock_com_obj.GetStep.return_value = mock_step

    sequence = Sequence(mock_com_obj, None)

    result = sequence.get_step(1, StepGroup.Cleanup)

    assert isinstance(result, Step)

    mock_com_obj.GetStep.assert_called_with(1, StepGroup.Cleanup)


def test_sequence_get_step_by_name():

    mock_com_obj = MagicMock()

    mock_step = MagicMock()

    mock_com_obj.GetStepByName.return_value = mock_step

    sequence = Sequence(mock_com_obj, None)

    result = sequence.get_step_by_name("MyStep")

    assert isinstance(result, Step)

    mock_com_obj.GetStepByName.assert_called_with("MyStep", StepGroup.Main)


def test_sequence_remove_step():

    mock_com_obj = MagicMock()

    sequence = Sequence(mock_com_obj, None)

    sequence.remove_step(0, StepGroup.Main)

    mock_com_obj.RemoveStep.assert_called_with(0, StepGroup.Main)


def test_sequence_insert_step():

    mock_com_obj = MagicMock()

    mock_step = MagicMock()

    mock_step._com_obj = MagicMock()

    sequence = Sequence(mock_com_obj, None)

    sequence.insert_step(mock_step, 0, StepGroup.Main)

    mock_com_obj.InsertStep.assert_called_with(mock_step._com_obj, 0, StepGroup.Main)


def test_sequence_new_step_logic():

    mock_com_obj = MagicMock()

    mock_engine = MagicMock()

    mock_engine_api = MagicMock()

    mock_engine._engine = mock_engine_api

    mock_adapter = MagicMock()

    mock_adapter.key_name = "DotNet Adapter"

    mock_engine.get_adapter_by_key_name.return_value = mock_adapter

    mock_new_step_com = MagicMock()

    mock_engine_api.NewStep.return_value = mock_new_step_com

    sequence = Sequence(mock_com_obj, mock_engine)

    result = sequence.new_step(
        adapter_name="DotNet Adapter",
        step_type_name="Action",
        name="CustomStepName",
        index=5,
        group=StepGroup.Setup,
    )

    assert isinstance(result, Step)

    mock_engine.get_adapter_by_key_name.assert_called_with("DotNet Adapter")

    mock_engine_api.NewStep.assert_called_with("DotNet Adapter", "Action")

    assert mock_new_step_com.Name == "CustomStepName"

    mock_com_obj.InsertStep.assert_called_with(mock_new_step_com, 5, StepGroup.Setup)


def test_sequence_release():

    mock_com_obj = MagicMock()

    sequence = Sequence(mock_com_obj, None)

    sequence.release()

    assert sequence._com_obj is None
