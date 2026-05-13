from __future__ import annotations

import logging
import re
import typing
from enum import Enum, IntEnum, IntFlag
from typing import TYPE_CHECKING

from py_teststand.adapters.adapter import Adapter, Module, UnmappedArgumentValueList
from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.property.property_object import PropertyObject

if TYPE_CHECKING:
    from py_teststand.adapters import DotNetModule
    from py_teststand.sequence.expression import EvaluationTypes


logger = logging.getLogger(__name__)


class DotNetRuntimeKind(str, Enum):
    Framework = "framework"
    Core = "core"
    Unknown = "unknown"


_CLR_VERSION_RE = re.compile(r"v?(\d+)\.(\d+)")


def parse_dotnet_runtime_kind(clr_version: str) -> DotNetRuntimeKind:
    if not clr_version:
        return DotNetRuntimeKind.Unknown
    match = _CLR_VERSION_RE.search(clr_version)
    if not match:
        return DotNetRuntimeKind.Unknown
    major = int(match.group(1))
    if major <= 4:
        return DotNetRuntimeKind.Framework
    return DotNetRuntimeKind.Core


class DotNetModuleMemberFlag(IntFlag):
    Static = 0x1
    TopLevel = 0x2


class DotNetModuleAssemblyLocation(IntEnum):
    File = 0
    GAC = 1


class DotNetParameterType(IntEnum):
    Boolean = 2
    Byte = 3
    Char = 14
    Class = 0
    Decimal = 13
    Double = 12
    Enum = 16
    Int16 = 5
    Int32 = 6
    Int64 = 7
    IntPtr = 15
    Object = 17
    SByte = 4
    Single = 11
    String = 1
    Struct = 18
    UInt16 = 8
    UInt32 = 9
    UInt64 = 10
    UIntPtr = 20
    Void = 19


class DotNetParameterFlag(IntFlag):
    IsArray = 0x100
    Lcid = 0x4
    Optional = 0x10


class DotNetParameterDirection(IntFlag):
    In = 0x1
    Out = 0x2
    Return = 0x4


class DotNetModuleMemberType(IntEnum):
    DoNotCall = 0
    CallMethod = 1
    GetProperty = 2
    SetProperty = 3
    CallConstructor = 4
    CreateRemote = 5
    UseExisting = 6


class DotNetAdapterGetMemberNamesOption(IntFlag):
    InstanceMembers = 0x1
    AllowLoadingMixedAssemblies = 0x2


