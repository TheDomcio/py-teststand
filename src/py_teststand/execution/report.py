from __future__ import annotations

import typing
from enum import IntEnum
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.property.property_object import PropertyObject

if TYPE_CHECKING:
    pass


class ReportConversion(IntEnum):
    NoConversion = 0
    ToCRLF = 1
    FromCRLF = 2


class Report(COMWrapper):
    @property
    @ts_interface
    def all(self) -> str:
        return str(self._com_obj.All)

    @ts_interface
    def append(self, string_to_append: str) -> int:
        return int(self._com_obj.Append(str(string_to_append)))

    @ts_interface
    def as_property_object(self) -> PropertyObject:
        return PropertyObject(self._com_obj.AsPropertyObject(), self._engine_ref)

    @property
    @ts_interface
    def format(self) -> str:
        return str(self._com_obj.Format)

    @format.setter
    @ts_interface
    def format(self, value: str) -> None:
        self._com_obj.Format = str(value)

    @ts_interface
    def get_section(self, oldest_index: int, latest_index: int) -> str:
        return str(self._com_obj.GetSection(int(oldest_index), int(latest_index)))

    @ts_interface
    def get_temp_file(self, linefeed_conversion: int, extension_string: str = "") -> str:
        return str(self._com_obj.GetTempFile(int(linefeed_conversion), str(extension_string)))

    @ts_interface
    def launch_viewer(self, linefeed_conversion: int) -> None:
        self._com_obj.LaunchViewer(int(linefeed_conversion))

    @ts_interface
    def load(self, path_string: str, linefeed_conversion: int) -> None:
        self._com_obj.Load(str(path_string), int(linefeed_conversion))

    @property
    @ts_interface
    def location(self) -> str:
        return str(self._com_obj.Location)

    @location.setter
    @ts_interface
    def location(self, value: str) -> None:
        self._com_obj.Location = str(value)

    @ts_interface
    def new_report_section(self) -> ReportSection:
        return ReportSection(self._com_obj.NewReportSection(), self._engine_ref)

    @ts_interface
    def refresh_display(self) -> None:
        self._com_obj.RefreshDisplay()

    @property
    @ts_interface
    def report_section(self) -> ReportSection:
        return ReportSection(self._com_obj.ReportSection, self._engine_ref)

    @report_section.setter
    @ts_interface
    def report_section(self, value: ReportSection) -> None:
        self._com_obj.ReportSection = value._com_obj

    @ts_interface
    def reset(self, new_value: str) -> int:
        return int(self._com_obj.Reset(str(new_value)))

    @property
    @ts_interface
    def reset_count(self) -> int:
        return int(self._com_obj.ResetCount)

    @ts_interface
    def save(
        self,
        path_string: str,
        append_if_already_exists: bool,
        linefeed_conversion: int,
    ) -> None:
        self._com_obj.Save(
            str(path_string), bool(append_if_already_exists), int(linefeed_conversion)
        )

    @ts_interface
    def set_temp_file_directory_ex(
        self, directory: str, temp_file_directory_option: int = 0
    ) -> None:
        self._com_obj.SetTempFileDirectoryEx(str(directory), int(temp_file_directory_option))

    @property
    @ts_interface
    def style_sheet_path(self) -> str:
        return str(self._com_obj.StyleSheetPath)

    @style_sheet_path.setter
    @ts_interface
    def style_sheet_path(self, value: str) -> None:
        self._com_obj.StyleSheetPath = str(value)

    @property
    @ts_interface
    def id(self) -> int:
        return int(self._com_obj.Id)

    @property
    @ts_interface
    def is_empty(self) -> bool:
        return bool(self._com_obj.IsEmpty)

    @property
    @ts_interface
    def latest_append_index(self) -> int:
        return int(self._com_obj.LatestAppendIndex)

    @property
    @ts_interface
    def suspend_report_refresh(self) -> bool:
        return bool(self._com_obj.SuspendReportRefresh)

    @suspend_report_refresh.setter
    @ts_interface
    def suspend_report_refresh(self, value: bool) -> None:
        self._com_obj.SuspendReportRefresh = bool(value)

    @property
    @ts_interface
    def temp_file_directory(self) -> str:
        return str(self._com_obj.TempFileDirectory)

    @temp_file_directory.setter
    @ts_interface
    def temp_file_directory(self, value: str) -> None:
        self._com_obj.TempFileDirectory = str(value)


