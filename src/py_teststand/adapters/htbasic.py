from __future__ import annotations

import typing
from enum import IntEnum

from py_teststand.adapters.adapter import Adapter, Module
from py_teststand.core.com_wrapper import ts_interface


class HTBasicDefaultWorkingDir(IntEnum):
    DoNotChange = 1
    HTBasicServer = 2
    SubroutineFile = 3
    Specific = 4


class HTBasicWorkingDir(IntEnum):
    AdapterDefault = 0
    DoNotChange = 1
    HTBasicServer = 2
    SubroutineFileDir = 3
    Specify = 4


class HTBasicStepAdditions:
    HTBasicStep_FunctionNameProp = "SubName"
    HTBasicStep_ModulePathProp = "ModulePath"
    HTBasicStep_SetWorkingDirProp = "SetWorkingDirType"
    HTBasicStep_ShowAppProp = "ShowApp"
    HTBasicStep_WorkingDirPathProp = "WorkingDirPath"


class HTBasicAdapter(Adapter):
    @property
    @ts_interface
    def default_working_directory(self) -> typing.Any:
        return HTBasicDefaultWorkingDir(self._com_obj.DefaultWorkingDirectory)

    @default_working_directory.setter
    @ts_interface
    def default_working_directory(self, value: HTBasicDefaultWorkingDir | int) -> None:
        self._com_obj.DefaultWorkingDirectory = int(value)

    @property
    @ts_interface
    def development_server_path(self) -> str:
        return str(self._com_obj.DevelopmentServerPath)

    @development_server_path.setter
    @ts_interface
    def development_server_path(self, value: str) -> None:
        self._com_obj.DevelopmentServerPath = value

    @property
    @ts_interface
    def run_time_server_path(self) -> str:
        return str(self._com_obj.RunTimeServerPath)

    @run_time_server_path.setter
    @ts_interface
    def run_time_server_path(self, value: str) -> None:
        self._com_obj.RunTimeServerPath = value

    @property
    @ts_interface
    def spec_working_directory_path(self) -> str:
        return str(self._com_obj.SpecWorkingDirectoryPath)

    @spec_working_directory_path.setter
    @ts_interface
    def spec_working_directory_path(self, value: str) -> None:
        self._com_obj.SpecWorkingDirectoryPath = value

    @property
    @ts_interface
    def use_development_server(self) -> bool:
        return bool(self._com_obj.UseDevelopmentServer)

    @use_development_server.setter
    @ts_interface
    def use_development_server(self, value: bool) -> None:
        self._com_obj.UseDevelopmentServer = value

    @ts_interface
    def as_adapter(self) -> Adapter:
        return Adapter(self._com_obj.AsAdapter(), self._engine_ref)


class HTBasicModule(Module):
    @ts_interface
    def as_module(self) -> Module:
        return Module(self._com_obj.AsModule(), self._engine_ref)

    @property
    @ts_interface
    def show_htbasic_app(self) -> bool:
        return bool(self._com_obj.ShowHTBasicApp)

    @show_htbasic_app.setter
    @ts_interface
    def show_htbasic_app(self, value: bool) -> None:
        self._com_obj.ShowHTBasicApp = value

    @property
    @ts_interface
    def subroutine_file_path(self) -> str:
        return str(self._com_obj.SubroutineFilePath)

    @subroutine_file_path.setter
    @ts_interface
    def subroutine_file_path(self, value: str) -> None:
        self._com_obj.SubroutineFilePath = value

    @property
    @ts_interface
    def subroutine_name(self) -> str:
        return str(self._com_obj.SubroutineName)

    @subroutine_name.setter
    @ts_interface
    def subroutine_name(self, value: str) -> None:
        self._com_obj.SubroutineName = value

    @property
    @ts_interface
    def working_directory(self) -> typing.Any:
        return HTBasicWorkingDir(self._com_obj.WorkingDirectory)

    @working_directory.setter
    @ts_interface
    def working_directory(self, value: (HTBasicWorkingDir | int)) -> None:
        self._com_obj.WorkingDirectory = int(value)

    @property
    @ts_interface
    def working_directory_specified_path(self) -> str:
        return str(self._com_obj.WorkingDirectorySpecifiedPath)

    @working_directory_specified_path.setter
    @ts_interface
    def working_directory_specified_path(self, value: str) -> None:
        self._com_obj.WorkingDirectorySpecifiedPath = value
