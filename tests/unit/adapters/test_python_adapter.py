from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from py_teststand.adapters.python import (
    PythonAdapter,
    PythonInterpreterSessionScope,
    PythonModule,
    PythonOperationScope,
    PythonOperationType,
    PythonParameterCategory,
)


@pytest.fixture
def mock_engine():

    return MagicMock()


def test_python_adapter_properties(mock_engine):

    mock_com = MagicMock()

    mock_com.DebugJustMyCode = True

    mock_com.DisplayConsoleForInterpreterSessions = False

    mock_com.EnableDebugging = True

    mock_com.InterpreterSessionScope = 2

    mock_com.PythonExecutablePath = "C:/Python/python.exe"

    mock_com.PythonVersion = "3.8"

    mock_com.PythonVirtualEnvironmentPath = "C:/venv"

    mock_com.ReloadModifiedModulesDuringExecution = True

    adapter = PythonAdapter(mock_com, mock_engine)

    assert adapter.debug_just_my_code is True

    assert adapter.display_console_for_interpreter_sessions is False

    assert adapter.enable_debugging is True

    assert adapter.interpreter_session_scope == PythonInterpreterSessionScope.PerExecution

    assert adapter.python_executable_path == "C:/Python/python.exe"

    assert adapter.python_version == "3.8"

    assert adapter.python_virtual_environment_path == "C:/venv"

    assert adapter.reload_modified_modules_during_execution is True

    adapter.debug_just_my_code = False

    assert mock_com.DebugJustMyCode is False


def test_python_module_properties(mock_engine):

    mock_com = MagicMock()

    mock_com.ClassName = "MyClass"

    mock_com.OperationType = 1

    mock_com.OperationScope = 0

    mock_com.InterpreterSessionScope = 3

    module = PythonModule(mock_com, mock_engine)

    assert module.class_name == "MyClass"

    assert module.operation_type == PythonOperationType.CallMethod

    assert module.operation_scope == PythonOperationScope.Module

    assert module.interpreter_session_scope == PythonInterpreterSessionScope.Global

    module.class_name = "NewClass"

    assert mock_com.ClassName == "NewClass"


def test_python_parameters_collection(mock_engine):

    mock_com = MagicMock()

    mock_param_com = MagicMock()

    mock_param_com.ParameterName = "Param1"

    mock_param_com.Category = 1

    mock_com.Parameters.Count = 1

    mock_com.Parameters.Item.return_value = mock_param_com

    module = PythonModule(mock_com, mock_engine)

    params = module.parameters

    assert len(params) == 1

    assert params[0].parameter_name == "Param1"

    assert params[0].category == PythonParameterCategory.Number


def test_python_arguments(mock_engine):

    mock_com = MagicMock()

    mock_args_com = MagicMock()

    mock_arg_com = MagicMock()

    mock_arg_com.Value = 42

    mock_args_com.Count = 1

    mock_args_com.Item.return_value = mock_arg_com

    mock_com.NewArguments.return_value = mock_args_com

    module = PythonModule(mock_com, mock_engine)

    args = module.new_arguments()

    assert len(args) == 1

    assert args[0].value == 42

    args[0].value = 100

    assert mock_arg_com.Value == 100


def test_python_adapter_methods(mock_engine):

    mock_com = MagicMock()

    adapter = PythonAdapter(mock_com, mock_engine)

    mock_com.GetEnumTypeMapping.return_value = "PythonEnum"

    assert adapter.get_enum_type_mapping("TSEnum") == "PythonEnum"

    mock_com.GetExcludeFromObject.return_value = True

    mock_type_def = MagicMock()

    assert adapter.get_exclude_from_object(mock_type_def, "Prop") is True

    adapter.set_enum_type_mapping("TSEnum", "PythonEnum")

    mock_com.SetEnumTypeMapping.assert_called_with("TSEnum", "PythonEnum")
