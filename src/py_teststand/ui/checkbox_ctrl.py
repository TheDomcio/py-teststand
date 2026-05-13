from __future__ import annotations

import typing
from enum import IntEnum

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.ui.styles import ContentAlignmentStyle, FontSource


class CheckBoxStyle(IntEnum):
    Normal = 0
    Button = 1


class CheckBox(COMWrapper):
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
    def checked(self) -> bool:
        return bool(self._com_obj.Checked)

    @checked.setter
    @ts_interface
    def checked(self, value: bool) -> None:
        self._com_obj.Checked = value

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
    def image_align(self) -> ContentAlignmentStyle:
        return ContentAlignmentStyle(self._com_obj.ImageAlign)

    @image_align.setter
    @ts_interface
    def image_align(self, value: int | ContentAlignmentStyle) -> None:
        self._com_obj.ImageAlign = int(value)

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
    def scale_with_dpi(self) -> bool:
        return bool(self._com_obj.ScaleWithDPI)

    @scale_with_dpi.setter
    @ts_interface
    def scale_with_dpi(self, value: bool) -> None:
        self._com_obj.ScaleWithDPI = value

    @property
    @ts_interface
    def style(self) -> CheckBoxStyle:
        return CheckBoxStyle(self._com_obj.Style)

    @style.setter
    @ts_interface
    def style(self, value: int | CheckBoxStyle) -> None:
        self._com_obj.Style = int(value)

    @property
    @ts_interface
    def text_align(self) -> ContentAlignmentStyle:
        return ContentAlignmentStyle(self._com_obj.TextAlign)

    @text_align.setter
    @ts_interface
    def text_align(self, value: int | ContentAlignmentStyle) -> None:
        self._com_obj.TextAlign = int(value)

    @ts_interface
    def localize(self) -> None:
        self._com_obj.Localize()
