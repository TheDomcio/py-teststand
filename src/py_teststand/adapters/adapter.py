from __future__ import annotations

import logging
import typing
from enum import IntEnum
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.property.property_object import PropertyObject

if TYPE_CHECKING:
    from py_teststand.adapters.activex import ActiveXModule
    from py_teststand.adapters.dll import DLLModule
    from py_teststand.adapters.dotnet import DotNetModule
    from py_teststand.adapters.labview import LabVIEWModule
    from py_teststand.adapters.sequence import SequenceCallModule
    from py_teststand.sequence.expression import EvaluationTypes


class AdapterCodeTemplatePolicy(IntEnum):
    UseOnlyNew = 0
    UseOnlyLegacy = 1
    UseNewAndLegacy = 2


class CommonCParameterType(IntEnum):
    Int8 = 0
    UInt8 = 1
    Int16 = 2
    UInt16 = 3
    Int32 = 4
    UInt32 = 5
    Float32 = 6
    Float64 = 7
    Int64 = 8
    UInt64 = 9
    CString = 0x20
    UnicodeString = 0x21
    CStringBuffer = 0x22
    UnicodeStringBuffer = 0x23
    IDispatch = 0x40
    CVIHandle = 0x41
    IUnknown = 0x42
    NotUsed = 200


class CommonCParameterPassOption(IntEnum):
    ByVal = 0
    ByPointer = 1
    ByReference = 0x10
    ByConstPointer = 0x41
    ByConstReference = 0x50


class CommonCParameterResultAction(IntEnum):
    NoAction = 0
    SetErrorIfNegative = 1
    SetErrorIfPositive = 2
    SetErrorIfZero = 3
    SetErrorIfNotZero = 4
    SetErrorCodeToReturnValue = 5


class CommonCParameterUnknownInfoFlag(IntEnum):
    EverythingKnown = 0
    DontKnowNumElements = 1
    DontKnowIfArrayOrPointer = 2
    DontKnowFirstDimensionSize = 3


class CommonCVerifyPrototypeResult(IntEnum):
    PrototypesMatch = 0
    ModuleUpdated = 1
    SourceUpdated = 2
    UserCancelled = 3


class DllCodeCreationTarget(IntEnum):
    TextFile = 0
    VisualStudio = 1


class DllInfoType(IntEnum):
    NoneValue = 0
    Enumeration = 1
    Struct = 2


logger = logging.getLogger(__name__)


class Adapter(PropertyObject):
    def __init__(self, com_obj: typing.Any, engine: typing.Any = None) -> None:
        super().__init__(com_obj, engine)

    @property
    def name(self) -> str:
        return self.key_name

    @property
    @ts_interface
    def key_name(self) -> str:
        return str(self._com_obj.KeyName)

    @property
    @ts_interface
    def display_name(self) -> str:
        return str(self._com_obj.DisplayName)

    @property
    @ts_interface
    def icon_name(self) -> str:
        return str(self._com_obj.IconName)

    @property
    @ts_interface
    def hidden(self) -> bool:
        return bool(self._com_obj.Hidden)

    @hidden.setter
    @ts_interface
    def hidden(self, value: bool) -> None:
        self._com_obj.Hidden = value

    @property
    def is_hidden(self) -> bool:
        return self.hidden

    @property
    @ts_interface
    def is_configurable(self) -> bool:
        return bool(self._com_obj.IsConfigurable)

    @property
    @ts_interface
    def is_supported(self) -> bool:
        return bool(self._com_obj.IsSupported)

    @property
    @ts_interface
    def large_icon(self) -> typing.Any:
        return self._com_obj.LargeIcon

    @property
    @ts_interface
    def large_icon_index(self) -> int:
        return int(self._com_obj.LargeIconIndex)

    @property
    @ts_interface
    def small_icon(self) -> typing.Any:
        return self._com_obj.SmallIcon

    @property
    @ts_interface
    def small_icon_index(self) -> int:
        return int(self._com_obj.SmallIconIndex)

    @property
    @ts_interface
    def show_args_in_step_description(self) -> bool:
        return bool(self._com_obj.ShowArgsInStepDescription)

    @show_args_in_step_description.setter
    @ts_interface
    def show_args_in_step_description(self, value: bool) -> None:
        self._com_obj.ShowArgsInStepDescription = value

    @property
    @ts_interface
    def can_create_code(self) -> bool:
        return bool(self._com_obj.CanCreateCode)

    @property
    @ts_interface
    def can_edit_code(self) -> bool:
        return bool(self._com_obj.CanEditCode)

    @ts_interface
    def configure(self, modal_window_handle: int = 0) -> bool:
        return bool(self._com_obj.Configure(modal_window_handle))

    @ts_interface
    def as_property_object(self) -> PropertyObject:
        return PropertyObject(self._com_obj.AsPropertyObject(), self._engine_ref)


