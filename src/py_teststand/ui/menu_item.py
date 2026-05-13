from __future__ import annotations

import typing
from enum import IntEnum

from py_teststand.core.com_wrapper import COMWrapper, ts_interface


class ExpressVIMenuItemProperties:
    ExpressVIMenu_IconProp = "IconHandle"
    ExpressVIMenu_IsSubmenuProp = "IsSubMenu"
    ExpressVIMenu_MenuItemsProp = "MenuItems"
    ExpressVIMenu_NameProp = "ItemName"
    ExpressVIMenu_PathProp = "ItemPath"
    ExpressVIMenu_SeparatorAboveProp = "SeparatorAbove"


class ToolMenuType(IntEnum):
    Command = 1
    Sequence = 2
    SequenceFile = 4
    SubMenu = 3


class EditTimeMenuItem(COMWrapper):
    @property
    @ts_interface
    def command_arguments(self) -> str:
        return str(self._com_obj.CommandArguments)

    @command_arguments.setter
    @ts_interface
    def command_arguments(self, value: str) -> None:
        self._com_obj.CommandArguments = value

    @property
    @ts_interface
    def command_arguments_expression(self) -> str:
        return str(self._com_obj.CommandArgumentsExpression)

    @command_arguments_expression.setter
    @ts_interface
    def command_arguments_expression(self, value: str) -> None:
        self._com_obj.CommandArgumentsExpression = value

    @property
    @ts_interface
    def command_initial_directory(self) -> str:
        return str(self._com_obj.CommandInitialDirectory)

    @command_initial_directory.setter
    @ts_interface
    def command_initial_directory(self, value: str) -> None:
        self._com_obj.CommandInitialDirectory = value

    @property
    @ts_interface
    def command_path(self) -> str:
        return str(self._com_obj.CommandPath)

    @command_path.setter
    @ts_interface
    def command_path(self, value: str) -> None:
        self._com_obj.CommandPath = value

    @property
    @ts_interface
    def editable(self) -> bool:
        return bool(self._com_obj.Editable)

    @editable.setter
    @ts_interface
    def editable(self, value: bool) -> None:
        self._com_obj.Editable = value

    @property
    @ts_interface
    def edits_selected_file(self) -> bool:
        return bool(self._com_obj.EditsSelectedFile)

    @edits_selected_file.setter
    @ts_interface
    def edits_selected_file(self, value: bool) -> None:
        self._com_obj.EditsSelectedFile = value

    @property
    @ts_interface
    def enabled_expression(self) -> str:
        return str(self._com_obj.EnabledExpression)

    @enabled_expression.setter
    @ts_interface
    def enabled_expression(self, value: str) -> None:
        self._com_obj.EnabledExpression = value

    @property
    @ts_interface
    def hidden_expression(self) -> str:
        return str(self._com_obj.HiddenExpression)

    @hidden_expression.setter
    @ts_interface
    def hidden_expression(self, value: str) -> None:
        self._com_obj.HiddenExpression = value

    @property
    @ts_interface
    def item_text_expression(self) -> str:
        return str(self._com_obj.ItemTextExpression)

    @item_text_expression.setter
    @ts_interface
    def item_text_expression(self, value: str) -> None:
        self._com_obj.ItemTextExpression = value

    @property
    @ts_interface
    def separator_before(self) -> bool:
        return bool(self._com_obj.SeparatorBefore)

    @separator_before.setter
    @ts_interface
    def separator_before(self, value: bool) -> None:
        self._com_obj.SeparatorBefore = value

    @property
    @ts_interface
    def sequence_file_path(self) -> str:
        return str(self._com_obj.SequenceFilePath)

    @sequence_file_path.setter
    @ts_interface
    def sequence_file_path(self, value: str) -> None:
        self._com_obj.SequenceFilePath = value

    @property
    @ts_interface
    def sequence_name(self) -> str:
        return str(self._com_obj.SequenceName)

    @sequence_name.setter
    @ts_interface
    def sequence_name(self, value: str) -> None:
        self._com_obj.SequenceName = value

    @property
    @ts_interface
    def sub_menu_items(self) -> EditTimeMenuItems:
        return EditTimeMenuItems(self._com_obj.SubMenuItems, self._engine_ref)

    @property
    @ts_interface
    def type(self) -> ToolMenuType:
        return ToolMenuType(self._com_obj.Type)

    @type.setter
    @ts_interface
    def type(self, value: int | ToolMenuType) -> None:
        self._com_obj.Type = int(value)


class EditTimeMenuItems(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index: typing.Any) -> EditTimeMenuItem:
        return EditTimeMenuItem(self._com_obj.Item(index), self._engine_ref)

    def __len__(self) -> int:
        return self.count

    def __getitem__(self, key: typing.Any) -> EditTimeMenuItem:
        return self.item(key)

    def __iter__(self) -> typing.Iterator[EditTimeMenuItem]:
        for i in range(self.count):
            yield self.item(i)

    @ts_interface
    def insert(self, name: str, index: int) -> EditTimeMenuItem:
        return EditTimeMenuItem(self._com_obj.Insert(name, index), self._engine_ref)

    @ts_interface
    def move_item(self, current_index: int, new_index: int) -> None:
        self._com_obj.MoveItem(current_index, new_index)

    @ts_interface
    def remove(self, index: int) -> None:
        self._com_obj.Remove(index)


class RunTimeMenuItem(COMWrapper):
    @property
    @ts_interface
    def edits_selected_file(self) -> bool:
        return bool(self._com_obj.EditsSelectedFile)

    @property
    @ts_interface
    def item_enabled(self) -> bool:
        return bool(self._com_obj.ItemEnabled)

    @property
    @ts_interface
    def separator_before(self) -> bool:
        return bool(self._com_obj.SeparatorBefore)

    @property
    @ts_interface
    def sub_menu_items(self) -> RunTimeMenuItems:
        return RunTimeMenuItems(self._com_obj.SubMenuItems, self._engine_ref)

    @property
    @ts_interface
    def text(self) -> str:
        return str(self._com_obj.Text)

    @ts_interface
    def invoke_item(self) -> None:
        self._com_obj.InvokeItem()


class RunTimeMenuItems(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index: typing.Any) -> RunTimeMenuItem:
        return RunTimeMenuItem(self._com_obj.Item(index), self._engine_ref)

    def __len__(self) -> int:
        return self.count

    def __getitem__(self, key: typing.Any) -> RunTimeMenuItem:
        return self.item(key)

    def __iter__(self) -> typing.Iterator[RunTimeMenuItem]:
        for i in range(self.count):
            yield self.item(i)
