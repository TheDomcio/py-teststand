from __future__ import annotations

import typing
from enum import IntEnum, IntFlag

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.ui.styles import FontSource

if typing.TYPE_CHECKING:
    from .connections import Borders, ListBarPages


class ListBarPageStyles(IntFlag):
    FrameSelectedItem = 0x1
    Tracking = 0x2
    IconsOnTop = 0x4


class ListBarButtonStyles(IntEnum):
    ThreeD = 1
    Flat = 2


class ListBar(COMWrapper):
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
    def button_font(self) -> typing.Any:
        return self._com_obj.ButtonFont

    @button_font.setter
    @ts_interface
    def button_font(self, value: typing.Any) -> None:
        self._com_obj.ButtonFont = value

    @property
    @ts_interface
    def button_font_source(self) -> FontSource:
        return FontSource(self._com_obj.ButtonFontSource)

    @button_font_source.setter
    @ts_interface
    def button_font_source(self, value: int | FontSource) -> None:
        self._com_obj.ButtonFontSource = int(value)

    @property
    @ts_interface
    def button_style(self) -> ListBarButtonStyles:
        return ListBarButtonStyles(self._com_obj.ButtonStyle)

    @button_style.setter
    @ts_interface
    def button_style(self, value: int | ListBarButtonStyles) -> None:
        self._com_obj.ButtonStyle = int(value)

    @property
    @ts_interface
    def button_text_color(self) -> int:
        return int(self._com_obj.ButtonTextColor)

    @button_text_color.setter
    @ts_interface
    def button_text_color(self, value: int) -> None:
        self._com_obj.ButtonTextColor = value

    @property
    @ts_interface
    def current_page(self) -> int:
        return int(self._com_obj.CurrentPage)

    @current_page.setter
    @ts_interface
    def current_page(self, value: int) -> None:
        self._com_obj.CurrentPage = value

    @property
    @ts_interface
    def h_wnd(self) -> int:
        return int(self._com_obj.hWnd)

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
    def page_font(self) -> typing.Any:
        return self._com_obj.PageFont

    @page_font.setter
    @ts_interface
    def page_font(self, value: typing.Any) -> None:
        self._com_obj.PageFont = value

    @property
    @ts_interface
    def page_font_source(self) -> FontSource:
        return FontSource(self._com_obj.PageFontSource)

    @page_font_source.setter
    @ts_interface
    def page_font_source(self, value: int | FontSource) -> None:
        self._com_obj.PageFontSource = int(value)

    @property
    @ts_interface
    def pages(self) -> ListBarPages:
        from .connections import ListBarPages

        return ListBarPages(self._com_obj.Pages, self._engine_ref)

    @property
    @ts_interface
    def page_style(self) -> ListBarPageStyles:
        return ListBarPageStyles(self._com_obj.PageStyle)

    @page_style.setter
    @ts_interface
    def page_style(self, value: int | ListBarPageStyles) -> None:
        self._com_obj.PageStyle = int(value)

    @property
    @ts_interface
    def page_text_color(self) -> int:
        return int(self._com_obj.PageTextColor)

    @page_text_color.setter
    @ts_interface
    def page_text_color(self, value: int) -> None:
        self._com_obj.PageTextColor = value

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
    def show_item_count(self) -> bool:
        return bool(self._com_obj.ShowItemCount)

    @show_item_count.setter
    @ts_interface
    def show_item_count(self, value: bool) -> None:
        self._com_obj.ShowItemCount = value

    @property
    @ts_interface
    def show_item_tip_strips(self) -> bool:
        return bool(self._com_obj.ShowItemTipStrips)

    @show_item_tip_strips.setter
    @ts_interface
    def show_item_tip_strips(self, value: bool) -> None:
        self._com_obj.ShowItemTipStrips = value

    @property
    @ts_interface
    def show_scroll_bar(self) -> bool:
        return bool(self._com_obj.ShowScrollBar)

    @show_scroll_bar.setter
    @ts_interface
    def show_scroll_bar(self, value: bool) -> None:
        self._com_obj.ShowScrollBar = value

    @ts_interface
    def hit_test(self, x: int, y: int) -> int:
        return int(self._com_obj.HitTest(x, y))

    @ts_interface
    def localize(self) -> None:
        self._com_obj.Localize()
