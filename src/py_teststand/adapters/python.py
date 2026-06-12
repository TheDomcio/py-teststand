from __future__ import annotations

import typing
from enum import IntEnum

from py_teststand.adapters.adapter import Adapter, Module
from py_teststand.core.com_wrapper import COMWrapper, ts_interface


class PythonInterpreterSessionScope(IntEnum):
    Global = 0x3
    ObjectReference = 0x0
    PerExecution = 0x2
    PerThread = 0x1


class PythonOperationScope(IntEnum):
    Class = 0x1
    ClassInstance = 0x2
    Module = 0x0


class PythonOperationType(IntEnum):
    CallMethod = 0x1
    CreateClassInstance = 0x0
    GetAttribute = 0x2
    SetAttribute = 0x3


class PythonParameterCategory(IntEnum):
    Boolean = 0x3
    Dispatch = 0x8
    Dynamic = 0x7
    Enum = 0x9
    List = 0x5
    NoneValue = 0x0
    Number = 0x1
    Object = 0x10
    Sequence = 0x6
    String = 0x2
    Tuple = 0x4


class PythonModuleArrayParameterCategory(IntEnum):
    List = 5
    NumPyArray = 16


if typing.TYPE_CHECKING:
    from py_teststand.property.property_object import PropertyObject
    from py_teststand.sequence.expression import EvaluationTypes


class PythonParameter(COMWrapper):
    @property
    @ts_interface
    def category(self) -> PythonParameterCategory:
        return PythonParameterCategory(self._com_obj.Category)

    @category.setter
    @ts_interface
    def category(self, value: PythonParameterCategory | int) -> None:
        self._com_obj.Category = int(value)

    @property
    @ts_interface
    def parameter_name(self) -> str:
        return str(self._com_obj.ParameterName)

    @parameter_name.setter
    @ts_interface
    def parameter_name(self, value: str) -> None:
        self._com_obj.ParameterName = value

    @property
    @ts_interface
    def valid_evaluation_types(self) -> EvaluationTypes:
        from py_teststand.sequence.expression import EvaluationTypes

        return EvaluationTypes(self._com_obj.ValidEvaluationTypes, self._engine_ref)

    @property
    @ts_interface
    def value_expr(self) -> str:
        return str(self._com_obj.ValueExpr)

    @value_expr.setter
    @ts_interface
    def value_expr(self, value: str) -> None:
        self._com_obj.ValueExpr = value

    @ts_interface
    def as_property_object(self) -> PropertyObject:
        from py_teststand.property.property_object import PropertyObject

        return PropertyObject(self._com_obj.AsPropertyObject(), self._engine_ref)


class PythonParameters(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index: int | str) -> PythonParameter:
        return PythonParameter(self._com_obj.Item(index), self._engine_ref)

    def __len__(self) -> int:
        return self.count

    def __getitem__(self, index: int | str) -> PythonParameter:
        return self.item(index)

    def __iter__(self) -> typing.Iterator[PythonParameter]:
        for i in range(self.count):
            yield self[i]

    @ts_interface
    def delete(self, index: int | str) -> None:
        self._com_obj.Delete(index)

    @ts_interface
    def move(self, current_index: int, new_index: int) -> None:
        self._com_obj.Move(current_index, new_index)

    @ts_interface
    def new(self, name: str, index: int = -1) -> PythonParameter:
        return PythonParameter(self._com_obj.New(name, index), self._engine_ref)


class PythonArgument(COMWrapper):
    @property
    @ts_interface
    def value(self) -> typing.Any:
        return self._com_obj.Value

    @value.setter
    @ts_interface
    def value(self, value: typing.Any) -> None:
        self._com_obj.Value = value


class PythonArguments(COMWrapper):
    @property
    @ts_interface
    def class_instance_reference_object(self) -> PropertyObject:
        from py_teststand.property.property_object import PropertyObject

        return PropertyObject(self._com_obj.ClassInstanceReferenceObject, self._engine_ref)

    @class_instance_reference_object.setter
    @ts_interface
    def class_instance_reference_object(self, value: PropertyObject) -> None:
        self._com_obj.ClassInstanceReferenceObject = value._com_obj

    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @property
    @ts_interface
    def interpreter_reference_object(self) -> PropertyObject:
        from py_teststand.property.property_object import PropertyObject

        return PropertyObject(self._com_obj.InterpreterReferenceObject, self._engine_ref)

    @interpreter_reference_object.setter
    @ts_interface
    def interpreter_reference_object(self, value: PropertyObject) -> None:
        self._com_obj.InterpreterReferenceObject = value._com_obj

    @ts_interface
    def item(self, index: int | str) -> PythonArgument:
        return PythonArgument(self._com_obj.Item(index), self._engine_ref)

    def __len__(self) -> int:
        return self.count

    def __getitem__(self, index: int | str) -> PythonArgument:
        return self.item(index)

    def __iter__(self) -> typing.Iterator[PythonArgument]:
        for i in range(self.count):
            yield self[i]


