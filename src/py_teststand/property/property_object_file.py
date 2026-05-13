from __future__ import annotations

import typing
from enum import IntEnum

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.property.property_object import PropertyObject


class PropertyObjectFileType(IntEnum):
    AdaptersConfigFile = 11
    ConfigFile = 0
    CustomConfigFile = 13
    GeneralEngineConfigFile = 9
    ProjectFile = 6
    PropertyObjectFile = 7
    SearchDirectoriesConfigFile = 10
    SequenceFile = 1
    StationGlobalsFile = 3
    TemplatesFile = 8
    TypePaletteFile = 2
    TypePalettesConfigFile = 12
    UsersFile = 4
    WorkspaceFile = 5


class FileWritingFormat(IntEnum):
    Ini = 1
    Binary = 2
    Xml = 3


class PropertyObjectFile(COMWrapper):
    @ts_interface
    def as_property_object(self) -> PropertyObject:
        return PropertyObject(self._com_obj.AsPropertyObject(), self._engine_ref)

    @ts_interface
    def check_for_modified_types(
        self,
        dlg_title: str,
        ok_button_text: str,
        options: int,
        version_inc_option: int,
    ) -> None:
        self._com_obj.CheckForModifiedTypes(
            str(dlg_title), str(ok_button_text), int(options), int(version_inc_option)
        )

    @ts_interface
    def handle_type_conflicts(self, handler_type: int) -> bool:
        return bool(self._com_obj.HandleTypeConflicts(int(handler_type)))

    @ts_interface
    def inc_change_count(self) -> None:
        self._com_obj.IncChangeCount()

    @ts_interface
    def lock(self, password_string: str = "") -> None:
        self._com_obj.Lock(str(password_string))

    @ts_interface
    def read_file(self, handler_type: int = 1) -> bool:
        return bool(self._com_obj.ReadFile(int(handler_type)))

    @ts_interface
    def save_file_if_modified(self, prompt: bool = True) -> bool:
        return bool(self._com_obj.SaveFileIfModified(bool(prompt)))

    @ts_interface
    def set_data(self, data: PropertyObject) -> None:
        self._com_obj.SetData(data._com_obj)

    @ts_interface
    def unlock(self, password_string: str) -> None:
        self._com_obj.Unlock(str(password_string))

    @ts_interface
    def write_file(self, write_format: int = 1) -> None:
        self._com_obj.WriteFile(int(write_format))

    @property
    @ts_interface
    def change_count(self) -> int:
        return int(self._com_obj.ChangeCount)

    @change_count.setter
    @ts_interface
    def change_count(self, value: int) -> None:
        self._com_obj.ChangeCount = int(value)

    @property
    @ts_interface
    def comment(self) -> str:
        return str(self._com_obj.Comment)

    @comment.setter
    @ts_interface
    def comment(self, value: str) -> None:
        self._com_obj.Comment = str(value)

    @property
    @ts_interface
    def content_type(self) -> str:
        return str(self._com_obj.ContentType)

    @content_type.setter
    @ts_interface
    def content_type(self, value: str) -> None:
        self._com_obj.ContentType = str(value)

    @property
    @ts_interface
    def data(self) -> PropertyObject:
        return PropertyObject(self._com_obj.Data, self._engine_ref)

    @data.setter
    @ts_interface
    def data(self, value: PropertyObject) -> None:
        self._com_obj.Data = value._com_obj

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
    def edit_privilege(self) -> str:
        return str(self._com_obj.EditPrivilege)

    @edit_privilege.setter
    @ts_interface
    def edit_privilege(self, value: str) -> None:
        self._com_obj.EditPrivilege = str(value)

    @property
    @ts_interface
    def file_section(self) -> str:
        return str(self._com_obj.FileSection)

    @file_section.setter
    @ts_interface
    def file_section(self, value: str) -> None:
        self._com_obj.FileSection = str(value)

    @property
    @ts_interface
    def file_type(self) -> PropertyObjectFileType:
        return PropertyObjectFileType(self._com_obj.FileType)

    @property
    @ts_interface
    def file_type_description(self) -> str:
        return str(self._com_obj.FileTypeDescription)

    @file_type_description.setter
    @ts_interface
    def file_type_description(self, value: str) -> None:
        self._com_obj.FileTypeDescription = str(value)

    @property
    @ts_interface
    def file_writing_format(self) -> int:
        return int(self._com_obj.FileWritingFormat)

    @file_writing_format.setter
    @ts_interface
    def file_writing_format(self, value: int) -> None:
        self._com_obj.FileWritingFormat = int(value)

    @property
    @ts_interface
    def id(self) -> int:
        return int(self._com_obj.Id)

    @property
    @ts_interface
    def is_disk_file_modified(self) -> int:
        return int(self._com_obj.IsDiskFileModified)

    @property
    @ts_interface
    def is_disk_file_read_only(self) -> bool:
        return bool(self._com_obj.IsDiskFileReadOnly)

    @property
    @ts_interface
    def is_modified(self) -> bool:
        return bool(self._com_obj.IsModified)

    @property
    @ts_interface
    def is_modified_by_user(self) -> bool:
        return bool(self._com_obj.IsModifiedByUser)

    @property
    @ts_interface
    def last_saved_change_count(self) -> int:
        return int(self._com_obj.LastSavedChangeCount)

    @property
    @ts_interface
    def locked(self) -> bool:
        return bool(self._com_obj.Locked)

    @property
    @ts_interface
    def open_status(self) -> int:
        return int(self._com_obj.OpenStatus)

    @open_status.setter
    @ts_interface
    def open_status(self, value: int) -> None:
        self._com_obj.OpenStatus = int(value)

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
    def protection(self) -> int:
        return int(self._com_obj.Protection)

    @protection.setter
    @ts_interface
    def protection(self, value: int) -> None:
        self._com_obj.Protection = int(value)

    @property
    @ts_interface
    def requirements(self) -> PropertyObject:
        return PropertyObject(self._com_obj.Requirements, self._engine_ref)

    @property
    @ts_interface
    def type_usage_list(self) -> TypeUsageList:
        return TypeUsageList(self._com_obj.TypeUsageList, self._engine_ref)

    @property
    @ts_interface
    def version(self) -> str:
        return str(self._com_obj.Version)

    @version.setter
    @ts_interface
    def version(self, value: str) -> None:
        self._com_obj.Version = str(value)


