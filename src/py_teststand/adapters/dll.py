from __future__ import annotations

import typing
from enum import IntEnum, IntFlag
from typing import TYPE_CHECKING

from py_teststand.adapters.adapter import (
    Adapter,
    CommonCModule,
    CommonCParameterPassOption,
    CommonCParameterType,
    DllCodeCreationTarget,
)
from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.property.property_object import PropertyObject


class StructMemberArrayStorageOption(IntEnum):
    InlineArray = 0x100
    ArrayPointer = 0x101
    LabVIEWArray = 0x102


class StructMemberStorageOption(IntEnum):
    InlineString = 0
    StringPointer = 1
    LabVIEWString = 2
    EmbeddedStruct = 32
    StructPointer = 33


class StructPassingOption(IntFlag):
    AdapterDefault = 0x0
    OneByte = 0x1
    TwoByte = 0x2
    FourByte = 0x4
    EightByte = 0x8
    SixteenByte = 16


class StructMemberType(IntEnum):
    Float32 = 0
    Float64 = 1
    Int8 = 2
    UInt8 = 3
    Int16 = 4
    UInt16 = 5
    Int32 = 6
    UInt32 = 7
    Int64 = 8
    UInt64 = 9
    CString = 0x20
    UnicodeString = 0x21
    CStringBuffer = 0x22
    UnicodeStringBuffer = 0x23
    IDispatch = 0x40
    CVIHandle = 0x41
    IUnknown = 0x42


class CommonCParameterFlag(IntFlag):
    NoneValue = 0
    SetErrorCodeToReturnValue = 1


class DLLParameterCategory(IntEnum):
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
    Boolean = 100
    BooleanArray = 101
    CNiVector = 200
    CNiMatrix = 201
    CNiComplex = 202
    CNiString = 203
    CNiComplexVector = 204
    TSObject = 205
    CNiBoolVector = 206
    CString = 207
    CStringArray = 208
    Bstr_t = 209
    CNiStringVector = 210


if TYPE_CHECKING:
    from py_teststand.adapters import DLLModule


class DLLAdapter(Adapter):
    @property
    @ts_interface
    def visual_studio_dte_version_for_debugging(self) -> typing.Any:
        return str(self._com_obj.VisualStudioDTEVersionForDebugging)

    @visual_studio_dte_version_for_debugging.setter
    @ts_interface
    def visual_studio_dte_version_for_debugging(self, value: str) -> None:
        self._com_obj.VisualStudioDTEVersionForDebugging = value

    @property
    @ts_interface
    def visual_studio_dte_version_for_editing(self) -> typing.Any:
        return str(self._com_obj.VisualStudioDTEVersionForEditing)

    @visual_studio_dte_version_for_editing.setter
    @ts_interface
    def visual_studio_dte_version_for_editing(self, value: str) -> None:
        self._com_obj.VisualStudioDTEVersionForEditing = value

    @ts_interface
    def as_adapter(self) -> Adapter:
        return Adapter(self._com_obj.AsAdapter(), self._engine_ref)

    @ts_interface
    def as_common_c_adapter(self) -> CommonCAdapter:
        return CommonCAdapter(self._com_obj.AsCommonCAdapter(), self._engine_ref)

    @ts_interface
    def new_module(self) -> DLLModule:
        from py_teststand.adapters import DLLModule

        return DLLModule(self._com_obj.NewModule(), self._engine_ref)