class CommonCParameter(PropertyObject):
    @property
    @ts_interface
    def name(self) -> str:
        return str(self._com_obj.Name)

    @name.setter
    @ts_interface
    def name(self, value: str) -> None:
        self._com_obj.Name = value

    @property
    @ts_interface
    def type_name(self) -> str:
        return str(self._com_obj.TypeName)

    @type_name.setter
    @ts_interface
    def type_name(self, value: str) -> None:
        self._com_obj.TypeName = value

    @property
    @ts_interface
    def array_dimensions(self) -> int:
        return int(self._com_obj.ArrayDimensions)

    @array_dimensions.setter
    @ts_interface
    def array_dimensions(self, value: int) -> None:
        self._com_obj.ArrayDimensions = value

    @property
    @ts_interface
    def display_value_expr(self) -> str:
        return str(self._com_obj.DisplayValueExpr)

    @property
    @ts_interface
    def enum_type_name(self) -> str:
        return str(self._com_obj.EnumTypeName)

    @property
    @ts_interface
    def flags(self) -> int:
        return int(self._com_obj.Flags)

    @flags.setter
    @ts_interface
    def flags(self, value: int) -> None:
        self._com_obj.Flags = value

    @ts_interface
    def display_create_custom_data_type_dialog(self, sequence_context: typing.Any) -> bool:
        raw_ctx = getattr(sequence_context, "_com_obj", sequence_context)
        return bool(self._com_obj.DisplayCreateCustomDataTypeDialog(raw_ctx))

    @ts_interface
    def enum_type_param_is_compatible(self, enum_type_name: str) -> bool:
        return bool(self._com_obj.EnumTypeParamIsCompatible(enum_type_name))

    @ts_interface
    def get_array_dimension_size(self, dimension: int) -> int:
        return int(self._com_obj.GetArrayDimensionSize(dimension))

    @ts_interface
    def get_array_dimension_size_expr(self, dimension: int) -> str:
        return str(self._com_obj.GetArrayDimensionSizeExpr(dimension))

    @ts_interface
    def get_description(self) -> str:
        return str(self._com_obj.GetDescription())

    @ts_interface
    def get_dll_info_type(self) -> DllInfoType:
        return DllInfoType(self._com_obj.GetDllInfoType())

    @ts_interface
    def get_enum_values(self) -> list[PropertyObject]:
        return [PropertyObject(po, self._engine_ref) for po in self._com_obj.GetEnumValues()]

    @property
    @ts_interface
    def parameter_name(self) -> str:
        return str(self._com_obj.ParameterName)

    @property
    @ts_interface
    def pass_opt(self) -> CommonCParameterPassOption:

        return CommonCParameterPassOption(self._com_obj.Pass)

    @pass_opt.setter
    @ts_interface
    def pass_opt(self, value: CommonCParameterPassOption | int) -> None:
        self._com_obj.Pass = int(value)

    @property
    @ts_interface
    def pass_array_element_by(self) -> PassArrayElementByOption:
        return PassArrayElementByOption(self._com_obj.PassArrayElementBy)

    @pass_array_element_by.setter
    @ts_interface
    def pass_array_element_by(self, value: PassArrayElementByOption | int) -> None:
        self._com_obj.PassArrayElementBy = int(value)

    @property
    @ts_interface
    def result_action(self) -> CommonCParameterResultAction:
        return CommonCParameterResultAction(self._com_obj.ResultAction)

    @result_action.setter
    @ts_interface
    def result_action(self, value: CommonCParameterResultAction | int) -> None:
        self._com_obj.ResultAction = int(value)

    @ts_interface
    def numeric_type_param_is_compatible(self, numeric_type_name: str) -> bool:
        return bool(self._com_obj.NumericTypeParamIsCompatible(numeric_type_name))

    @property
    @ts_interface
    def string_buffer_size(self) -> int:
        return int(self._com_obj.StringBufferSize)

    @string_buffer_size.setter
    @ts_interface
    def string_buffer_size(self, value: int) -> None:
        self._com_obj.StringBufferSize = value

    @property
    @ts_interface
    def string_buffer_size_expr(self) -> str:
        return str(self._com_obj.StringBufferSizeExpr)

    @string_buffer_size_expr.setter
    @ts_interface
    def string_buffer_size_expr(self, value: str) -> None:
        self._com_obj.StringBufferSizeExpr = value

    @property
    @ts_interface
    def struct_type(self) -> str:
        return str(self._com_obj.StructType)

    @struct_type.setter
    @ts_interface
    def struct_type(self, value: str) -> None:
        self._com_obj.StructType = value

    @ts_interface
    def set_array_dimension_size(self, dimension: int, size: int) -> typing.Any:
        self._com_obj.SetArrayDimensionSize(dimension, size)

    @ts_interface
    def set_array_dimension_size_expr(self, dimension: int, size_expr: str) -> typing.Any:
        self._com_obj.SetArrayDimensionSizeExpr(dimension, size_expr)

    @property
    @ts_interface
    def unknown_info(self) -> CommonCParameterUnknownInfoFlag:
        return CommonCParameterUnknownInfoFlag(self._com_obj.UnknownInfo)

    @unknown_info.setter
    @ts_interface
    def unknown_info(self, value: CommonCParameterUnknownInfoFlag | int) -> None:
        self._com_obj.UnknownInfo = int(value)

    @property
    @ts_interface
    def user_data(self) -> PropertyObject:
        return PropertyObject(self._com_obj.UserData, self._engine_ref)

    @user_data.setter
    @ts_interface
    def user_data(self, value: PropertyObject) -> None:
        self._com_obj.UserData = value._com_obj

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

    @property
    @ts_interface
    def value_expr_is_ignored(self) -> bool:
        return bool(self._com_obj.ValueExprIsIgnored)

    @value_expr_is_ignored.setter
    @ts_interface
    def value_expr_is_ignored(self, value: bool) -> None:
        self._com_obj.ValueExprIsIgnored = value

    @property
    @ts_interface
    def value_expr_is_optional(self) -> bool:
        return bool(self._com_obj.ValueExprIsOptional)

    @ts_interface
    def as_property_object(self) -> PropertyObject:
        return PropertyObject(self._com_obj.AsPropertyObject(), self._engine_ref)