class PythonModule(Module):
    @property
    @ts_interface
    def class_instance_location_expr(self) -> str:
        return str(self._com_obj.ClassInstanceLocationExpr)

    @class_instance_location_expr.setter
    @ts_interface
    def class_instance_location_expr(self, value: str) -> None:
        self._com_obj.ClassInstanceLocationExpr = value

    @property
    @ts_interface
    def class_name(self) -> str:
        return str(self._com_obj.ClassName)

    @class_name.setter
    @ts_interface
    def class_name(self, value: str) -> None:
        self._com_obj.ClassName = value

    @property
    @ts_interface
    def create_interpreter_session_if_does_not_exist(self) -> bool:
        return bool(self._com_obj.CreateInterpreterSessionIfDoesNotExist)

    @create_interpreter_session_if_does_not_exist.setter
    @ts_interface
    def create_interpreter_session_if_does_not_exist(self, value: bool) -> None:
        self._com_obj.CreateInterpreterSessionIfDoesNotExist = value

    @property
    @ts_interface
    def default_parameter_category_for_array(self) -> PythonParameterCategory:
        return PythonParameterCategory(self._com_obj.DefaultParameterCategoryForArray)

    @default_parameter_category_for_array.setter
    @ts_interface
    def default_parameter_category_for_array(self, value: PythonParameterCategory | int) -> None:
        self._com_obj.DefaultParameterCategoryForArray = int(value)

    @property
    @ts_interface
    def function_or_attribute_name(self) -> str:
        return str(self._com_obj.FunctionOrAttributeName)

    @function_or_attribute_name.setter
    @ts_interface
    def function_or_attribute_name(self, value: str) -> None:
        self._com_obj.FunctionOrAttributeName = value

    @property
    @ts_interface
    def interpreter_reference_expr(self) -> str:
        return str(self._com_obj.InterpreterReferenceExpr)

    @interpreter_reference_expr.setter
    @ts_interface
    def interpreter_reference_expr(self, value: str) -> None:
        self._com_obj.InterpreterReferenceExpr = value

    @property
    @ts_interface
    def interpreter_session_scope(self) -> PythonInterpreterSessionScope:
        return PythonInterpreterSessionScope(self._com_obj.InterpreterSessionScope)

    @interpreter_session_scope.setter
    @ts_interface
    def interpreter_session_scope(self, value: PythonInterpreterSessionScope | int) -> None:
        self._com_obj.InterpreterSessionScope = int(value)

    @property
    @ts_interface
    def module_path(self) -> str:
        return str(self._com_obj.ModulePath)

    @module_path.setter
    @ts_interface
    def module_path(self, value: str) -> None:
        self._com_obj.ModulePath = value

    @property
    @ts_interface
    def operation_scope(self) -> PythonOperationScope:
        return PythonOperationScope(self._com_obj.OperationScope)

    @operation_scope.setter
    @ts_interface
    def operation_scope(self, value: PythonOperationScope | int) -> None:
        self._com_obj.OperationScope = int(value)

    @property
    @ts_interface
    def operation_type(self) -> PythonOperationType:
        return PythonOperationType(self._com_obj.OperationType)

    @operation_type.setter
    @ts_interface
    def operation_type(self, value: PythonOperationType | int) -> None:
        self._com_obj.OperationType = int(value)

    @property
    @ts_interface
    def parameters(self) -> PythonParameters:
        return PythonParameters(self._com_obj.Parameters, self._engine_ref)

    @property
    @ts_interface
    def python_version(self) -> str:
        return str(self._com_obj.PythonVersion)

    @python_version.setter
    @ts_interface
    def python_version(self, value: str) -> None:
        self._com_obj.PythonVersion = value

    @property
    @ts_interface
    def python_virtual_environment_path(self) -> str:
        return str(self._com_obj.PythonVirtualEnvironmentPath)

    @python_virtual_environment_path.setter
    @ts_interface
    def python_virtual_environment_path(self, value: str) -> None:
        self._com_obj.PythonVirtualEnvironmentPath = value

    @property
    @ts_interface
    def use_adapter_settings_for_interpreter_session(self) -> bool:
        return bool(self._com_obj.UseAdapterSettingsForInterpreterSession)

    @use_adapter_settings_for_interpreter_session.setter
    @ts_interface
    def use_adapter_settings_for_interpreter_session(self, value: bool) -> None:
        self._com_obj.UseAdapterSettingsForInterpreterSession = value

    @ts_interface
    def as_module(self) -> Module:
        return Module(self._com_obj.AsModule(), self._engine_ref)

    @ts_interface
    def execute(self, arguments: PythonArguments) -> None:
        self._com_obj.Execute(arguments._com_obj)

    @ts_interface
    def new_arguments(self) -> PythonArguments:
        return PythonArguments(self._com_obj.NewArguments(), self._engine_ref)


