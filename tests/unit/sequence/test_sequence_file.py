from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from py_teststand.core.exceptions import SequenceFileLoadError
from py_teststand.sequence.sequence_file import SequenceFile


def test_sequence_file_context_manager_normal(engine):

    mock_com = MagicMock()

    sf = SequenceFile(mock_com, engine)

    with sf as f:
        assert f is sf

    with sf:
        pass

    assert not hasattr(sf, "_com_obj") or sf._com_obj is None


def test_sequence_file_contract_get_model_absolute_path(engine):

    mock_com = MagicMock()

    mock_com.GetModelAbsolutePath.return_value = ("C:\\model.seq", True)

    sf = SequenceFile(mock_com, engine)

    path, exists = sf.get_model_absolute_path()

    assert path == "C:\\model.seq"

    assert exists is True

    mock_com.GetModelAbsolutePath.assert_called_once_with(False)


def test_sequence_file_contract_load_modules(engine):

    mock_com = MagicMock()

    mock_com.LoadModules.return_value = True

    sf = SequenceFile(mock_com, engine)

    mock_context = MagicMock()

    mock_context._com_obj = "real_com_obj"

    res = sf.load_modules(options=1, context=mock_context)

    assert res is True

    mock_com.LoadModules.assert_called_once_with(1, "real_com_obj")


def test_sequence_file_exception_translation(engine):

    mock_com = MagicMock()

    class ComError(Exception):
        hresult: int

    def mock_save(*_args, **_kwargs):

        error = ComError("COM Error")

        error.hresult = -19036

        raise error

    mock_com.Save.side_effect = mock_save

    sf = SequenceFile(mock_com, engine)

    with pytest.raises(SequenceFileLoadError) as exc_info:
        sf.save()

    assert exc_info.value.hresult == -19036
