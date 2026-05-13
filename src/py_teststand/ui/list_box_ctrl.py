from __future__ import annotations

import typing
from enum import IntFlag

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.ui.styles import AutoSizingOption, FontSource, MousePointerStyle

if typing.TYPE_CHECKING:
    from .connections import Borders


class EditingFlag(IntFlag):
    CutPasteDelete = 0x7
    Copy = 8
    DragDrop = 16
    Rename = 32


class ListBoxColumn(COMWrapper):
    @property
    @ts_interface
    def auto_sizing(self) -> AutoSizingOption:
        return AutoSizingOption(self._com_obj.AutoSizing)

    @auto_sizing.setter
    @ts_interface
    def auto_sizing(self, value: int | AutoSizingOption) -> None:
        self._com_obj.AutoSizing = int(value)

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
    def index(self) -> int:
        return int(self._com_obj.Index)

    @property
    @ts_interface
    def width(self) -> int:
        return int(self._com_obj.Width)

    @width.setter
    @ts_interface
    def width(self, value: int) -> None:
        self._com_obj.Width = value


class ListBoxColumns(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index_or_name: typing.Any) -> ListBoxColumn:
        return ListBoxColumn(self._com_obj.Item(index_or_name), self._engine_ref)

    def __len__(self) -> int:
        return self.count

    def __getitem__(self, key: typing.Any) -> ListBoxColumn:
        return self.item(key)

    def __iter__(self) -> typing.Iterator[ListBoxColumn]:
        for i in range(self.count):
            yield self.item(i)


class ListBox(COMWrapper):
    @property
    @ts_interface
    def auto_size_columns(self) -> bool:
        return bool(self._com_obj.AutoSizeColumns)

    @auto_size_columns.setter
    @ts_interface
    def auto_size_columns(self, value: bool) -> None:
        self._com_obj.AutoSizeColumns = value

    @property
    @ts_interface
    def back_color(self) -> int:
        return int(self._com_obj.BackColor)

    @back_color.setter
    @ts_interface
    def back_color(self, value: int) -> None:
        self._com_obj.BackColor = value

    @property
    @ts_interface
    def borders(self) -> Borders:
        from .connections import Borders

        return Borders(self._com_obj.Borders, self._engine_ref)

    @property
    @ts_interface
    def can_edit_label(self) -> bool:
        return bool(self._com_obj.CanEditLabel)

    @can_edit_label.setter
    @ts_interface
    def can_edit_label(self, value: bool) -> None:
        self._com_obj.CanEditLabel = value

    @property
    @ts_interface
    def columns(self) -> int:
        return int(self._com_obj.Columns)

    @columns.setter
    @ts_interface
    def columns(self, value: int) -> None:
        self._com_obj.Columns = value

    @property
    @ts_interface
    def column_set(self) -> ListBoxColumns:
        return ListBoxColumns(self._com_obj.ColumnSet, self._engine_ref)

    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @property
    @ts_interface
    def editing_flags(self) -> EditingFlag:
        return EditingFlag(self._com_obj.EditingFlags)

    @editing_flags.setter
    @ts_interface
    def editing_flags(self, value: int | EditingFlag) -> None:
        self._com_obj.EditingFlags = int(value)

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
    def font(self) -> typing.Any:
        return self._com_obj.Font

    @font.setter
    @ts_interface
    def font(self, value: typing.Any) -> None:
        self._com_obj.Font = value

    @property
    @ts_interface
    def font_source(self) -> FontSource:
        return FontSource(self._com_obj.FontSource)

    @font_source.setter
    @ts_interface
    def font_source(self, value: int | FontSource) -> None:
        self._com_obj.FontSource = int(value)

    @property
    @ts_interface
    def fore_color(self) -> int:
        return int(self._com_obj.ForeColor)

    @fore_color.setter
    @ts_interface
    def fore_color(self, value: int) -> None:
        self._com_obj.ForeColor = value

    @property
    @ts_interface
    def h_wnd(self) -> int:
        return int(self._com_obj.hWnd)

    @property
    @ts_interface
    def item_index(self) -> int:
        return int(self._com_obj.ItemIndex)

    @item_index.setter
    @ts_interface
    def item_index(self, value: int) -> None:
        self._com_obj.ItemIndex = value

    @property
    @ts_interface
    def mouse_icon(self) -> typing.Any:
        return self._com_obj.MouseIcon

    @mouse_icon.setter
    @ts_interface
    def mouse_icon(self, value: typing.Any) -> None:
        self._com_obj.MouseIcon = value

    @property
    @ts_interface
    def mouse_pointer(self) -> MousePointerStyle:
        return MousePointerStyle(self._com_obj.MousePointer)

    @mouse_pointer.setter
    @ts_interface
    def mouse_pointer(self, value: int | MousePointerStyle) -> None:
        self._com_obj.MousePointer = int(value)

    @property
    @ts_interface
    def scale_with_dpi(self) -> bool:
        return bool(self._com_obj.ScaleWithDPI)

    @scale_with_dpi.setter
    @ts_interface
    def scale_with_dpi(self, value: bool) -> None:
        self._com_obj.ScaleWithDPI = value

    @property
    @ts_interface
    def show_headers(self) -> bool:
        return bool(self._com_obj.ShowHeaders)

    @show_headers.setter
    @ts_interface
    def show_headers(self, value: bool) -> None:
        self._com_obj.ShowHeaders = value

    @property
    @ts_interface
    def tooltip_visible(self) -> bool:
        return bool(self._com_obj.TooltipVisible)

    @tooltip_visible.setter
    @ts_interface
    def tooltip_visible(self, value: bool) -> None:
        self._com_obj.TooltipVisible = value

    @ts_interface
    def edit_label(self) -> None:
        self._com_obj.EditLabel()

    @ts_interface
    def get_item_text(self, item_index: int, column_index: int) -> str:
        return str(self._com_obj.GetItemText(item_index, column_index))

    @ts_interface
    def hit_test(self, x: int, y: int) -> tuple[int, int, int]:
        return self._com_obj.HitTest(x, y, 0, 0, 0)
