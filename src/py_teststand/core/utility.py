from __future__ import annotations

from py_teststand.core.com_wrapper import COMWrapper, ts_interface


class Utility(COMWrapper):
    @ts_interface
    def escape(self, string_to_escape: str, options: int = 0) -> str:
        return str(self._com_obj.Escape(str(string_to_escape), int(options)))

    @ts_interface
    def unescape(self, string_to_unescape: str, options: int = 0) -> str:
        return str(self._com_obj.Unescape(str(string_to_unescape), int(options)))

    @ts_interface
    def create_debug_logs(self, reserved: int = 0) -> None:
        self._com_obj.CreateDebugLogs(int(reserved))