class DotNetAdapter(Adapter):
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

    @property
    def runtime_kind(self) -> DotNetRuntimeKind:
        ref = self._engine_ref
        engine: typing.Any = ref() if ref is not None else None
        if engine is None:
            return DotNetRuntimeKind.Unknown
        try:
            return parse_dotnet_runtime_kind(str(getattr(engine, "dot_net_clr_version", "")))
        except Exception:
            return DotNetRuntimeKind.Unknown

    @property
    def gac_supported(self) -> bool:
        return self.runtime_kind == DotNetRuntimeKind.Framework

    def _warn_if_gac_unsupported(self, assembly_location: int) -> None:
        if assembly_location != DotNetModuleAssemblyLocation.GAC:
            return
        kind = self.runtime_kind
        if kind == DotNetRuntimeKind.Framework or kind == DotNetRuntimeKind.Unknown:
            return
        logger.warning(
            "GAC assembly location not supported under .NET Core (CLR=%s); use File instead.",
            kind.value,
        )

    @ts_interface
    def cache_assembly_info(self, assembly_location: int, assembly_path: str) -> typing.Any:
        self._warn_if_gac_unsupported(assembly_location)
        self._com_obj.CacheAssemblyInfo(assembly_location, assembly_path)

    @ts_interface
    def cache_assembly_info_ex(
        self, assembly_location: int, assembly_path: str, options: int
    ) -> None:
        self._warn_if_gac_unsupported(assembly_location)
        self._com_obj.CacheAssemblyInfoEx(assembly_location, assembly_path, options)

    @ts_interface
    def get_class_names(
        self, assembly_location: int, assembly_path: str, options: int
    ) -> list[str]:
        self._warn_if_gac_unsupported(assembly_location)
        res = self._com_obj.GetClassNames(assembly_location, assembly_path, options)
        return list(res[0]) if isinstance(res, (list, tuple)) else []

    @ts_interface
    def get_member_names(
        self, assembly_location: int, assembly_path: str, class_name: str, options: int
    ) -> list[str]:
        self._warn_if_gac_unsupported(assembly_location)
        res = self._com_obj.GetMemberNames(assembly_location, assembly_path, class_name, options)
        return list(res[0]) if isinstance(res, (list, tuple)) else []

    @ts_interface
    def get_exclude_from_structure(
        self, type_definition: PropertyObject, property_lookup_string: str
    ) -> bool:
        return bool(
            self._com_obj.GetExcludeFromStructure(type_definition._com_obj, property_lookup_string)
        )

    @ts_interface
    def set_exclude_from_structure(
        self, type_definition: PropertyObject, property_lookup_string: str, exclude: bool
    ) -> None:
        self._com_obj.SetExcludeFromStructure(
            type_definition._com_obj, property_lookup_string, exclude
        )

    @ts_interface
    def get_gac_assembly_strong_names(self) -> list[str]:
        if self.runtime_kind == DotNetRuntimeKind.Core:
            return []
        return list(self._com_obj.GetGACAssemblyStrongNames())

    @ts_interface
    def get_structure_member_label(
        self, type_definition: PropertyObject, property_lookup_string: str
    ) -> str:
        return str(
            self._com_obj.GetStructureMemberLabel(type_definition._com_obj, property_lookup_string)
        )

    @ts_interface
    def set_structure_member_label(
        self, type_definition: PropertyObject, property_lookup_string: str, label: str
    ) -> None:
        self._com_obj.SetStructureMemberLabel(
            type_definition._com_obj, property_lookup_string, label
        )

    @ts_interface
    def get_structure_passing_enabled(self, type_definition: PropertyObject) -> typing.Any:
        return bool(self._com_obj.GetStructurePassingEnabled(type_definition._com_obj))

    @ts_interface
    def set_structure_passing_enabled(
        self, type_definition: PropertyObject, enabled: bool
    ) -> typing.Any:
        self._com_obj.SetStructurePassingEnabled(type_definition._com_obj, enabled)

    @ts_interface
    def is_class_valid(
        self, assembly_location: int, assembly_path: str, class_name: str
    ) -> typing.Any:
        return bool(self._com_obj.IsClassValid(assembly_location, assembly_path, class_name))

    @ts_interface
    def is_class_valid_ex(
        self, assembly_location: int, assembly_path: str, class_name: str, options: int
    ) -> bool:
        return bool(
            self._com_obj.IsClassValidEx(assembly_location, assembly_path, class_name, options)
        )

    @ts_interface
    def new_module(self) -> DotNetModule:
        from py_teststand.adapters import DotNetModule

        return DotNetModule(self._com_obj.NewModule(), self._engine_ref)


