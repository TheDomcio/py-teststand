from __future__ import annotations

import typing
from enum import IntEnum, IntFlag
from typing import TYPE_CHECKING

from py_teststand.adapters.adapter import Adapter, Module
from py_teststand.core.com_wrapper import COMWrapper, ts_interface


class VarType(IntFlag):
    EMPTY = 0
    NULL = 1
    I2 = 2
    I4 = 3
    R4 = 4
    R8 = 5
    CY = 6
    DATE = 7
    BSTR = 8
    DISPATCH = 9
    ERROR = 10
    BOOL = 11
    VARIANT = 12
    UNKNOWN = 13
    DECIMAL = 14
    Record = 15
    I1 = 16
    UI1 = 17
    UI2 = 18
    UI4 = 19
    I8 = 20
    UI8 = 21
    INT = 22
    UINT = 23
    ARRAY = 8192
    BYREF = 16384


if TYPE_CHECKING:
    from py_teststand.property.property_object import PropertyObject
    from py_teststand.sequence.expression import EvaluationTypes
    from py_teststand.sequence.sequence_file import SequenceFile


class UpdateAutomationIDsResult(typing.NamedTuple):
    num_steps_modified: int
    num_step_updates_failed: int
    error_description: str


class ActiveXModuleMemberType(IntFlag):
    DoNotCall = -1
    CallMethod = 1
    GetProperty = 2
    SetProperty = 4
    SetPropertyByRef = 8


class ActiveXModuleCreate(IntEnum):
    New = 0
    AttachToActive = 1
    FromFile = 2
    DoNotCreate = 3


class ActiveXParameterDirection(IntFlag):
    Unknown = 0x0
    In = 0x1
    Out = 0x2


class ActiveXInterface(COMWrapper):
    @property
    @ts_interface
    def dispatch_members(self) -> ActiveXMembers:
        return ActiveXMembers(self._com_obj.DispatchMembers, self._engine_ref)

    @property
    @ts_interface
    def documentation(self) -> str:
        return str(self._com_obj.Documentation)

    @property
    @ts_interface
    def for_typedef_only(self) -> bool:
        return bool(self._com_obj.ForTypedefOnly)

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
    def id(self) -> str:
        return str(self._com_obj.Id)

    @property
    @ts_interface
    def name(self) -> str:
        return str(self._com_obj.Name)

    @property
    @ts_interface
    def type_flags(self) -> int:
        return int(self._com_obj.TypeFlags)

    @property
    @ts_interface
    def vtable_members(self) -> ActiveXMembers:
        return ActiveXMembers(self._com_obj.VTableMembers, self._engine_ref)


class ActiveXServer(COMWrapper):
    @property
    @ts_interface
    def co_classes(self) -> ActiveXCoClasses:
        return ActiveXCoClasses(self._com_obj.CoClasses, self._engine_ref)

    @property
    @ts_interface
    def display_name(self) -> str:
        return str(self._com_obj.DisplayName)

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
    def id(self) -> str:
        return str(self._com_obj.Id)

    @property
    @ts_interface
    def interfaces(self) -> ActiveXInterfaces:
        return ActiveXInterfaces(self._com_obj.Interfaces, self._engine_ref)

    @property
    @ts_interface
    def library_flags(self) -> int:
        return int(self._com_obj.LibraryFlags)

    @ts_interface
    def load_type_library(self) -> bool:
        return bool(self._com_obj.LoadTypeLibrary())

    @property
    @ts_interface
    def locale_id(self) -> int:
        return int(self._com_obj.LocaleId)

    @property
    @ts_interface
    def major_version(self) -> int:
        return int(self._com_obj.MajorVersion)

    @property
    @ts_interface
    def minor_version(self) -> int:
        return int(self._com_obj.MinorVersion)

    @property
    @ts_interface
    def name(self) -> str:
        return str(self._com_obj.Name)

    @property
    @ts_interface
    def path(self) -> str:
        return str(self._com_obj.Path)

    @path.setter
    @ts_interface
    def path(self, value: str) -> None:
        self._com_obj.Path = value

    @property
    @ts_interface
    def version_string(self) -> str:
        return str(self._com_obj.VersionString)


class ActiveXMember(COMWrapper):
    @property
    @ts_interface
    def dispatch_id(self) -> int:
        return int(self._com_obj.DispatchId)

    @property
    @ts_interface
    def documentation(self) -> str:
        return str(self._com_obj.Documentation)

    @property
    @ts_interface
    def function_flags(self) -> int:
        return int(self._com_obj.FunctionFlags)

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
    def member_type(self) -> ActiveXModuleMemberType:
        return ActiveXModuleMemberType(self._com_obj.MemberType)

    @property
    @ts_interface
    def name(self) -> str:
        return str(self._com_obj.Name)

    @property
    @ts_interface
    def parameter_type_warnings(self) -> str:
        return str(self._com_obj.ParameterTypeWarnings)

    @property
    @ts_interface
    def vtable_offset(self) -> int:
        return int(self._com_obj.VTableOffset)