class TypeUsageList(COMWrapper):
    @property
    @ts_interface
    def change_count(self) -> int:
        return int(self._com_obj.ChangeCount)

    @property
    @ts_interface
    def num_types(self) -> int:
        return int(self._com_obj.NumTypes)

    @ts_interface
    def add_used_types(self, prop_object: PropertyObject) -> bool:
        return bool(self._com_obj.AddUsedTypes(prop_object._com_obj))

    @ts_interface
    def create_and_insert_new_type_from_existing(
        self,
        existing_type: PropertyObject,
        index: int,
        type_category: int,
        reserved: int = 0,
    ) -> PropertyObject:
        return PropertyObject(
            self._com_obj.CreateAndInsertNewTypeFromExisting(
                existing_type._com_obj, int(index), int(type_category), int(reserved)
            ),
            self._engine_ref,
        )

    @ts_interface
    def get_is_type_attached_to_file(self, index: int) -> bool:
        return bool(self._com_obj.GetIsTypeAttachedToFile(int(index)))

    @ts_interface
    def get_type_definition(self, index: int) -> PropertyObject:
        return PropertyObject(self._com_obj.GetTypeDefinition(int(index)), self._engine_ref)

    @ts_interface
    def get_type_index(self, type_name: str) -> int:
        return int(self._com_obj.GetTypeIndex(str(type_name)))

    @ts_interface
    def insert_type(self, type_to_insert: PropertyObject, index: int, type_category: int) -> None:
        self._com_obj.InsertType(type_to_insert._com_obj, int(index), int(type_category))

    @ts_interface
    def move_type(self, index: int, new_index: int) -> None:
        self._com_obj.MoveType(int(index), int(new_index))

    @ts_interface
    def remove_type(self, index: int) -> PropertyObject:
        return PropertyObject(self._com_obj.RemoveType(int(index)), self._engine_ref)

    @ts_interface
    def set_is_type_attached_to_file(self, index: int, store: bool) -> None:
        self._com_obj.SetIsTypeAttachedToFile(int(index), bool(store))

    @ts_interface
    def union(self, union_type_usage_list: TypeUsageList) -> bool:
        return bool(self._com_obj.Union(union_type_usage_list._com_obj))

    @ts_interface
    def validate_new_type_name(self, new_name: str, allow_duplicates: bool) -> typing.Any:
        return self._com_obj.ValidateNewTypeName(str(new_name), bool(allow_duplicates))

    def __len__(self) -> int:
        return self.num_types