class DotNetModule(Module):
    @property
    @ts_interface
    def allow_unload(self) -> typing.Any:
        return bool(self._com_obj.AllowUnload)

    @allow_unload.setter
    @ts_interface
    def allow_unload(self, value: bool) -> None:
        self._com_obj.AllowUnload = value

    @property
    @ts_interface
    def parameters(self) -> PropertyObject:
        return PropertyObject(self._com_obj.Parameters, self._engine_ref)

    def get_parameters(self) -> typing.Iterator[PropertyObject | None]:
        params_po = self.parameters
        count = params_po.get_num_elements()
        for i in range(count):
            (yield params_po.get_property_object_by_offset(i))

    @property
    @ts_interface
    def assembly_warnings(self) -> str:
        return str(self._com_obj.AssemblyWarnings)

    @property
    @ts_interface
    def calls(self) -> DotNetCalls:
        return DotNetCalls(self._com_obj.Calls, self._engine_ref)

    @property
    @ts_interface
    def class_help_string(self) -> str:
        return str(self._com_obj.ClassHelpString)

    @property
    @ts_interface
    def class_name(self) -> str:
        return str(self._com_obj.ClassName)

    @class_name.setter
    @ts_interface
    def class_name(self, value: str) -> None:
        self._com_obj.ClassName = value

    @ts_interface
    def clear_unmapped_constructor_argument_values(self) -> None:
        self._com_obj.ClearUnmappedConstructorArgumentValues()

    @property
    @ts_interface
    def constructor_index(self) -> int:
        return int(self._com_obj.ConstructorIndex)

    @constructor_index.setter
    @ts_interface
    def constructor_index(self, value: int) -> None:
        self._com_obj.ConstructorIndex = value

    @property
    @ts_interface
    def constructor_parameters(self) -> DotNetParameters:
        return DotNetParameters(self._com_obj.ConstructorParameters, self._engine_ref)

    @property
    @ts_interface
    def constructor_prototype(self) -> str:
        return str(self._com_obj.ConstructorPrototype)

    @property
    @ts_interface
    def create_object(self) -> bool:
        return bool(self._com_obj.CreateObject)

    @create_object.setter
    @ts_interface
    def create_object(self, value: bool) -> None:
        self._com_obj.CreateObject = value

    @ts_interface
    def display_create_custom_data_type_dialog(self, sequence_context: typing.Any) -> typing.Any:
        raw_ctx = getattr(sequence_context, "_com_obj", None) if sequence_context else None
        return bool(self._com_obj.DisplayCreateCustomDataTypeDialog(raw_ctx))

    @property
    @ts_interface
    def dispose_object(self) -> bool:
        return bool(self._com_obj.DisposeObject)

    @dispose_object.setter
    @ts_interface
    def dispose_object(self, value: bool) -> None:
        self._com_obj.DisposeObject = value

    @ts_interface
    def execute(
        self, sequence_context: typing.Any = None, arguments: typing.Any = None
    ) -> typing.Any:
        raw_ctx = getattr(sequence_context, "_com_obj", None) if sequence_context else None
        raw_args = getattr(arguments, "_com_obj", None) if arguments else None
        self._com_obj.Execute(raw_ctx, raw_args)

    @ts_interface
    def get_assembly(self) -> typing.Any:
        return self._com_obj.GetAssembly()

    @ts_interface
    def get_constructor_metadata_token(self) -> int:
        return int(self._com_obj.GetConstructorMetadataToken())

    @ts_interface
    def get_metadata_token(self) -> int:
        return int(self._com_obj.GetMetadataToken())

    @property
    @ts_interface
    def is_constructor_prototype_incompatible(self) -> bool:
        return bool(self._com_obj.IsConstructorPrototypeIncompatible)

    @property
    @ts_interface
    def is_struct(self) -> bool:
        return bool(self._com_obj.IsStruct)

    @ts_interface
    def load_constructor_info(self, discard_parameter_values: bool = False) -> typing.Any:
        return bool(self._com_obj.LoadConstructorInfo(discard_parameter_values))

    @ts_interface
    def load_constructor_prototype_from_metadata_token(
        self, metadata_token: int, options: int = 0
    ) -> bool:
        return bool(
            self._com_obj.LoadConstructorPrototypeFromMetadataToken(metadata_token, options)
        )

    @ts_interface
    def load_member_info(self, discard_parameter_values: bool = False) -> typing.Any:
        return bool(self._com_obj.LoadMemberInfo(discard_parameter_values))

    @ts_interface
    def load_prototype_from_metadata_token(
        self, metadata_token: int, options: int = 0
    ) -> typing.Any:
        return bool(self._com_obj.LoadPrototypeFromMetadataToken(metadata_token, options))

    @property
    @ts_interface
    def member_flags(self) -> DotNetModuleMemberFlag:
        return DotNetModuleMemberFlag(self._com_obj.MemberFlags)

    @member_flags.setter
    @ts_interface
    def member_flags(self, value: DotNetModuleMemberFlag | int) -> None:
        self._com_obj.MemberFlags = int(value)

    @property
    @ts_interface
    def member_help_string(self) -> str:
        return str(self._com_obj.MemberHelpString)

    @property
    @ts_interface
    def member_index(self) -> int:
        return int(self._com_obj.MemberIndex)

    @member_index.setter
    @ts_interface
    def member_index(self, value: int) -> None:
        self._com_obj.MemberIndex = value

    @property
    @ts_interface
    def member_name(self) -> str:
        return str(self._com_obj.MemberName)

    @member_name.setter
    @ts_interface
    def member_name(self, value: str) -> None:
        self._com_obj.MemberName = value

    @property
    @ts_interface
    def member_type(self) -> DotNetModuleMemberType:
        return DotNetModuleMemberType(self._com_obj.MemberType)

    @member_type.setter
    @ts_interface
    def member_type(self, value: DotNetModuleMemberType | int) -> None:
        self._com_obj.MemberType = int(value)

    @property
    @ts_interface
    def name_of_method_to_create(self) -> str:
        return str(self._com_obj.NameOfMethodToCreate)

    @name_of_method_to_create.setter
    @ts_interface
    def name_of_method_to_create(self, value: str) -> None:
        self._com_obj.NameOfMethodToCreate = value

    @ts_interface
    def new_module_arguments(self) -> DotNetModuleArguments:
        return DotNetModuleArguments(self._com_obj.NewModuleArguments(), self._engine_ref)

    @property
    @ts_interface
    def remote_host(self) -> typing.Any:
        return str(self._com_obj.RemoteHost)

    @remote_host.setter
    @ts_interface
    def remote_host(self, value: str) -> None:
        self._com_obj.RemoteHost = value

    @ts_interface
    def set_assembly(self, location: int, path: str) -> typing.Any:
        self._com_obj.SetAssembly(location, path)

    @property
    @ts_interface
    def solution_file_path(self) -> str:
        return str(self._com_obj.SolutionFilePath)

    @solution_file_path.setter
    @ts_interface
    def solution_file_path(self, value: str) -> None:
        self._com_obj.SolutionFilePath = value

    @property
    @ts_interface
    def specify_host_by_expression(self) -> bool:
        return bool(self._com_obj.SpecifyHostByExpression)

    @specify_host_by_expression.setter
    @ts_interface
    def specify_host_by_expression(self, value: bool) -> None:
        self._com_obj.SpecifyHostByExpression = value

    @property
    @ts_interface
    def unmapped_constructor_argument_values(self) -> UnmappedArgumentValueList:
        return UnmappedArgumentValueList(
            self._com_obj.UnmappedConstructorArgumentValues, self._engine_ref
        )

    @property
    @ts_interface
    def use_step_load_options(self) -> bool:
        return bool(self._com_obj.UseStepLoadOptions)

    @use_step_load_options.setter
    @ts_interface
    def use_step_load_options(self, value: bool) -> None:
        self._com_obj.UseStepLoadOptions = value

    @property
    @ts_interface
    def class_reference(self) -> str:
        return str(self._com_obj.ClassReference)

    @class_reference.setter
    @ts_interface
    def class_reference(self, value: str) -> None:
        self._com_obj.ClassReference = value

    @property
    @ts_interface
    def source_file_path(self) -> str:
        return str(self._com_obj.SourceFilePath)

    @property
    @ts_interface
    def project_file_path(self) -> str:
        return str(self._com_obj.ProjectFilePath)

    @property
    @ts_interface
    def member_name(self) -> str:
        try:
            return str(self._com_obj.MemberName)
        except AttributeError:
            return str(self._com_obj.FunctionName)

    @member_name.setter
    @ts_interface
    def member_name(self, value: str) -> None:
        try:
            self._com_obj.MemberName = value
        except AttributeError:
            self._com_obj.FunctionName = value

    @property
    @ts_interface
    def assembly_location(self) -> DotNetModuleAssemblyLocation:
        res = self._com_obj.GetAssembly()
        return DotNetModuleAssemblyLocation(int(res[0]))

    @assembly_location.setter
    @ts_interface
    def assembly_location(self, value: (DotNetModuleAssemblyLocation | int)) -> None:
        name = self.assembly_name
        self._com_obj.SetAssembly(int(value), name)

    @property
    @ts_interface
    def assembly_name(self) -> str:
        res = self._com_obj.GetAssembly()
        return str(res[1])

    @assembly_name.setter
    @ts_interface
    def assembly_name(self, value: str) -> None:
        loc = self.assembly_location
        try:
            self._com_obj.SetAssembly(loc, value)
        except Exception:
            try:
                if loc == DotNetModuleAssemblyLocation.GAC:
                    self._com_obj.AssemblyStrongName = value
                else:
                    self._com_obj.AssemblyPath = value
            except Exception:
                try:
                    self._com_obj.SetAssembly(loc, value, 0)
                except Exception:
                    raise

    @property
    @ts_interface
    def member_type(self) -> DotNetModuleMemberType:
        return DotNetModuleMemberType(int(self._com_obj.MemberType))

    @property
    @ts_interface
    def remote_host(self) -> str:
        return str(self._com_obj.RemoteHost)

    @remote_host.setter
    @ts_interface
    def remote_host(self, value: str) -> None:
        self._com_obj.RemoteHost = value

    @property
    @ts_interface
    def specify_host_by_expression(self) -> bool:
        return bool(self._com_obj.SpecifyHostByExpression)

    @ts_interface
    def create_object(self) -> typing.Any:
        return self._com_obj.CreateObject()

    @ts_interface
    def dispose_object(self) -> None:
        self._com_obj.DisposeObject()

    @ts_interface
    def as_module(self) -> Module:
        return Module(self._com_obj.AsModule(), self._engine_ref)

    @ts_interface
    def clear_unmapped_argument_values(self) -> None:
        return self._com_obj.ClearUnmappedArgumentValues()

    @ts_interface
    def create_code(self) -> bool:
        return bool(self._com_obj.CreateCode())

    @ts_interface
    def get_description(self, options: int = 0) -> str:
        return str(self._com_obj.GetDescription(options))

    @ts_interface
    def get_last_load_warnings(self) -> list[str]:
        result = self._com_obj.GetLastLoadWarnings()
        if isinstance(result, str):
            return [result] if result else []
        return list(result)

    @ts_interface
    def specify(self, options: int = 0) -> bool:
        return bool(self._com_obj.Specify(options))


