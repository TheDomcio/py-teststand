from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COMWrapper, ts_interface

if TYPE_CHECKING:
    from py_teststand.property.property_object import PropertyObject


class UserPrivilege(str, Enum):
    def __str__(self) -> str:
        return str(self.value)

    Abort = "Abort"
    ConfigAdapter = "ConfigAdapter"
    ConfigApp = "ConfigApp"
    ConfigDatabase = "ConfigDatabase"
    ConfigEngine = "ConfigEngine"
    ConfigModel = "ConfigModel"
    ConfigReport = "ConfigReport"
    Configure = "Configure"
    CtrlExecFlow = "ControlExecFlow"
    Debug = "Debug"
    Develop = "Develop"
    EditProcessModelFiles = "EditProcessModelFiles"
    EditRuntimeVariables = "EditRuntimeVariables"
    EditSequenceFiles = "EditSequenceFiles"
    EditStationGlobals = "EditStationGlobals"
    EditTemplates = "EditTemplates"
    EditTypes = "EditTypes"
    EditUsers = "EditUsers"
    EditWorkspace = "EditWorkspace"
    Execute = "Execute"
    GrantAll = "GrantAll"
    LoopSelectedTests = "LoopSelectedTests"
    Operate = "Operate"
    RunAnySequence = "RunAnySequence"
    RunSelectedTests = "RunSelectedTests"
    SaveSequenceFiles = "SaveSequenceFiles"
    SinglePass = "SinglePass"
    Terminate = "Terminate"
    UserLoggedIn = "*"
    UseSourceControl = "UseSourceControl"


class User(COMWrapper):
    @ts_interface
    def as_property_object(self) -> PropertyObject:
        from py_teststand.property.property_object import PropertyObject

        return PropertyObject(self._com_obj.AsPropertyObject(), self._engine_ref)

    @property
    @ts_interface
    def full_name(self) -> str:
        return str(self._com_obj.FullName)

    @full_name.setter
    @ts_interface
    def full_name(self, value: str) -> None:
        self._com_obj.FullName = value

    @property
    @ts_interface
    def login_name(self) -> str:
        return str(self._com_obj.LoginName)

    @login_name.setter
    @ts_interface
    def login_name(self, value: str) -> None:
        self._com_obj.LoginName = value

    @property
    @ts_interface
    def members(self) -> PropertyObject:
        from py_teststand.property.property_object import PropertyObject

        return PropertyObject(self._com_obj.Members, self._engine_ref)

    @property
    @ts_interface
    def password(self) -> str:
        return str(self._com_obj.Password)

    @password.setter
    @ts_interface
    def password(self, value: str) -> None:
        self._com_obj.Password = value

    @property
    @ts_interface
    def privileges(self) -> PropertyObject:
        from py_teststand.property.property_object import PropertyObject

        return PropertyObject(self._com_obj.Privileges, self._engine_ref)

    @ts_interface
    def has_privilege(self, privilege_name: str) -> bool:
        return bool(self._com_obj.HasPrivilege(privilege_name))

    @ts_interface
    def validate_password(self, password: str) -> bool:
        return bool(self._com_obj.ValidatePassword(password))


UserGroup = User
