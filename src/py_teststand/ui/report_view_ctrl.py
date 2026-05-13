from __future__ import annotations

import typing
from enum import IntEnum, IntFlag

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.ui.styles import FontSource

if typing.TYPE_CHECKING:
    from .connections import Borders


class ToolBarTextStyle(IntEnum):
    TextBelow = 0
    TextRight = 1
    TextInvisible = 2


class ReportViewButton(IntFlag):
    NoneValue = 0x0
    Print = 64
    Find = 0x2
    Filter = 0x4
    Refresh = 0x8
    Back = 1
    ExternalViewer = 32
    FontSize = 128
    Forward = 2
    Home = 16
    OpenReportLocation = 512
    SelectActiveReport = 256
    Stop = 4


class ReportView(COMWrapper):
    @property
    @ts_interface
    def borders(self) -> Borders:
        from .connections import Borders

        return Borders(self._com_obj.Borders, self._engine_ref)

    @property
    @ts_interface
    def buttons_visible(self) -> ReportViewButton:
        return ReportViewButton(self._com_obj.ButtonsVisible)

    @buttons_visible.setter
    @ts_interface
    def buttons_visible(self, value: int | ReportViewButton) -> None:
        self._com_obj.ButtonsVisible = int(value)

    @property
    @ts_interface
    def large_icons(self) -> bool:
        return bool(self._com_obj.LargeIcons)

    @large_icons.setter
    @ts_interface
    def large_icons(self, value: bool) -> None:
        self._com_obj.LargeIcons = value

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
    def text_report_back_color(self) -> int:
        return int(self._com_obj.TextReportBackColor)

    @text_report_back_color.setter
    @ts_interface
    def text_report_back_color(self, value: int) -> None:
        self._com_obj.TextReportBackColor = value

    @property
    @ts_interface
    def text_report_color(self) -> int:
        return int(self._com_obj.TextReportColor)

    @text_report_color.setter
    @ts_interface
    def text_report_color(self, value: int) -> None:
        self._com_obj.TextReportColor = value

    @property
    @ts_interface
    def text_report_font(self) -> typing.Any:
        return self._com_obj.TextReportFont

    @property
    @ts_interface
    def text_report_font_source(self) -> FontSource:
        return FontSource(self._com_obj.TextReportFontSource)

    @text_report_font_source.setter
    @ts_interface
    def text_report_font_source(self, value: int | FontSource) -> None:
        self._com_obj.TextReportFontSource = int(value)

    @property
    @ts_interface
    def tool_bar_text_style(self) -> ToolBarTextStyle:
        return ToolBarTextStyle(self._com_obj.ToolBarTextStyle)

    @tool_bar_text_style.setter
    @ts_interface
    def tool_bar_text_style(self, value: int | ToolBarTextStyle) -> None:
        self._com_obj.ToolBarTextStyle = int(value)

    @property
    @ts_interface
    def tool_bar_visible(self) -> bool:
        return bool(self._com_obj.ToolBarVisible)

    @tool_bar_visible.setter
    @ts_interface
    def tool_bar_visible(self, value: bool) -> None:
        self._com_obj.ToolBarVisible = value

    @ts_interface
    def get_html_ctrl(self) -> int:
        return int(self._com_obj.GetHTMLCtrl())

    @ts_interface
    def get_rich_edit_ctrl(self) -> int:
        return int(self._com_obj.GetRichEditCtrl())

    @ts_interface
    def print_report(self, show_print_dialog: bool) -> None:
        self._com_obj.PrintReport(show_print_dialog)

    @ts_interface
    def update_from_execution(self, execution: typing.Any) -> None:
        raw_exec = getattr(execution, "_com_obj", execution)
        self._com_obj.UpdateFromExecution(raw_exec)

    @ts_interface
    def update_from_file(self, file_name: str) -> None:
        self._com_obj.UpdateFromFile(file_name)