class PassArrayElementByOption(IntEnum):
    ByVal = 0
    ByAddr = 1


class ModuleType(IntEnum):
    RuleAnalysisModule = 0
    RuleConfigurationModule = 1


class Module(PropertyObject):
    @property
    @ts_interface
    def adapter(self) -> typing.Any:
        return Adapter(self._com_obj.Adapter, self._engine_ref)

    @property
    @ts_interface
    def can_create_code(self) -> bool:
        return bool(self._com_obj.CanCreateCode)

    @property
    @ts_interface
    def can_edit_code(self) -> bool:
        return bool(self._com_obj.CanEditCode)

    @property
    @ts_interface
    def can_specify(self) -> bool:
        return bool(self._com_obj.CanSpecify)

    @ts_interface
    def clear_unmapped_argument_values(self) -> None:
        self._com_obj.ClearUnmappedArgumentValues()

    @ts_interface
    def create_code(self) -> bool:
        return bool(self._com_obj.CreateCode())

    @ts_interface
    def edit_code(self) -> bool:
        return bool(self._com_obj.EditCode())

    @ts_interface
    def get_description(self) -> typing.Any:
        return str(self._com_obj.GetDescription())

    @ts_interface
    def get_last_load_warnings(self) -> list[str]:
        return list(self._com_obj.GetLastLoadWarnings())

    @ts_interface
    def is_prototype_incompatible(self) -> bool:
        return bool(self._com_obj.IsPrototypeIncompatible())

    @ts_interface
    def load(self, load_options: int = 0, sequence_context: typing.Any = None) -> typing.Any:
        raw_ctx = (
            getattr(sequence_context, "_com_obj", sequence_context) if sequence_context else None
        )
        return bool(self._com_obj.Load(int(load_options), raw_ctx))

    @ts_interface
    def specify(self, options: int = 0) -> typing.Any:
        return bool(self._com_obj.Specify(int(options)))

    @property
    @ts_interface
    def step(self) -> typing.Any:
        from py_teststand.sequence.step import Step

        return Step(self._com_obj.Step, self._engine_ref)

    @ts_interface
    def unload(self) -> bool:
        return bool(self._com_obj.Unload())

    @property
    @ts_interface
    def unmapped_argument_values(self) -> UnmappedArgumentValueList:
        return UnmappedArgumentValueList(self._com_obj.UnmappedArgumentValues, self._engine_ref)

    @ts_interface
    def load_prototype(self, options: int = 0) -> typing.Any:
        return bool(self._com_obj.LoadPrototype(options))

    @ts_interface
    def evaluate_ex(self, expression: str, options: int = 0) -> typing.Any:

        return self._com_obj.EvaluateEx(expression, options)

    @ts_interface
    def as_property_object(self) -> PropertyObject:
        return PropertyObject(self._com_obj.AsPropertyObject(), self._engine_ref)

    @ts_interface
    def as_dot_net_module(self) -> DotNetModule:
        from py_teststand.adapters.dotnet import DotNetModule

        return DotNetModule(self._com_obj, self._engine_ref)

    @ts_interface
    def as_labview_module(self) -> LabVIEWModule:
        from py_teststand.adapters.labview import LabVIEWModule

        return LabVIEWModule(self._com_obj, self._engine_ref)

    @ts_interface
    def as_activex_module(self) -> ActiveXModule:
        from py_teststand.adapters.activex import ActiveXModule

        return ActiveXModule(self._com_obj, self._engine_ref)

    @ts_interface
    def as_dll_module(self) -> DLLModule:
        from py_teststand.adapters.dll import DLLModule

        return DLLModule(self._com_obj, self._engine_ref)

    @ts_interface
    def as_sequence_call_module(self) -> SequenceCallModule:
        from py_teststand.adapters.sequence import SequenceCallModule

        return SequenceCallModule(self._com_obj, self._engine_ref)

    @property
    @ts_interface
    def comment(self) -> str:
        return str(self._com_obj.Comment)

    @property
    @ts_interface
    def name(self) -> str:
        return str(self._com_obj.Name)

    @property
    @ts_interface
    def description(self) -> str:
        return str(self._com_obj.Description)

    @property
    @ts_interface
    def path(self) -> str:
        return str(self._com_obj.Path)