class DotNetArgument(COMWrapper):
    @property
    @ts_interface
    def elements(self) -> DotNetArguments:
        return DotNetArguments(self._com_obj.Elements, self._engine_ref)

    @property
    @ts_interface
    def parameter_name(self) -> str:
        return str(self._com_obj.ParameterName)

    @property
    @ts_interface
    def value(self) -> PropertyObject:
        from py_teststand.property.property_object import PropertyObject

        return PropertyObject(self._com_obj.Value, self._engine_ref)

    @value.setter
    @ts_interface
    def value(self, val: typing.Any) -> None:
        self._com_obj.Value = val._com_obj if hasattr(val, "_com_obj") else val


class DotNetArguments(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index: typing.Any) -> typing.Any:
        return DotNetArgument(self._com_obj.Item(index), self._engine_ref)


class DotNetCall(COMWrapper):
    @property
    @ts_interface
    def call_index(self) -> int:
        return int(self._com_obj.CallIndex)

    @property
    @ts_interface
    def class_help_string(self) -> str:
        return str(self._com_obj.ClassHelpString)

    @property
    @ts_interface
    def class_name(self) -> str:
        return str(self._com_obj.ClassName)

    @property
    @ts_interface
    def class_name_for_next_call(self) -> str:
        return str(self._com_obj.ClassNameForNextCall)

    @ts_interface
    def create_code(self) -> bool:
        return bool(self._com_obj.CreateCode())

    @ts_interface
    def edit_code(self) -> bool:
        return bool(self._com_obj.EditCode())

    @ts_interface
    def get_assembly(self) -> typing.Any:
        return self._com_obj.GetAssembly()

    @ts_interface
    def get_assembly_for_next_call(self) -> typing.Any:
        return self._com_obj.GetAssemblyForNextCall()

    @ts_interface
    def is_call_valid(self) -> typing.Any:
        return self._com_obj.IsCallValid()

    @property
    @ts_interface
    def is_prototype_incompatible(self) -> bool:
        return bool(self._com_obj.IsPrototypeIncompatible)

    @ts_interface
    def load_prototype_from_signature(
        self, signature: str, allow_member_name_matching: bool, options: int = 0
    ) -> bool:
        return bool(
            self._com_obj.LoadPrototypeFromSignature(signature, allow_member_name_matching, options)
        )

    @property
    @ts_interface
    def member_flags(self) -> DotNetModuleMemberFlag:
        return DotNetModuleMemberFlag(int(self._com_obj.MemberFlags))

    @property
    @ts_interface
    def member_help_string(self) -> str:
        return str(self._com_obj.MemberHelpString)

    @property
    @ts_interface
    def member_name(self) -> str:
        return str(self._com_obj.MemberName)

    @property
    @ts_interface
    def member_type(self) -> DotNetModuleMemberType:
        return DotNetModuleMemberType(int(self._com_obj.MemberType))

    @ts_interface
    def reload_prototype(self, options: int = 0) -> typing.Any:
        return bool(self._com_obj.ReloadPrototype(options))

    @ts_interface
    def set_incomplete_signature(self, partial_signature: str) -> typing.Any:
        self._com_obj.SetIncompleteSignature(partial_signature)

    @property
    @ts_interface
    def signature(self) -> str:
        return str(self._com_obj.Signature)

    @property
    @ts_interface
    def parameters(self) -> DotNetParameters:
        return DotNetParameters(self._com_obj.Parameters, self._engine_ref)

    @property
    @ts_interface
    def unmapped_argument_values(self) -> UnmappedArgumentValueList:
        return UnmappedArgumentValueList(self._com_obj.UnmappedArgumentValues, self._engine_ref)


