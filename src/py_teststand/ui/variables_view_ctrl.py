from __future__ import annotations

import typing

from py_teststand.core.com_wrapper import COMWrapper, ts_interface

if typing.TYPE_CHECKING:
    from .connections import Borders


class VariablesViewCtrl(COMWrapper):
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

    @property
    @ts_interface
    def borders(self) -> Borders:
        from .connections import Borders

        return Borders(self._com_obj.Borders, self._engine_ref)

    @property
    @ts_interface
    def scale_with_dpi(self) -> bool:
        return bool(self._com_obj.ScaleWithDPI)

    @scale_with_dpi.setter
    @ts_interface
    def scale_with_dpi(self, value: bool) -> None:
        self._com_obj.ScaleWithDPI = value
