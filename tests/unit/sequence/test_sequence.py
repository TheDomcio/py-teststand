from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from py_teststand.sequence.sequence import (
    LoadModuleOption,
    Sequence,
)
from py_teststand.sequence.step_group import StepGroup


def test_sequence_contract_get_break_on_end_settings(engine):

    mock_com = MagicMock()

    mock_com.GetBreakOnEndSettings.return_value = (True, False, 5, "RunState.LoopIndex == 5")

    seq = Sequence(mock_com, engine)

    is_set, enabled, pass_count, condition = seq.get_break_on_end_settings(StepGroup.Main)

    assert is_set is True

    assert enabled is False

    assert pass_count == 5

    assert condition == "RunState.LoopIndex == 5"

    mock_com.GetBreakOnEndSettings.assert_called_once_with(
        int(StepGroup.Main), None, None, None, None, None
    )


def test_sequence_contract_load_modules(engine):

    mock_com = MagicMock()

    mock_com.LoadModules.return_value = True

    seq = Sequence(mock_com, engine)

    mock_context = MagicMock()

    mock_context._com_obj = "real_context_obj"

    res = seq.load_modules(load_options=LoadModuleOption.NoneValue, context=mock_context)

    assert res is True

    mock_com.LoadModules.assert_called_once_with(
        int(LoadModuleOption.NoneValue), "real_context_obj"
    )


def test_sequence_exception_translation(engine):

    mock_com = MagicMock()

    class ComError(Exception):
        hresult: int

    def mock_eval(*_args, **_kwargs):

        error = ComError("COM Error")

        error.hresult = -17306

        raise error

    mock_com.GetEffectiveType.side_effect = mock_eval

    seq = Sequence(mock_com, engine)

    from py_teststand.core.exceptions import InvalidPropertyError

    with pytest.raises(InvalidPropertyError) as exc_info:
        seq.get_effective_type()

    assert exc_info.value.hresult == -17306
