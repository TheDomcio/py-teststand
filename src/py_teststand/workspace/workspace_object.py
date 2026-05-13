from __future__ import annotations

import typing
from enum import IntEnum, IntFlag
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COMWrapper, ts_interface


class WorkspaceObjectType(IntEnum):
    WorkspaceFile = 1
    ProjectFile = 2
    Folder = 3
    SequenceFile = 4
    OtherFile = 5


class SourceControlCommand(IntEnum):
    AddToSC = 1
    RemoveFromSC = 2
    CheckOut = 3
    CheckIn = 4
    GetLatest = 5
    UndoCheckOut = 6
    ShowDifferences = 7
    ShowHistory = 8
    ShowProperties = 9
    ShowProviderOptions = 10


class SourceControlCommandOption(IntFlag):
    NoneValue = 0
    DoNotRecurse = 1
    SkipPromptDialog = 2
    ShowPromptDialog = 4
    SkipErrorDialog = 8


class SourceControlStatus(IntFlag):
    NotInSC = 0
    InSC = 1
    CheckedOut = 2
    CheckedOutOther = 4
    CheckedOutMultiple = 16
    OutOfDate = 32
    Deleted = 64
    CheckedOutByUser = 4096


if TYPE_CHECKING:
    from py_teststand.core.engine import Engine
    from py_teststand.property.property_object import PropertyObject
    from py_teststand.property.property_object_file import PropertyObjectFile


class WorkspaceObject(COMWrapper):
    def __init__(self, com_obj: typing.Any, engine: Engine | None = None) -> None:
        super().__init__(com_obj, engine)

    @property
    @ts_interface
    def display_name(self) -> str:
        return str(self._com_obj.DisplayName)

    @display_name.setter
    @ts_interface
    def display_name(self, value: str) -> None:
        self._com_obj.DisplayName = str(value)

    @property
    @ts_interface
    def path(self) -> str:
        return str(self._com_obj.Path)

    @path.setter
    @ts_interface
    def path(self, value: str) -> None:
        self._com_obj.Path = str(value)

    @property
    @ts_interface
    def file_exists(self) -> bool:
        return bool(self._com_obj.FileExists)

    @property
    @ts_interface
    def object_type(self) -> WorkspaceObjectType:
        return WorkspaceObjectType(self._com_obj.ObjectType)

    @property
    @ts_interface
    def num_contained_objects(self) -> int:
        return int(self._com_obj.NumContainedObjects)

    @property
    @ts_interface
    def source_control_status(self) -> SourceControlStatus:
        return SourceControlStatus(self._com_obj.SourceControlStatus)

    @ts_interface
    def get_contained_object(self, index: int) -> WorkspaceObject:
        return WorkspaceObject(self._com_obj.GetContainedObject(int(index)), self.engine)

    @ts_interface
    def get_parent_container(self) -> WorkspaceObject | None:
        com_parent = self._com_obj.GetParentContainer()
        return WorkspaceObject(com_parent, self.engine) if com_parent else None

    @ts_interface
    def get_absolute_path(self) -> str:
        return str(self._com_obj.GetAbsolutePath())

    @ts_interface
    def update_status(self, options: int | SourceControlCommandOption = 0) -> None:
        self._com_obj.UpdateStatus(int(options))

    @ts_interface
    def as_property_object(self) -> PropertyObject:
        from py_teststand.property.property_object import PropertyObject

        return PropertyObject(self._com_obj.AsPropertyObject(), self.engine)

    @property
    @ts_interface
    def code_module_seq_file_path(self) -> str:
        return str(self._com_obj.CodeModuleSeqFilePath)

    @property
    @ts_interface
    def is_code_module(self) -> bool:
        return bool(self._com_obj.IsCodeModule)

    @property
    @ts_interface
    def last_source_control_messages(self) -> str:
        return str(self._com_obj.LastSourceControlMessages)

    @property
    @ts_interface
    def project_file(self) -> PropertyObjectFile | None:
        from py_teststand.property.property_object_file import PropertyObjectFile

        com_file = self._com_obj.ProjectFile
        return PropertyObjectFile(com_file, self.engine) if com_file else None

    @ts_interface
    def can_do_source_control_command(
        self,
        sc_command: int | SourceControlCommand,
        options: int | SourceControlCommandOption = 0,
        item_list: typing.Any | None = None,
    ) -> bool:
        return bool(
            self._com_obj.CanDoSourceControlCommand(int(sc_command), int(options), item_list)
        )

    @ts_interface
    def do_source_control_command(
        self,
        sc_command: int | SourceControlCommand,
        options: int | SourceControlCommandOption = 0,
        item_list: typing.Any | None = None,
    ) -> tuple[bool, bool]:
        res = self._com_obj.DoSourceControlCommand(int(sc_command), None, int(options), item_list)
        if isinstance(res, tuple):
            return bool(res[0]), bool(res[1])
        return bool(res), False

    @ts_interface
    def insert_code_modules(self, item_list: typing.Any | None = None) -> list[WorkspaceObject]:
        res = self._com_obj.InsertCodeModules(item_list)
        if not res:
            return []
        return [WorkspaceObject(item, self.engine) for item in res]

    @ts_interface
    def insert_object(self, object_to_insert: WorkspaceObject, index: int) -> None:
        self._com_obj.InsertObject(object_to_insert._com_obj, int(index))

    @ts_interface
    def new_file(self, path_string: str = "") -> WorkspaceObject:
        return WorkspaceObject(self._com_obj.NewFile(str(path_string)), self.engine)

    @ts_interface
    def new_folder(self, folder_name: str = "") -> WorkspaceObject:
        return WorkspaceObject(self._com_obj.NewFolder(str(folder_name)), self.engine)

    @ts_interface
    def remove_object(self, index: int) -> WorkspaceObject:
        return WorkspaceObject(self._com_obj.RemoveObject(int(index)), self.engine)
