from __future__ import annotations

import typing
from enum import IntFlag
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COMWrapper, ts_interface

if TYPE_CHECKING:
    from py_teststand.core.engine import Engine
    from py_teststand.property.property_object_file import PropertyObjectFile
    from py_teststand.workspace.workspace_object import WorkspaceObject


class SaveWorkspaceFileOption(IntFlag):
    NoneValue = 0x0
    PromptUser = 0x1
    SkipReadOnlyFiles = 0x4
    SkipWorkspaceFile = 0x2


class WorkspaceFile(COMWrapper):
    def __init__(self, com_obj: typing.Any, engine: Engine | None = None) -> None:
        super().__init__(com_obj, engine)

    @property
    @ts_interface
    def is_connected_to_sc_provider(self) -> bool:
        return bool(self._com_obj.IsConnectedToSCProvider)

    @property
    @ts_interface
    def provider_name(self) -> str:
        return str(self._com_obj.ProviderName)

    @provider_name.setter
    @ts_interface
    def provider_name(self, value: str) -> None:
        self._com_obj.ProviderName = value

    @property
    @ts_interface
    def options_file(self) -> PropertyObjectFile:
        from py_teststand.property.property_object_file import PropertyObjectFile

        return PropertyObjectFile(self._com_obj.OptionsFile, self.engine)

    @property
    @ts_interface
    def root_workspace_object(self) -> WorkspaceObject:
        from py_teststand.workspace.workspace_object import WorkspaceObject

        return WorkspaceObject(self._com_obj.RootWorkspaceObject, self.engine)

    @property
    @ts_interface
    def path(self) -> str:
        return str(self._com_obj.AsPropertyObjectFile().Path)

    @ts_interface
    def find_workspace_object(self, path: str) -> WorkspaceObject | None:
        from py_teststand.workspace.workspace_object import WorkspaceObject

        com_obj = self._com_obj.FindWorkspaceObject(path)
        return WorkspaceObject(com_obj, self.engine) if com_obj else None

    @ts_interface
    def save_workspace_and_project_files(self, options: int | SaveWorkspaceFileOption = 0) -> bool:
        return bool(self._com_obj.SaveWorkspaceAndProjectFiles(int(options)))

    @ts_interface
    def display_add_file_to_workspace_dialog(
        self, selected_project: WorkspaceObject | typing.Any, full_path: str
    ) -> bool:
        proj_com = getattr(selected_project, "_com_obj", selected_project)
        return bool(self._com_obj.DisplayAddFileToWorkspaceDialog(proj_com, full_path))

    @ts_interface
    def run_source_control_provider(self) -> None:
        self._com_obj.RunSourceControlProvider()

    @ts_interface
    def as_property_object_file(self) -> PropertyObjectFile:
        from py_teststand.property.property_object_file import PropertyObjectFile

        return PropertyObjectFile(self._com_obj.AsPropertyObjectFile(), self.engine)