class CommonCModule(Module):
    @property
    @ts_interface
    def code_template_name(self) -> str:
        return str(self._com_obj.CodeTemplateName)

    @code_template_name.setter
    @ts_interface
    def code_template_name(self, value: str) -> None:
        self._com_obj.CodeTemplateName = value

    @property
    @ts_interface
    def function_name(self) -> str:
        return str(self._com_obj.FunctionName)

    @function_name.setter
    @ts_interface
    def function_name(self, value: str) -> None:
        self._com_obj.FunctionName = value

    @property
    @ts_interface
    def function_call(self) -> str:
        return str(self._com_obj.FunctionCall)

    @ts_interface
    def load_prototype_from_code_template(self) -> None:
        self._com_obj.LoadPrototypeFromCodeTemplate()

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
    def project_file_path(self) -> str:
        return str(self._com_obj.ProjectFilePath)

    @project_file_path.setter
    @ts_interface
    def project_file_path(self, value: str) -> None:
        self._com_obj.ProjectFilePath = value

    @property
    @ts_interface
    def source_file_path(self) -> str:
        return str(self._com_obj.SourceFilePath)

    @source_file_path.setter
    @ts_interface
    def source_file_path(self, value: str) -> None:
        self._com_obj.SourceFilePath = value

    @ts_interface
    def update_prototype_from_source(self) -> bool:
        return bool(self._com_obj.UpdatePrototypeFromSource())

    @ts_interface
    def verify_prototype(self, options: int = 0) -> CommonCVerifyPrototypeResult:
        return CommonCVerifyPrototypeResult(self._com_obj.VerifyPrototype(options))

    @ts_interface
    def verify_prototype_from_source(self, options: int = 0) -> CommonCVerifyPrototypeResult:
        return CommonCVerifyPrototypeResult(self._com_obj.VerifyPrototypeFromSource(options))

    @property
    @ts_interface
    def workspace_file_path(self) -> str:
        return str(self._com_obj.WorkspaceFilePath)

    @workspace_file_path.setter
    @ts_interface
    def workspace_file_path(self, value: str) -> None:
        self._com_obj.WorkspaceFilePath = value

    @ts_interface
    def as_module(self) -> Module:
        return Module(self._com_obj.AsModule(), self._engine_ref)

    @ts_interface
    def accept_function_call(
        self,
        evaluation_context: PropertyObject,
        func_call: str,
        allow_editing_prototype: bool,
    ) -> bool:
        return bool(
            self._com_obj.AcceptFunctionCall(
                evaluation_context._com_obj,
                func_call,
                allow_editing_prototype,
            ),
        )


class UnmappedArgumentValue(COMWrapper):
    @property
    @ts_interface
    def name(self) -> str:
        return str(self._com_obj.Name)

    @property
    @ts_interface
    def type_name(self) -> str:
        return str(self._com_obj.TypeName)

    @property
    @ts_interface
    def unmapped_argument_values(self) -> UnmappedArgumentValueList:
        return UnmappedArgumentValueList(self._com_obj.UnmappedArgumentValues, self._engine_ref)

    @property
    @ts_interface
    def value_expr(self) -> str:
        return str(self._com_obj.ValueExpr)


class UnmappedArgumentValueList(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index: typing.Any) -> typing.Any:
        return UnmappedArgumentValue(self._com_obj.Item(index), self._engine_ref)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    def __len__(self) -> int:
        return self.count

    def __getitem__(self, index: (int | str)) -> UnmappedArgumentValue:
        return self.item(index)
