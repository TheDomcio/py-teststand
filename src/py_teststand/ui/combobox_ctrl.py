from __future__ import annotations

import typing
from enum import IntEnum

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.ui.styles import FontSource, MousePointerStyle


class ComboBoxStyle(IntEnum):
    DropDownCombo = 0
    DropDownList = 2


class ComboBox(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

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
    def height_with_dropdown(self) -> int:
        return int(self._com_obj.HeightWithDropdown)

    @height_with_dropdown.setter
    @ts_interface
    def height_with_dropdown(self, value: int) -> None:
        self._com_obj.HeightWithDropdown = value

    @property
    @ts_interface
    def h_wnd(self) -> int:
        return int(self._com_obj.hWnd)

    @ts_interface
    def get_item_text(self, index: int) -> str:
        return str(self._com_obj.GetItemText(index))

    @property
    @ts_interface
    def icon_size(self) -> int:
        return int(self._com_obj.IconSize)

    @icon_size.setter
    @ts_interface
    def icon_size(self, value: int) -> None:
        self._com_obj.IconSize = value

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
    def read_only(self) -> bool:
        return bool(self._com_obj.ReadOnly)

    @read_only.setter
    @ts_interface
    def read_only(self, value: bool) -> None:
        self._com_obj.ReadOnly = value

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
    def show_images(self) -> bool:
        return bool(self._com_obj.ShowImages)

    @show_images.setter
    @ts_interface
    def show_images(self, value: bool) -> None:
        self._com_obj.ShowImages = value

    @property
    @ts_interface
    def style(self) -> ComboBoxStyle:
        return ComboBoxStyle(self._com_obj.Style)

    @style.setter
    @ts_interface
    def style(self, value: int | ComboBoxStyle) -> None:
        self._com_obj.Style = int(value)

    @property
    @ts_interface
    def tooltip_visible(self) -> bool:
        return bool(self._com_obj.TooltipVisible)

    @tooltip_visible.setter
    @ts_interface
    def tooltip_visible(self, value: bool) -> None:
        self._com_obj.TooltipVisible = value