class CommonCAdapter(Adapter):
    @ts_interface
    def get_dll_functions(self, dll_path: str) -> typing.Any:
        return self._com_obj.GetDllFunctions(dll_path)

    @ts_interface
    def get_allow_struct_passing(self, type_definition: PropertyObject) -> typing.Any:
        return bool(self._com_obj.GetAllowStructPassing(type_definition._com_obj))

    @ts_interface
    def get_enumeration_names(self, include_enum_arrays: bool) -> typing.Any:
        return list(self._com_obj.GetEnumerationNames(include_enum_arrays))

    @ts_interface
    def get_exclude_from_struct(
        self,
        type_definition: PropertyObject,
        property_lookup_string: str,
    ) -> bool:
        return bool(
            self._com_obj.GetExcludeFromStruct(type_definition._com_obj, property_lookup_string),
        )

    @ts_interface
    def get_struct_member_array_storage(
        self,
        type_definition: PropertyObject,
        property_lookup_string: str,
    ) -> StructMemberArrayStorageOption:
        return StructMemberArrayStorageOption(
            self._com_obj.GetStructMemberArrayStorage(
                type_definition._com_obj,
                property_lookup_string,
            ),
        )

    @ts_interface
    def get_struct_member_storage(
        self,
        type_definition: PropertyObject,
        property_lookup_string: str,
    ) -> StructMemberStorageOption:
        return StructMemberStorageOption(
            self._com_obj.GetStructMemberStorage(type_definition._com_obj, property_lookup_string),
        )

    @ts_interface
    def get_struct_member_string_buffer_size(
        self,
        type_definition: PropertyObject,
        property_lookup_string: str,
    ) -> int:
        return int(
            self._com_obj.GetStructMemberStringBufferSize(
                type_definition._com_obj,
                property_lookup_string,
            ),
        )

    @ts_interface
    def get_struct_member_type(
        self,
        type_definition: PropertyObject,
        property_lookup_string: str,
    ) -> StructMemberType:
        return StructMemberType(
            self._com_obj.GetStructMemberType(type_definition._com_obj, property_lookup_string),
        )

    @ts_interface
    def get_struct_names(self) -> list[str]:
        return list(self._com_obj.GetStructNames())

    @ts_interface
    def get_struct_packing(self, type_definition: PropertyObject) -> StructPassingOption:
        return StructPassingOption(self._com_obj.GetStructPacking(type_definition._com_obj))

    @ts_interface
    def set_allow_struct_passing(
        self,
        type_definition: PropertyObject,
        allow_struct_passing: bool,
    ) -> None:
        self._com_obj.SetAllowStructPassing(type_definition._com_obj, allow_struct_passing)

    @ts_interface
    def set_exclude_from_struct(
        self,
        type_definition: PropertyObject,
        property_lookup_string: str,
        exclude_from_struct: bool,
    ) -> None:
        self._com_obj.SetExcludeFromStruct(
            type_definition._com_obj,
            property_lookup_string,
            exclude_from_struct,
        )

    @ts_interface
    def set_struct_member_array_storage(
        self,
        type_definition: PropertyObject,
        property_lookup_string: str,
        storage_option: StructMemberArrayStorageOption | int,
    ) -> None:
        self._com_obj.SetStructMemberArrayStorage(
            type_definition._com_obj,
            property_lookup_string,
            int(storage_option),
        )

    @ts_interface
    def set_struct_member_storage(
        self,
        type_definition: PropertyObject,
        property_lookup_string: str,
        storage_option: StructMemberStorageOption | int,
    ) -> None:
        self._com_obj.SetStructMemberStorage(
            type_definition._com_obj,
            property_lookup_string,
            int(storage_option),
        )

    @ts_interface
    def set_struct_member_string_buffer_size(
        self,
        type_definition: PropertyObject,
        property_lookup_string: str,
        buffer_size: int,
    ) -> None:
        self._com_obj.SetStructMemberStringBufferSize(
            type_definition._com_obj,
            property_lookup_string,
            buffer_size,
        )

    @ts_interface
    def set_struct_member_type(
        self,
        type_definition: PropertyObject,
        property_lookup_string: str,
        member_type: StructMemberType | int,
    ) -> None:
        self._com_obj.SetStructMemberType(
            type_definition._com_obj,
            property_lookup_string,
            int(member_type),
        )

    @ts_interface
    def set_struct_packing(
        self,
        type_definition: PropertyObject,
        packing_option: StructPassingOption | int,
    ) -> None:
        self._com_obj.SetStructPacking(type_definition._com_obj, int(packing_option))


class DLLModule(CommonCModule):
    @ts_interface
    def as_common_c_module(self) -> CommonCModule:
        return CommonCModule(self._com_obj.AsCommonCModule(), self._engine_ref)

    @property
    @ts_interface
    def code_creation_target(self) -> DllCodeCreationTarget:
        return DllCodeCreationTarget(self._com_obj.CodeCreationTarget)

    @code_creation_target.setter
    @ts_interface
    def code_creation_target(self, value: DllCodeCreationTarget | int) -> None:
        self._com_obj.CodeCreationTarget = int(value)

    @property
    @ts_interface
    def parameters(self) -> DllParameterList:
        return DllParameterList(self._com_obj.Parameters, self._engine_ref)

    @ts_interface
    def execute(
        self,
        sequence_context: typing.Any = None,
        arguments: typing.Any = None,
    ) -> typing.Any:
        ctx_obj = (
            sequence_context._com_obj if hasattr(sequence_context, "_com_obj") else sequence_context
        )
        arg_obj = arguments._com_obj if hasattr(arguments, "_com_obj") else arguments
        self._com_obj.Execute(ctx_obj, arg_obj)


