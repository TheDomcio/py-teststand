from __future__ import annotations

import typing

from py_teststand.core.com_wrapper import COMWrapper, ts_interface

if typing.TYPE_CHECKING:
    from .connections import Borders, InsertionPalettePages


class InsertionPalette(COMWrapper):
    @property
    @ts_interface
    def allow_editing(self) -> bool:
        return bool(self._com_obj.AllowEditing)

    @allow_editing.setter
    @ts_interface
    def allow_editing(self, value: bool) -> None:
        self._com_obj.AllowEditing = value

    @property
    @ts_interface
    def borders(self) -> Borders:
        from .connections import Borders

        return Borders(self._com_obj.Borders, self._engine_ref)

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
    def h_wnd(self) -> int:
        return int(self._com_obj.hWnd)

    @h_wnd.setter
    @ts_interface
    def h_wnd(self, value: int) -> None:
        self._com_obj.hWnd = value

    @property
    @ts_interface
    def pages(self) -> InsertionPalettePages:
        from .connections import InsertionPalettePages

        return InsertionPalettePages(self._com_obj.Pages, self._engine_ref)

    @property
    @ts_interface
    def palette_layout(self) -> str:
        return str(self._com_obj.PaletteLayout)

    @palette_layout.setter
    @ts_interface
    def palette_layout(self, value: str) -> None:
        self._com_obj.PaletteLayout = value

    @property
    @ts_interface
    def scale_with_dpi(self) -> bool:
        return bool(self._com_obj.ScaleWithDPI)

    @scale_with_dpi.setter
    @ts_interface
    def scale_with_dpi(self, value: bool) -> None:
        self._com_obj.ScaleWithDPI = value

    def release(self) -> None:
        object.__setattr__(self, "_com_obj", None)
