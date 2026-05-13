from __future__ import annotations

import typing
from enum import IntEnum

from py_teststand.adapters.adapter import (
    Adapter,
    AdapterCodeTemplatePolicy,
    CommonCModule,
    CommonCParameter,
    CommonCParameterPassOption,
    CommonCParameterType,
)
from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.property.property_object import PropertyObject


class CVIModuleType(IntEnum):
    Obj = 0
    Source = 1
    DLL = 2
    Lib = 3


class CVIParameterCategory(IntEnum):
    Numeric = 0
    NumericArray = 1
    String = 2
    Void = 3
    Object = 4
    CStruct = 5
    StringArray = 6
    ObjectArray = 7
    CStructArray = 8
    Pointer = 9
    Enum = 10
    EnumArray = 11
    TestData = 100
    TestError = 101


class GetModuleFromProjectOption(IntEnum):
    def __str__(self) -> str:
        return str(self.value)

    NoneValue = 0
    NoPrompts = 1


class CVIAdapter(Adapter):
    @property
    @ts_interface
    def code_template_policy(self) -> AdapterCodeTemplatePolicy:
        return AdapterCodeTemplatePolicy(self._com_obj.CodeTemplatePolicy)

    @code_template_policy.setter
    @ts_interface
    def code_template_policy(self, value: AdapterCodeTemplatePolicy | int) -> None:
        self._com_obj.CodeTemplatePolicy = int(value)

    @property
    @ts_interface
    def execute_steps_in_external_instance(self) -> bool:
        return bool(self._com_obj.ExecuteStepsInExternalInstance)

    @execute_steps_in_external_instance.setter
    @ts_interface
    def execute_steps_in_external_instance(self, value: bool) -> None:
        self._com_obj.ExecuteStepsInExternalInstance = value

    @property
    @ts_interface
    def execution_server_project_path_name(self) -> str:
        return str(self._com_obj.ExecutionServerProjectPathName)

    @execution_server_project_path_name.setter
    @ts_interface
    def execution_server_project_path_name(self, value: str) -> None:
        self._com_obj.ExecutionServerProjectPathName = value

    @ts_interface
    def as_adapter(self) -> Adapter:
        return Adapter(self._com_obj.AsAdapter(), self._engine_ref)

    @ts_interface
    def as_common_c_adapter(self) -> typing.Any:
        from py_teststand.adapters.dll import CommonCAdapter

        return CommonCAdapter(self._com_obj.AsCommonCAdapter(), self._engine_ref)

    @ts_interface
    def new_module(self) -> CVIModule:
        return CVIModule(self._com_obj.NewModule(), self._engine_ref)


class CVIModule(CommonCModule):
    @property
    @ts_interface
    def allow_project_file_when_selecting_module(self) -> bool:
        return bool(self._com_obj.AllowProjectFileWhenSelectingModule)

    @property
    @ts_interface
    def always_run_in_process(self) -> bool:
        return bool(self._com_obj.AlwaysRunInProcess)

    @always_run_in_process.setter
    @ts_interface
    def always_run_in_process(self, value: bool) -> None:
        self._com_obj.AlwaysRunInProcess = value

    @property
    @ts_interface
    def as_common_c_module(self) -> CommonCModule:
        return CommonCModule(self._com_obj.AsCommonCModule, self._engine_ref)

    @ts_interface
    def execute(
        self, sequence_context_param: typing.Any, arguments_param: typing.Any
    ) -> typing.Any:
        ctx_obj = (
            sequence_context_param._com_obj
            if hasattr(sequence_context_param, "_com_obj")
            else sequence_context_param
        )
        args_obj = (
            arguments_param._com_obj if hasattr(arguments_param, "_com_obj") else arguments_param
        )
        self._com_obj.Execute(ctx_obj, args_obj)

    @ts_interface
    def get_module_path_from_project(
        self, project_path_param: str, options: GetModuleFromProjectOption | int
    ) -> tuple[bool, str]:
        return self._com_obj.GetModulePathFromProject(project_path_param, int(options))

    @ts_interface
    def get_project_file_path_from_dll(self, dll_path: str) -> typing.Any:
        return self._com_obj.GetProjectFilePathFromDll(dll_path)

    @ts_interface
    def get_source_file_path_from_dll(self, dll_path: str, function: str) -> typing.Any:
        return self._com_obj.GetSourceFilePathFromDll(dll_path, function)

    @property
    @ts_interface
    def module_type(self) -> CVIModuleType:
        return CVIModuleType(self._com_obj.ModuleType)

    @module_type.setter
    @ts_interface
    def module_type(self, value: CVIModuleType | int) -> None:
        self._com_obj.ModuleType = int(value)

    @property
    @ts_interface
    def parameters(self) -> CVIParameterList:
        return CVIParameterList(self._com_obj.Parameters, self._engine_ref)