class DllArgument(PropertyObject):
    def __init__(self, com_obj: typing.Any, engine: typing.Any = None) -> None:
        super().__init__(com_obj, engine)

    @property
    @ts_interface
    def imaginary_part_value(self) -> PropertyObject:
        return PropertyObject(self._com_obj.ImaginaryPartValue, self._engine_ref)

    @imaginary_part_value.setter
    @ts_interface
    def imaginary_part_value(self, val: typing.Any) -> None:
        self._com_obj.ImaginaryPartValue = val._com_obj if hasattr(val, "_com_obj") else val

    @property
    @ts_interface
    def value(self) -> PropertyObject:
        return PropertyObject(self._com_obj.Value, self._engine_ref)

    @value.setter
    @ts_interface
    def value(self, val: typing.Any) -> None:
        self._com_obj.Value = val._com_obj if hasattr(val, "_com_obj") else val


class DllArgumentList(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index: typing.Any) -> typing.Any:
        return DllArgument(self._com_obj.Item(index), self._engine_ref)


class DllFunction(COMWrapper):
    @property
    @ts_interface
    def display_name(self) -> str:
        return str(self._com_obj.DisplayName)

    @property
    @ts_interface
    def has_parameter_information(self) -> bool:
        return bool(self._com_obj.HasParameterInformation)

    @property
    @ts_interface
    def help_context(self) -> int:
        return int(self._com_obj.HelpContext)

    @property
    @ts_interface
    def help_file_path(self) -> str:
        return str(self._com_obj.HelpFilePath)

    @property
    @ts_interface
    def parameter_type_warnings(self) -> str:
        return str(self._com_obj.ParameterTypeWarnings)

    @property
    @ts_interface
    def symbol_name(self) -> str:
        return str(self._com_obj.SymbolName)

    @property
    @ts_interface
    def unique_display_name(self) -> str:
        return str(self._com_obj.UniqueDisplayName)


class DllFunctionList(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index: typing.Any) -> typing.Any:
        return DllFunction(self._com_obj.Item(index), self._engine_ref)


class DllParameter(COMWrapper):
    def __init__(self, com_obj: typing.Any, engine: typing.Any = None) -> None:
        COMWrapper.__init__(self, com_obj, engine)

    @ts_interface
    def as_common_c_parameter(self) -> typing.Any:
        from py_teststand.adapters.adapter import CommonCParameter as CommonCParam

        return CommonCParam(self._com_obj.AsCommonCParameter(), self._engine_ref)

    @property
    @ts_interface
    def category(self) -> DLLParameterCategory:
        return DLLParameterCategory(self._com_obj.Category)

    @category.setter
    @ts_interface
    def category(self, value: DLLParameterCategory | int) -> None:
        self._com_obj.Category = int(value)

    @property
    @ts_interface
    def imaginary_part_value_expr(self) -> str:
        return str(self._com_obj.ImaginaryPartValueExpr)

    @imaginary_part_value_expr.setter
    @ts_interface
    def imaginary_part_value_expr(self, value: str) -> None:
        self._com_obj.ImaginaryPartValueExpr = value

    @property
    @ts_interface
    def ts_object_parameter_type(self) -> str:
        return str(self._com_obj.TSObjectParameterType)

    @ts_object_parameter_type.setter
    @ts_interface
    def ts_object_parameter_type(self, value: str) -> None:
        self._com_obj.TSObjectParameterType = value

    @property
    @ts_interface
    def type(self) -> CommonCParameterType:
        return CommonCParameterType(self._com_obj.Type)

    @type.setter
    @ts_interface
    def type(self, value: CommonCParameterType | int) -> None:
        self._com_obj.Type = int(value)


class DllParameterList:
    def __init__(self, com_obj: typing.Any, engine: typing.Any = None) -> None:
        self._com_obj: typing.Any = com_obj
        self._engine_ref = engine

    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index: typing.Any) -> typing.Any:
        return DllParameter(self._com_obj.Item(index), self._engine_ref)

    @ts_interface
    def delete(self, index: int) -> typing.Any:
        self._com_obj.Delete(index)

    @ts_interface
    def move(self, index: int, new_index: int) -> typing.Any:
        self._com_obj.Move(index, new_index)

    @ts_interface
    def new(
        self,
        index: int,
        parameter_name: str,
        parameter_value_expr: str,
        parameter_category: DLLParameterCategory | int,
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
    def new_arguments(self) -> DllArgumentList:
        return DllArgumentList(self._com_obj.NewArguments(), self._engine_ref)