class DotNetCalls(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index: typing.Any) -> typing.Any:
        return DotNetCall(self._com_obj.Item(index), self._engine_ref)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def delete(self, index: int) -> typing.Any:
        self._com_obj.Delete(index)

    @ts_interface
    def delete_all_after_index(self, index: int) -> typing.Any:
        self._com_obj.DeleteAllAfterIndex(index)

    @ts_interface
    def new(self, index: int) -> typing.Any:
        return DotNetCall(self._com_obj.New(index), self._engine_ref)

    def release(self) -> None:
        "Releases the underlying COM object."
        self._com_obj = None

    def __del__(self) -> None:
        try:
            self.release()
        except Exception:
            pass


class DotNetModuleArguments(PropertyObject):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index: typing.Any) -> typing.Any:
        return DotNetArguments(self._com_obj.Item(index), self._engine_ref)

    def __len__(self) -> int:
        return self.count

    def __getitem__(self, index: typing.Any) -> DotNetArguments:
        return self.item(index)

    def __iter__(self) -> typing.Iterator[DotNetArguments]:
        for i in range(self.count):
            (yield self.item(i))


class DotNetParameters(PropertyObject):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index: typing.Any) -> typing.Any:
        return DotNetParameter(self._com_obj.Item(index), self._engine_ref)

    def __len__(self) -> int:
        return self.count

    def __getitem__(self, index: typing.Any) -> DotNetParameter:
        return self.item(index)

    def __iter__(self) -> typing.Iterator[DotNetParameter]:
        for i in range(self.count):
            (yield self.item(i))


