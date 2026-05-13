from __future__ import annotations

import typing
from enum import IntEnum

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.ui.styles import AlignmentStyle, FontSource, MousePointerStyle


class BorderStyles(IntEnum):
    NoBorder = 0
    Fixed3D = 1
    FixedSingle = 2


class Label(COMWrapper):
    @property
    @ts_interface
    def alignment(self) -> AlignmentStyle:
        return AlignmentStyle(self._com_obj.Alignment)

    @alignment.setter
    @ts_interface
    def alignment(self, value: int | AlignmentStyle) -> None:
        self._com_obj.Alignment = int(value)

    @property
    @ts_interface
    def auto_size(self) -> bool:
        return bool(self._com_obj.AutoSize)

    @auto_size.setter
    @ts_interface
    def auto_size(self, value: bool) -> None:
        self._com_obj.AutoSize = value

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
    def border_style(self) -> BorderStyles:
        return BorderStyles(self._com_obj.BorderStyle)

    @border_style.setter
    @ts_interface
    def border_style(self, value: int | BorderStyles) -> None:
        self._com_obj.BorderStyle = int(value)

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
    def use_mnemonic(self) -> bool:
        return bool(self._com_obj.UseMnemonic)

    @use_mnemonic.setter
    @ts_interface
    def use_mnemonic(self, value: bool) -> None:
        self._com_obj.UseMnemonic = value

    @property
    @ts_interface
    def word_wrap(self) -> bool:
        return bool(self._com_obj.WordWrap)

    @word_wrap.setter
    @ts_interface
    def word_wrap(self, value: bool) -> None:
        self._com_obj.WordWrap = value

    @ts_interface
    def localize(self) -> None:
        self._com_obj.Localize()
