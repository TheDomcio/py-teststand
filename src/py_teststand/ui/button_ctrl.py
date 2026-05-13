from __future__ import annotations

import typing
from enum import IntEnum

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.ui.styles import ContentAlignmentStyle, FontSource, MousePointerStyle


class ButtonActionStyle(IntEnum):
    PushButton = 0
    ToggleButton = 1


class ButtonStyle(IntEnum):
    Standard = 1
    ToolBar = 2


class ButtonSizing(IntEnum):
    AlwaysAutoSize = 0
    GrowOnly = 1
    ShrinkOnly = 2
    NeverAutoSize = 3


class TextImageRelation(IntEnum):
    Overlay = 0
    ImageBelowText = 1
    ImageAboveText = 2
    ImageBeforeText = 3
    ImageAfterText = 4


class Button(COMWrapper):
    @property
    @ts_interface
    def action_style(self) -> ButtonActionStyle:
        return ButtonActionStyle(self._com_obj.ActionStyle)

    @action_style.setter
    @ts_interface
    def action_style(self, value: int | ButtonActionStyle) -> None:
        self._com_obj.ActionStyle = int(value)

    @property
    @ts_interface
    def auto_sizing(self) -> ButtonSizing:
        return ButtonSizing(self._com_obj.AutoSizing)

    @auto_sizing.setter
    @ts_interface
    def auto_sizing(self, value: int | ButtonSizing) -> None:
        self._com_obj.AutoSizing = int(value)

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
    def caption(self) -> str:
        return str(self._com_obj.Caption)

    @caption.setter
    @ts_interface
    def caption(self, value: str) -> None:
        self._com_obj.Caption = value

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
    def image(self) -> typing.Any:
        return self._com_obj.Image

    @image.setter
    @ts_interface
    def image(self, value: typing.Any) -> None:
        self._com_obj.Image = value

    @property
    @ts_interface
    def image_alignment(self) -> ContentAlignmentStyle:
        return ContentAlignmentStyle(self._com_obj.ImageAlignment)

    @image_alignment.setter
    @ts_interface
    def image_alignment(self, value: int | ContentAlignmentStyle) -> None:
        self._com_obj.ImageAlignment = int(value)

    @property
    @ts_interface
    def mask_color(self) -> int:
        return int(self._com_obj.MaskColor)

    @mask_color.setter
    @ts_interface
    def mask_color(self, value: int) -> None:
        self._com_obj.MaskColor = value

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
    def show_focus_rect(self) -> bool:
        return bool(self._com_obj.ShowFocusRect)

    @show_focus_rect.setter
    @ts_interface
    def show_focus_rect(self, value: bool) -> None:
        self._com_obj.ShowFocusRect = value

    @property
    @ts_interface
    def style(self) -> ButtonStyle:
        return ButtonStyle(self._com_obj.Style)

    @style.setter
    @ts_interface
    def style(self, value: int | ButtonStyle) -> None:
        self._com_obj.Style = int(value)

    @property
    @ts_interface
    def text_alignment(self) -> ContentAlignmentStyle:
        return ContentAlignmentStyle(self._com_obj.TextAlignment)

    @text_alignment.setter
    @ts_interface
    def text_alignment(self, value: int | ContentAlignmentStyle) -> None:
        self._com_obj.TextAlignment = int(value)

    @property
    @ts_interface
    def text_image_relation(self) -> TextImageRelation:
        return TextImageRelation(self._com_obj.TextImageRelation)

    @text_image_relation.setter
    @ts_interface
    def text_image_relation(self, value: int | TextImageRelation) -> None:
        self._com_obj.TextImageRelation = int(value)

    @property
    @ts_interface
    def user_data(self) -> typing.Any:
        return self._com_obj.UserData

    @user_data.setter
    @ts_interface
    def user_data(self, value: typing.Any) -> None:
        self._com_obj.UserData = value

    @ts_interface
    def do_click(self) -> None:
        self._com_obj.DoClick()

    @ts_interface
    def localize(self) -> None:
        self._com_obj.Localize()