class CVIParameterList:
    def __init__(self, com_obj: typing.Any, engine: typing.Any = None) -> None:
        self._com_obj: typing.Any = com_obj
        self._engine_ref = engine

    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def delete(self, index: int) -> typing.Any:
        self._com_obj.Delete(index)

    @ts_interface
    def item(self, index: typing.Any) -> typing.Any:
        return CVIParameter(self._com_obj.Item(index), self._engine_ref)

    @ts_interface
    def move(self, index: int, new_index: int) -> typing.Any:
        self._com_obj.Move(index, new_index)

    @ts_interface
    def new(
        self,
        index: int,
        parameter_name: str,
        parameter_value_expr: str,
        parameter_category: CVIParameterCategory | int,
        parameter_pass: CommonCParameterPassOption | int,
        parameter_type: CommonCParameterType | int,
    ) -> None:
        self._com_obj.New(
            index,
            parameter_name,
            parameter_value_expr,
            int(parameter_category),
            int(parameter_pass),
            int(parameter_type),
        )

    @ts_interface
    def new_arguments(self) -> CVIArgumentList:
        return CVIArgumentList(self._com_obj.NewArguments(), self._engine_ref)

    def release(self) -> None:
        "Releases the underlying COM object."
        self._com_obj = None

    def __del__(self) -> None:
        try:
            self.release()
        except Exception:
            pass


class CVIArgument(PropertyObject):
    def __init__(self, com_obj: typing.Any, engine: typing.Any = None) -> None:
        super().__init__(com_obj, engine)

    @property
    @ts_interface
    def value(self) -> PropertyObject:
        return PropertyObject(self._com_obj.Value, self._engine_ref)

    @value.setter
    @ts_interface
    def value(self, val: typing.Any) -> None:
        self._com_obj.Value = val._com_obj if hasattr(val, "_com_obj") else val


class CVIParameter(COMWrapper):
    @property
    @ts_interface
    def category(self) -> CVIParameterCategory:
        return CVIParameterCategory(self._com_obj.Category)

    @category.setter
    @ts_interface
    def category(self, value: CVIParameterCategory | int) -> None:
        self._com_obj.Category = int(value)

    @property
    @ts_interface
    def type(self) -> CommonCParameterType:
        return CommonCParameterType(self._com_obj.Type)

    @type.setter
    @ts_interface
    def type(self, value: CommonCParameterType | int) -> None:
        self._com_obj.Type = int(value)

    @ts_interface
    def as_common_c_parameter(self) -> CommonCParameter:
        return CommonCParameter(self._com_obj.AsCommonCParameter(), self._engine_ref)

    def release(self) -> None:
        "Releases the underlying COM object."
        self._com_obj = None

    def __del__(self) -> None:
        try:
            self.release()
        except Exception:
            pass


class CVIArgumentList:
    def __init__(self, com_obj: typing.Any, engine: typing.Any = None) -> None:
        self._com_obj: typing.Any = com_obj
        self._engine_ref = engine

    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index: typing.Any) -> typing.Any:
        return CVIArgument(self._com_obj.Item(index), self._engine_ref)

    def release(self) -> None:
        "Releases the underlying COM object."
        self._com_obj = None

    def __del__(self) -> None:
        try:
            self.release()
        except Exception:
            pass
