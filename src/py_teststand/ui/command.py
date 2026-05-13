from __future__ import annotations

import typing
from enum import IntEnum, IntFlag

from py_teststand.core.com_wrapper import COMWrapper, ts_interface


class Command(COMWrapper):
    @property
    @ts_interface
    def kind(self) -> typing.Any:
        from .application_manager import CommandKind

        return CommandKind(int(self._com_obj.Kind))

    @property
    @ts_interface
    def enabled(self) -> bool:
        return bool(self._com_obj.Enabled)

    @enabled.setter
    @ts_interface
    def enabled(self, value: bool) -> None:
        self._com_obj.Enabled = value

    @property
    @ts_interface
    def visible(self) -> bool:
        return bool(self._com_obj.Visible)

    @visible.setter
    @ts_interface
    def visible(self, value: bool) -> None:
        self._com_obj.Visible = value

    @property
    @ts_interface
    def is_separator(self) -> bool:
        return bool(self._com_obj.IsSeparator)

    @property
    @ts_interface
    def is_toggle(self) -> bool:
        return bool(self._com_obj.IsToggle)

    @property
    @ts_interface
    def toggle_state(self) -> bool:
        return bool(self._com_obj.ToggleState)

    @toggle_state.setter
    @ts_interface
    def toggle_state(self, value: bool) -> None:
        self._com_obj.ToggleState = value

    @property
    @ts_interface
    def checked(self) -> bool:
        return self.toggle_state

    @checked.setter
    @ts_interface
    def checked(self, value: bool) -> None:
        self.toggle_state = value

    @property
    @ts_interface
    def caption(self) -> str:
        return str(self._com_obj.Caption)

    @caption.setter
    @ts_interface
    def caption(self, value: str) -> None:
        self._com_obj.Caption = value

    @property
    @ts_interface
    def display_name(self) -> str:

        return str(self._com_obj.GetDisplayName())

    @display_name.setter
    @ts_interface
    def display_name(self, value: str) -> None:

        self._com_obj.SetDisplayName(value)

    @property
    @ts_interface
    def icon_name(self) -> str:
        return str(self._com_obj.IconName)

    @property
    @ts_interface
    def lv_shortcut_key(self) -> int:
        return int(self._com_obj.LVShortcutKey)

    @lv_shortcut_key.setter
    @ts_interface
    def lv_shortcut_key(self, value: int) -> None:
        self._com_obj.LVShortcutKey = value

    @property
    @ts_interface
    def lv_shortcut_modifier(self) -> int:
        return int(self._com_obj.LVShortcutModifier)

    @lv_shortcut_modifier.setter
    @ts_interface
    def lv_shortcut_modifier(self, value: int) -> None:
        self._com_obj.LVShortcutModifier = value

    @property
    @ts_interface
    def shortcut_key(self) -> str:
        return str(self._com_obj.ShortcutKey)

    @shortcut_key.setter
    @ts_interface
    def shortcut_key(self, value: str) -> None:
        self._com_obj.ShortcutKey = value

    @property
    @ts_interface
    def shortcut_modifier(self) -> int:
        return int(self._com_obj.ShortcutModifier)

    @shortcut_modifier.setter
    @ts_interface
    def shortcut_modifier(self, value: int) -> None:
        self._com_obj.ShortcutModifier = value

    @property
    @ts_interface
    def user_data(self) -> typing.Any:
        return self._com_obj.UserData

    @user_data.setter
    @ts_interface
    def user_data(self, value: typing.Any) -> None:
        self._com_obj.UserData = value

    @property
    @ts_interface
    def user_object(self) -> typing.Any:
        return self._com_obj.UserObject

    @user_object.setter
    @ts_interface
    def user_object(self, value: typing.Any) -> None:
        self._com_obj.UserObject = value

    @property
    @ts_interface
    def sequence_file_view_mgr(self) -> typing.Any | None:
        from .sequence_file_view_manager import SequenceFileViewManager

        mgr = self._com_obj.SequenceFileViewMgr
        return SequenceFileViewManager(mgr, self._engine_ref) if mgr else None

    @property
    @ts_interface
    def execution_view_mgr(self) -> typing.Any | None:
        from .execution_view_manager import ExecutionViewManager

        mgr = self._com_obj.ExecutionViewMgr
        return ExecutionViewManager(mgr, self._engine_ref) if mgr else None

    @property
    @ts_interface
    def subsidiary_commands(self) -> typing.Any:
        return Commands(self._com_obj.SubsidiaryCommands, self._engine_ref)

    @ts_interface
    def execute(self, activate: bool = True) -> None:
        self._com_obj.Execute(activate)

    @property
    @ts_interface
    def entry_point(self) -> typing.Any:
        from .entry_point import EntryPoint

        obj = self._com_obj.EntryPoint
        return EntryPoint(obj, self._engine_ref) if obj else None

    @property
    @ts_interface
    def entry_point_index(self) -> int:
        return int(self._com_obj.EntryPointIndex)

    @ts_interface
    def get_display_name(self) -> str:
        return str(self._com_obj.GetDisplayName())

    @ts_interface
    def set_display_name(self, value: str) -> None:
        self._com_obj.SetDisplayName(str(value))


class Commands(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index: int) -> Command:
        return Command(self._com_obj.Item(index), self._engine_ref)

    def __len__(self) -> int:

        return self.count

    def __getitem__(self, index: int) -> Command:

        return self.item(index)

    def __iter__(self):

        for i in range(self.count):
            yield self.item(i)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def insert(self, command: Command, index: int) -> None:
        self._com_obj.Insert(command._com_obj, index)

    @ts_interface
    def insert_kind(self, command_kind: int, index: int) -> Command:
        return Command(self._com_obj.InsertKind(command_kind, index), self._engine_ref)

    @ts_interface
    def remove(self, index: int) -> None:
        self._com_obj.Remove(index)

    @ts_interface
    def insert_into_win32_menu(self, menu_handle: int, before_index: int = -1) -> None:
        self._com_obj.InsertIntoWin32Menu(menu_handle, before_index)


class ExecutionViewConnectionOption(IntFlag):
    NoneValue = 0x0
    IgnoreColors = 1


class ExecutionDisplayReason(IntEnum):
    UIMessage = 0
    StartExecution = 1
    Breakpoint = 2
    BreakOnUserRequest = 3
    BreakOnRunTimeError = 4
    GotoLocation = 5
