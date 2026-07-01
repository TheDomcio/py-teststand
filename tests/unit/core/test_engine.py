from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from py_teststand import Engine, Execution
from py_teststand.core.engine import DecimalPointLocalizationOption, RTEOption


@pytest.fixture
def mock_engine_com():

    mock_com = MagicMock()

    mock_com.Is64Bit = True

    mock_com.TestStandDirectory = "C:/TestStand"

    mock_com.BinDirectory = "C:/TestStand/Bin"

    mock_com.ConfigDirectory = "C:/TestStand/Cfg"

    mock_com.SecondsAtStartIn1970UniversalCoordinatedTime = 1620000000.0

    mock_com.SecondsSince1970UniversalCoordinatedTime = 1620000010.0

    return mock_com


def test_engine_properties(mock_engine_com):

    engine = Engine(com_obj=mock_engine_com)

    assert engine.is_64bit is True

    assert engine.test_stand_directory == "C:/TestStand"

    assert engine.bin_directory == "C:/TestStand/Bin"

    assert engine.config_directory == "C:/TestStand/Cfg"

    assert engine.seconds_at_start_in_1970_universal_coordinated_time == 1620000000.0

    assert engine.seconds_since_1970_universal_coordinated_time == 1620000010.0


def test_engine_delocalize_expression(mock_engine_com):

    engine = Engine(com_obj=mock_engine_com)

    mock_engine_com.DelocalizeExpression.return_value = "1.5"

    result = engine.delocalize_expression("1,5", DecimalPointLocalizationOption.UseComma)

    assert result == "1.5"

    mock_engine_com.DelocalizeExpression.assert_called_with(
        "1,5",
        int(DecimalPointLocalizationOption.UseComma),
    )


def test_engine_new_execution(mock_engine_com):

    engine = Engine(com_obj=mock_engine_com)

    mock_seq_file = MagicMock()

    mock_seq_file._com_obj = MagicMock()

    mock_model = MagicMock()

    mock_model._com_obj = MagicMock()

    mock_exec_com = MagicMock()

    mock_engine_com.NewExecution.return_value = mock_exec_com

    execution = engine.new_execution(
        sequence_file=mock_seq_file,
        sequence_name="MainSequence",
        process_model=mock_model,
        break_at_first=True,
        exec_type_mask=1,
    )

    assert isinstance(execution, Execution)

    try:
        import pythoncom

        missing = pythoncom.Missing

    except ImportError:
        missing = None

    mock_engine_com.NewExecution.assert_called_with(
        mock_seq_file._com_obj,
        "MainSequence",
        mock_model._com_obj,
        True,
        1,
        missing,
        missing,
        missing,
    )


def test_engine_display_runtime_error_dialog(mock_engine_com):

    engine = Engine(com_obj=mock_engine_com)

    mock_engine_com.DisplayRunTimeErrorDialog.return_value = (True, False, 3)

    result = engine.display_runtime_error_dialog("Title", "Error", False, True)

    assert result == (True, False, RTEOption.Abort)

    mock_engine_com.DisplayRunTimeErrorDialog.assert_called_with("Title", "Error", False, True)


def test_engine_init_frozen_no_rmtree():

    from unittest.mock import patch

    import pythoncom

    mock_error = pythoncom.com_error(0x80020009, "Exception occurred", None, None)

    with patch("sys.frozen", True, create=True), patch(
        "win32com.client.gencache.EnsureDispatch", side_effect=mock_error
    ), patch("win32com.client.DispatchEx") as mock_dispatch_ex, patch(
        "shutil.rmtree"
    ) as mock_rmtree:
        with patch("pythoncom.CoInitializeEx"):
            try:
                Engine()
            except Exception:
                pass

        mock_rmtree.assert_not_called()
        mock_dispatch_ex.assert_called_once_with("TestStand.Engine.1")


def test_engine_init_unfrozen_rmtree_on_failure():

    from unittest.mock import MagicMock, patch

    import pythoncom
    import win32com

    mock_error = pythoncom.com_error(0x80020009, "Exception occurred", None, None)

    patch_ensure = patch(
        "win32com.client.gencache.EnsureDispatch",
        side_effect=[mock_error, MagicMock()],
    )
    with patch.object(win32com, "__gen_path__", "C:/dummy_gen_path", create=True), patch(
        "pathlib.Path.exists", return_value=True
    ), patch_ensure as mock_ensure, patch("shutil.rmtree") as mock_rmtree:
        with patch("pythoncom.CoInitializeEx"):
            Engine()

        mock_rmtree.assert_called_once_with("C:/dummy_gen_path")
        assert mock_ensure.call_count == 2


def test_engine_init_rmtree_permission_error_fallback():

    from unittest.mock import patch

    import pythoncom
    import win32com

    mock_error = pythoncom.com_error(0x80020009, "Exception occurred", None, None)

    with patch.object(win32com, "__gen_path__", "C:/dummy_gen_path", create=True), patch(
        "pathlib.Path.exists", return_value=True
    ), patch("win32com.client.gencache.EnsureDispatch", side_effect=mock_error), patch(
        "shutil.rmtree", side_effect=PermissionError("Permission denied")
    ) as mock_rmtree, patch("win32com.client.DispatchEx") as mock_dispatch_ex:
        with patch("pythoncom.CoInitializeEx"):
            try:
                Engine()
            except Exception:
                pass

        mock_rmtree.assert_called_once_with("C:/dummy_gen_path")
        mock_dispatch_ex.assert_called_once_with("TestStand.Engine.1")