class Reports(COMWrapper):
    @property
    @ts_interface
    def active_report(self) -> Report | None:
        com_report = self._com_obj.ActiveReport
        return Report(com_report, self._engine_ref) if com_report else None

    @active_report.setter
    @ts_interface
    def active_report(self, value: Report | None) -> None:
        self._com_obj.ActiveReport = value._com_obj if value else None

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def insert(self, index: int = -1) -> Report:
        return Report(self._com_obj.Insert(int(index)), self._engine_ref)

    @ts_interface
    def insert_existing(self, report: Report, index: int = -1) -> None:
        self._com_obj.InsertExisting(report._com_obj, int(index))

    @ts_interface
    def item(self, index: int | str) -> Report:
        return Report(self._com_obj.Item(index), self._engine_ref)

    @ts_interface
    def remove(self, index: int) -> Report:
        return Report(self._com_obj.Remove(int(index)), self._engine_ref)

    @ts_interface
    def replace(self, old_val: Report, new_val: Report) -> Report:
        return Report(self._com_obj.Replace(old_val._com_obj, new_val._com_obj), self._engine_ref)

    def __len__(self) -> int:
        return self.count

    def __getitem__(self, index: int | str) -> Report:
        return self.item(index)

    def __iter__(self) -> typing.Iterator[Report]:
        for i in range(self.count):
            yield self.item(i)


class ReportSection(COMWrapper):
    @property
    @ts_interface
    def body(self) -> str:
        return str(self._com_obj.Body)

    @body.setter
    @ts_interface
    def body(self, value: str) -> None:
        self._com_obj.Body = str(value)

    @property
    @ts_interface
    def footer(self) -> str:
        return str(self._com_obj.Footer)

    @footer.setter
    @ts_interface
    def footer(self, value: str) -> None:
        self._com_obj.Footer = str(value)

    @ts_interface
    def get_all_text(self) -> str:
        return str(self._com_obj.GetAllText())

    @property
    @ts_interface
    def header(self) -> str:
        return str(self._com_obj.Header)

    @header.setter
    @ts_interface
    def header(self, value: str) -> None:
        self._com_obj.Header = str(value)

    @property
    @ts_interface
    def id(self) -> int:
        return int(self._com_obj.Id)

    @property
    @ts_interface
    def is_empty(self) -> bool:
        return bool(self._com_obj.IsEmpty)

    @property
    @ts_interface
    def report_subsections(self) -> ReportSections:
        return ReportSections(self._com_obj.ReportSubsections, self._engine_ref)


class ReportSections(COMWrapper):
    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def insert(
        self, index: int = -1, header: str = "", body: str = "", footer: str = ""
    ) -> ReportSection:
        return ReportSection(
            self._com_obj.Insert(int(index), str(header), str(body), str(footer)),
            self._engine_ref,
        )

    @ts_interface
    def insert_existing(self, section: ReportSection, index: int = -1) -> None:
        self._com_obj.InsertExisting(section._com_obj, int(index))

    @ts_interface
    def item(self, index: int | str) -> ReportSection:
        return ReportSection(self._com_obj.Item(index), self._engine_ref)

    @ts_interface
    def remove(self, index: int) -> ReportSection:
        return ReportSection(self._com_obj.Remove(int(index)), self._engine_ref)

    def __len__(self) -> int:
        return self.count

    def __getitem__(self, index: int | str) -> ReportSection:
        return self.item(index)

    def __iter__(self) -> typing.Iterator[ReportSection]:
        for i in range(self.count):
            yield self.item(i)
