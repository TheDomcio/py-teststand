from __future__ import annotations

from py_teststand.core.com_wrapper import COMWrapper, ts_interface


class SearchDirectory(COMWrapper):
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
    def disabled(self) -> bool:
        return bool(self._com_obj.Disabled)

    @disabled.setter
    @ts_interface
    def disabled(self, value: bool) -> None:
        self._com_obj.Disabled = bool(value)

    @property
    @ts_interface
    def search_subdirectories(self) -> bool:
        return bool(self._com_obj.SearchSubdirectories)

    @search_subdirectories.setter
    @ts_interface
    def search_subdirectories(self, value: bool) -> None:
        self._com_obj.SearchSubdirectories = bool(value)

    @property
    @ts_interface
    def file_extension_restrictions(self) -> str:
        return str(self._com_obj.FileExtensionRestrictions)

    @file_extension_restrictions.setter
    @ts_interface
    def file_extension_restrictions(self, value: str) -> None:
        self._com_obj.FileExtensionRestrictions = str(value)

    @property
    @ts_interface
    def exclude_file_extension(self) -> bool:
        return bool(self._com_obj.ExcludeFileExtension)

    @exclude_file_extension.setter
    @ts_interface
    def exclude_file_extension(self, value: bool) -> None:
        self._com_obj.ExcludeFileExtension = bool(value)

    @property
    @ts_interface
    def exclude_hidden_subdirectories(self) -> bool:
        return bool(self._com_obj.ExcludeHiddenSubdirectories)

    @exclude_hidden_subdirectories.setter
    @ts_interface
    def exclude_hidden_subdirectories(self, value: bool) -> None:
        self._com_obj.ExcludeHiddenSubdirectories = bool(value)

    @property
    @ts_interface
    def type(self) -> int:
        return int(self._com_obj.Type)


class SearchDirectories(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index: int) -> SearchDirectory:
        return SearchDirectory(self._com_obj.Item(int(index)), self._engine_ref)

    def __len__(self) -> int:

        return self.count

    def __getitem__(self, index: int) -> SearchDirectory:

        return self.item(index)

    def __iter__(self):

        for i in range(self.count):
            yield self.item(i)

    @ts_interface
    def insert(
        self,
        path: str,
        index: int = -1,
        search_sub_dirs: bool = False,
        file_ext_restrict: str = "",
        exclude: bool = False,
        disabled: bool = False,
    ) -> None:
        self._com_obj.Insert(
            str(path),
            int(index),
            bool(search_sub_dirs),
            str(file_ext_restrict),
            bool(exclude),
            bool(disabled),
        )

    @ts_interface
    def remove(self, index: int) -> None:
        self._com_obj.Remove(int(index))

    @ts_interface
    def reload(self) -> None:
        self._com_obj.Reload()

    @ts_interface
    def move_search_directory(self, index: int, new_index: int) -> None:
        self._com_obj.MoveSearchDirectory(int(index), int(new_index))