class PythonAdapter(Adapter):
    @property
    @ts_interface
    def debug_just_my_code(self) -> bool:
        return bool(self._com_obj.DebugJustMyCode)

    @debug_just_my_code.setter
    @ts_interface
    def debug_just_my_code(self, value: bool) -> None:
        self._com_obj.DebugJustMyCode = value

    @property
    @ts_interface
    def display_console_for_interpreter_sessions(self) -> bool:
        return bool(self._com_obj.DisplayConsoleForInterpreterSessions)

    @display_console_for_interpreter_sessions.setter
    @ts_interface
    def display_console_for_interpreter_sessions(self, value: bool) -> None:
        self._com_obj.DisplayConsoleForInterpreterSessions = value

    @property
    @ts_interface
    def enable_debugging(self) -> bool:
        return bool(self._com_obj.EnableDebugging)

    @enable_debugging.setter
    @ts_interface
    def enable_debugging(self, value: bool) -> None:
        self._com_obj.EnableDebugging = value

    @property
    @ts_interface
    def interpreter_session_scope(self) -> PythonInterpreterSessionScope:
        return PythonInterpreterSessionScope(self._com_obj.InterpreterSessionScope)

    @interpreter_session_scope.setter
    @ts_interface
    def interpreter_session_scope(self, value: PythonInterpreterSessionScope | int) -> None:
        self._com_obj.InterpreterSessionScope = int(value)

    @property
    @ts_interface
    def python_executable_path(self) -> str:
        return str(self._com_obj.PythonExecutablePath)

    @python_executable_path.setter
    @ts_interface
    def python_executable_path(self, value: str) -> None:
        self._com_obj.PythonExecutablePath = value

    @property
    @ts_interface
    def python_version(self) -> str:
        return str(self._com_obj.PythonVersion)

    @python_version.setter
    @ts_interface
    def python_version(self, value: str) -> None:
        self._com_obj.PythonVersion = value

    @property
    @ts_interface
    def python_virtual_environment_path(self) -> str:
        return str(self._com_obj.PythonVirtualEnvironmentPath)

    @python_virtual_environment_path.setter
    @ts_interface
    def python_virtual_environment_path(self, value: str) -> None:
        self._com_obj.PythonVirtualEnvironmentPath = value

    @property
    @ts_interface
    def reload_modified_modules_during_execution(self) -> bool:
        return bool(self._com_obj.ReloadModifiedModulesDuringExecution)

    @reload_modified_modules_during_execution.setter
    @ts_interface
    def reload_modified_modules_during_execution(self, value: bool) -> None:
        self._com_obj.ReloadModifiedModulesDuringExecution = value

    @ts_interface
    def as_adapter(self) -> Adapter:
        return Adapter(self._com_obj.AsAdapter(), self._engine_ref)

    @ts_interface
    def get_enum_type_mapping(self, enum_type_name: str) -> str:
        return str(self._com_obj.GetEnumTypeMapping(enum_type_name))

    @ts_interface
    def get_exclude_from_object(
        self,
        type_definition: PropertyObject,
        property_lookup_string: str,
    ) -> bool:
        return bool(
            self._com_obj.GetExcludeFromObject(type_definition._com_obj, property_lookup_string),
        )

    @ts_interface
    def get_parameter_category_in_object(
        self,
        type_definition: PropertyObject,
        property_lookup_string: str,
    ) -> PythonParameterCategory:
        return PythonParameterCategory(
            self._com_obj.GetParameterCategoryInObject(
                type_definition._com_obj,
                property_lookup_string,
            ),
        )

    @ts_interface
    def new_module(self) -> PythonModule:
        return PythonModule(self._com_obj.NewModule(), self._engine_ref)

    @ts_interface
    def set_enum_type_mapping(self, enum_type_name: str, python_enum_name: str) -> None:
        self._com_obj.SetEnumTypeMapping(enum_type_name, python_enum_name)

    @ts_interface
    def set_exclude_from_object(
        self,
        type_definition: PropertyObject,
        property_lookup_string: str,
        exclude: bool,
    ) -> None:
        self._com_obj.SetExcludeFromObject(
            type_definition._com_obj,
            property_lookup_string,
            exclude,
        )

    @ts_interface
    def set_parameter_category_in_object(
        self,
        type_definition: PropertyObject,
        property_lookup_string: str,
        category: PythonParameterCategory | int,
    ) -> None:
        self._com_obj.SetParameterCategoryInObject(
            type_definition._com_obj,
            property_lookup_string,
            int(category),
        )

    @ts_interface
    def validate_module(self, module_to_validate: PythonModule) -> bool:
        return bool(self._com_obj.ValidateModule(module_to_validate._com_obj))

    @ts_interface
    def validate_python_version_and_virtual_environment_path(
        self,
        python_version: str,
        virtual_env_path: str,
    ) -> str:
        return str(
            self._com_obj.ValidatePythonVersionAndVirtualEnvironmentPath(
                python_version,
                virtual_env_path,
            ),
        )