class ActiveXServers(COMWrapper):
    @ts_interface
    def __len__(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def __getitem__(self, index: typing.Any) -> ActiveXServer:
        return ActiveXServer(self._com_obj.Item(index), self._engine_ref)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def refresh(self) -> None:
        self._com_obj.Refresh()

    @property
    @ts_interface
    def refresh_count(self) -> int:
        return int(self._com_obj.RefreshCount)

    @ts_interface
    def register_type_library(self, type_library_path: str) -> tuple[str, bool]:
        result = self._com_obj.RegisterTypeLibrary(type_library_path)
        if isinstance(result, tuple):
            return str(result[0]), bool(result[1])
        return str(result), False


class ActiveXMembers(COMWrapper):
    @ts_interface
    def __len__(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def __getitem__(self, index: typing.Any) -> ActiveXMember:
        return ActiveXMember(self._com_obj.Item(index), self._engine_ref)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]


class ActiveXParameters(COMWrapper):
    @ts_interface
    def __len__(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def __getitem__(self, index: typing.Any) -> ActiveXParameter:
        return ActiveXParameter(self._com_obj.Item(index), self._engine_ref)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]


class ActiveXParameter(COMWrapper):
    @ts_interface
    def as_property_object(self) -> PropertyObject:
        from py_teststand.property.property_object import PropertyObject

        return PropertyObject(self._com_obj.AsPropertyObject(), self._engine_ref)

    @ts_interface
    def get_enum_values(self) -> list[PropertyObject]:
        from py_teststand.property.property_object import PropertyObject

        return [PropertyObject(obj, self._engine_ref) for obj in self._com_obj.GetEnumValues()]

    @property
    @ts_interface
    def default_value(self) -> str:
        return str(self._com_obj.DefaultValue)

    @property
    @ts_interface
    def direction(self) -> ActiveXParameterDirection:
        return ActiveXParameterDirection(self._com_obj.Direction)

    @property
    @ts_interface
    def display_type(self) -> str:
        return str(self._com_obj.DisplayType)

    @property
    @ts_interface
    def enum_type_name(self) -> str:
        return str(self._com_obj.EnumTypeName)

    @property
    @ts_interface
    def is_optional(self) -> bool:
        return bool(self._com_obj.IsOptional)

    @ts_interface
    def is_parameter_mapping(self) -> tuple[bool, str]:
        reason_not_valid = ""
        is_valid = bool(self._com_obj.IsParameterMapping(reason_not_valid))
        return is_valid, str(reason_not_valid)

    @property
    @ts_interface
    def parameter_name(self) -> str:
        return str(self._com_obj.ParameterName)

    @property
    @ts_interface
    def type(self) -> PropertyObject:
        from py_teststand.property.property_object import PropertyObject

        return PropertyObject(self._com_obj.Type, self._engine_ref)

    @property
    @ts_interface
    def use_default(self) -> bool:
        return bool(self._com_obj.UseDefault)

    @use_default.setter
    @ts_interface
    def use_default(self, value: bool) -> None:
        self._com_obj.UseDefault = value

    @property
    @ts_interface
    def user_data(self) -> PropertyObject:
        from py_teststand.property.property_object import PropertyObject

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

    @property
    @ts_interface
    def value_expr_is_optional(self) -> bool:
        return bool(self._com_obj.ValueExprIsOptional)


class ActiveXCoClasses(COMWrapper):
    @ts_interface
    def __len__(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def __getitem__(self, index: typing.Any) -> ActiveXCoClass:
        return ActiveXCoClass(self._com_obj.Item(index), self._engine_ref)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]


class ActiveXInterfaces(COMWrapper):
    @ts_interface
    def __len__(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def __getitem__(self, index: typing.Any) -> ActiveXInterface:
        return ActiveXInterface(self._com_obj.Item(index), self._engine_ref)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]


class ActiveXCoClass(COMWrapper):
    @property
    @ts_interface
    def documentation(self) -> str:
        return str(self._com_obj.Documentation)

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
    def id(self) -> str:
        return str(self._com_obj.Id)

    @property
    @ts_interface
    def interfaces(self) -> ActiveXInterfaces:
        return ActiveXInterfaces(self._com_obj.Interfaces, self._engine_ref)

    @property
    @ts_interface
    def name(self) -> str:
        return str(self._com_obj.Name)

    @property
    @ts_interface
    def type_flags(self) -> int:
        return int(self._com_obj.TypeFlags)

    @ts_interface
    def get_interface_implementation_type_flags(self, interface_index: int) -> int:
        return int(self._com_obj.GetInterfaceImplementationTypeFlags(interface_index))


class ActiveXModule(Module):
    @property
    @ts_interface
    def activex_reference_expr(self) -> str:
        return str(self._com_obj.ActiveXReferenceExpr)

    @activex_reference_expr.setter
    @ts_interface
    def activex_reference_expr(self, value: str) -> None:
        self._com_obj.ActiveXReferenceExpr = value

    @property
    @ts_interface
    def coclass_name(self) -> str:
        return str(self._com_obj.CoClassName)

    @coclass_name.setter
    @ts_interface
    def coclass_name(self, value: str) -> None:
        self._com_obj.CoClassName = value

    @property
    @ts_interface
    def create_option(self) -> ActiveXModuleCreate:
        return ActiveXModuleCreate(self._com_obj.CreateOption)

    @create_option.setter
    @ts_interface
    def create_option(self, value: ActiveXModuleCreate) -> None:
        self._com_obj.CreateOption = value

    @property
    @ts_interface
    def file_path(self) -> str:
        return str(self._com_obj.FilePath)

    @file_path.setter
    @ts_interface
    def file_path(self, value: str) -> None:
        self._com_obj.FilePath = value

    @property
    @ts_interface
    def interface_name(self) -> str:
        return str(self._com_obj.InterfaceName)

    @interface_name.setter
    @ts_interface
    def interface_name(self, value: str) -> None:
        self._com_obj.InterfaceName = value

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
    def member_type(self) -> ActiveXModuleMemberType:
        return ActiveXModuleMemberType(self._com_obj.MemberType)

    @member_type.setter
    @ts_interface
    def member_type(self, value: ActiveXModuleMemberType | int) -> None:
        self._com_obj.MemberType = int(value)

    @ts_interface
    def load_member_info(self, discard_parameter_values: bool = False) -> bool:
        return bool(self._com_obj.LoadMemberInfo(discard_parameter_values))

    @property
    @ts_interface
    def parameters(self) -> ActiveXParameters:
        return ActiveXParameters(self._com_obj.Parameters, self._engine_ref)

    @ts_interface
    def reload_server(self) -> bool:
        return bool(self._com_obj.ReloadServer())

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
    def server_id(self) -> str:
        return str(self._com_obj.ServerId)

    @server_id.setter
    @ts_interface
    def server_id(self, value: str) -> None:
        self._com_obj.ServerId = value

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
    def use_step_load_options(self) -> bool:
        return bool(self._com_obj.UseStepLoadOptions)

    @use_step_load_options.setter
    @ts_interface
    def use_step_load_options(self, value: bool) -> None:
        self._com_obj.UseStepLoadOptions = value

    @ts_interface
    def as_module(self) -> Module:
        return Module(self._com_obj.AsModule(), self._engine_ref)


class ActiveXAdapter(Adapter):
    @property
    @ts_interface
    def servers(self) -> ActiveXServers:
        return ActiveXServers(self._com_obj.Servers, self._engine_ref)

    @property
    @ts_interface
    def show_activex_controls_when_specifying_module(self) -> bool:
        return bool(self._com_obj.ShowActiveXControlsWhenSpecifyingModule)

    @show_activex_controls_when_specifying_module.setter
    @ts_interface
    def show_activex_controls_when_specifying_module(self, value: bool) -> None:
        self._com_obj.ShowActiveXControlsWhenSpecifyingModule = value

    @property
    @ts_interface
    def unload_unused_activex_servers_after_exec(self) -> bool:
        return bool(self._com_obj.UnloadUnusedActiveXServersAfterExec)

    @unload_unused_activex_servers_after_exec.setter
    @ts_interface
    def unload_unused_activex_servers_after_exec(self, value: bool) -> None:
        self._com_obj.UnloadUnusedActiveXServersAfterExec = value

    @property
    @ts_interface
    def use_late_binding(self) -> bool:
        return bool(self._com_obj.UseLateBinding)

    @use_late_binding.setter
    @ts_interface
    def use_late_binding(self, value: bool) -> None:
        self._com_obj.UseLateBinding = value

    @ts_interface
    def as_adapter(self) -> Adapter:
        return Adapter(self._com_obj.AsAdapter(), self._engine_ref)

    @ts_interface
    def update_automation_ids(self, seq_file_to_update: SequenceFile) -> UpdateAutomationIDsResult:
        result = self._com_obj.UpdateAutomationIDs(seq_file_to_update._com_obj)
        return UpdateAutomationIDsResult(
            num_steps_modified=int(result[0]),
            num_step_updates_failed=int(result[1]),
            error_description=str(result[2]),
        )