class DotNetParameter(PropertyObject):
    @property
    @ts_interface
    def array_dimensions(self) -> int:
        return int(self._com_obj.ArrayDimensions)

    @property
    @ts_interface
    def array_dimensions_ex(self) -> str:
        return str(self._com_obj.ArrayDimensionsEx)

    @property
    @ts_interface
    def category(self) -> int:
        return int(self._com_obj.Category)

    @property
    @ts_interface
    def default_value(self) -> str:
        return str(self._com_obj.DefaultValue)

    @ts_interface
    def delete_array_element(self, index: int) -> typing.Any:
        self._com_obj.DeleteArrayElement(index)

    @property
    @ts_interface
    def direction(self) -> DotNetParameterDirection:
        return DotNetParameterDirection(self._com_obj.Direction)

    @property
    @ts_interface
    def elements(self) -> DotNetParameters:
        return DotNetParameters(self._com_obj.Elements, self._engine_ref)

    @ts_interface
    def display_create_custom_data_type_dialog(self, sequence_context: typing.Any) -> typing.Any:
        return bool(self._com_obj.DisplayCreateCustomDataTypeDialog(sequence_context._com_obj))

    @property
    @ts_interface
    def display_type(self) -> str:
        return str(self._com_obj.DisplayType)

    @property
    @ts_interface
    def dispose_object(self) -> bool:
        return bool(self._com_obj.DisposeObject)

    @dispose_object.setter
    @ts_interface
    def dispose_object(self, value: bool) -> None:
        self._com_obj.DisposeObject = value

    @property
    @ts_interface
    def flags(self) -> DotNetParameterFlag:
        return DotNetParameterFlag(self._com_obj.Flags)

    @property
    @ts_interface
    def help_string(self) -> str:
        return str(self._com_obj.HelpString)

    @ts_interface
    def get_enum_values(self) -> list[PropertyObject]:
        res = self._com_obj.GetEnumValues()
        return [PropertyObject(obj, self._engine_ref) for obj in res]

    @ts_interface
    def insert_array_element(self, index: int) -> typing.Any:
        self._com_obj.InsertArrayElement(index)

    @ts_interface
    def is_parameter_mapping_invalid(self) -> typing.Any:
        res = self._com_obj.IsParameterMappingInvalid("")
        return (bool(res[0]), str(res[1]))

    @ts_interface
    def is_struct_mapping_invalid(self) -> typing.Any:
        res = self._com_obj.IsStructMappingInvalid("")
        return (bool(res[0]), str(res[1]))

    @property
    @ts_interface
    def name(self) -> str:
        return str(self._com_obj.Name)

    @property
    @ts_interface
    def parameter_name(self) -> str:
        return str(self._com_obj.ParameterName)

    @property
    @ts_interface
    def use_default_value(self) -> bool:
        return bool(self._com_obj.UseDefaultValue)

    @use_default_value.setter
    @ts_interface
    def use_default_value(self, value: bool) -> None:
        self._com_obj.UseDefaultValue = value

    @property
    @ts_interface
    def type(self) -> DotNetParameterType:
        return DotNetParameterType(self._com_obj.Type)

    @property
    @ts_interface
    def type_name(self) -> str:
        return str(self._com_obj.TypeName)

    @property
    @ts_interface
    def valid_evaluation_types(self) -> EvaluationTypes:
        from py_teststand.sequence.expression import EvaluationTypes

        return EvaluationTypes(self._com_obj.ValidEvaluationTypes, self._engine_ref)

    @property
    @ts_interface
    def value_expr_is_ignored(self) -> bool:
        return bool(self._com_obj.ValueExprIsIgnored)

    @property
    @ts_interface
    def value_expr_is_optional(self) -> bool:
        return bool(self._com_obj.ValueExprIsOptional)

    @property
    @ts_interface
    def value_expr(self) -> str:
        return str(self._com_obj.ValueExpr)

    @value_expr.setter
    @ts_interface
    def value_expr(self, value: str) -> None:
        self._com_obj.ValueExpr = value
