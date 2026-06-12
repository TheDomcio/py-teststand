from __future__ import annotations

import typing
from enum import IntEnum

from py_teststand.core.com_wrapper import COMWrapper, ts_interface


class FileOpenMode(IntEnum):
    NoneValue = 0
    Truncate = 1
    Append = 2
    Uniquify = 4


class ExecutionOutputRecordStream(COMWrapper):
    @property
    @ts_interface
    def close_at_next_uut_or_batch(self) -> bool:
        return bool(self._com_obj.CloseAtNextUUTOrBatch)

    @close_at_next_uut_or_batch.setter
    @ts_interface
    def close_at_next_uut_or_batch(self, value: bool) -> None:
        self._com_obj.CloseAtNextUUTOrBatch = bool(value)

    @property
    @ts_interface
    def format(self) -> str:
        return str(self._com_obj.Format)

    @format.setter
    @ts_interface
    def format(self, value: str) -> None:
        self._com_obj.Format = str(value)

    @property
    @ts_interface
    def name(self) -> str:
        return str(self._com_obj.Name)

    @property
    @ts_interface
    def num_records_to_display_in_report_view(self) -> int:
        return int(self._com_obj.NumRecordsToDisplayInReportView)

    @num_records_to_display_in_report_view.setter
    @ts_interface
    def num_records_to_display_in_report_view(self, value: int) -> None:
        self._com_obj.NumRecordsToDisplayInReportView = int(value)

    @ts_interface
    def clear_records_from_report_view(self) -> None:
        self._com_obj.ClearRecordsFromReportView()

    @ts_interface
    def close(self) -> None:
        self._com_obj.Close()

    @ts_interface
    def define_fields(self, field_definitions: typing.Any, mapping: str = "") -> None:
        self._com_obj.DefineFields(field_definitions, str(mapping))

    @ts_interface
    def flush(self) -> None:
        self._com_obj.Flush()

    @ts_interface
    def insert(self, stream: ExecutionOutputRecordStream) -> None:
        self._com_obj.Insert(stream._com_obj)

    @ts_interface
    def remove(self, stream: ExecutionOutputRecordStream) -> None:
        self._com_obj.Remove(stream._com_obj)

    @ts_interface
    def remove_all_streams(self) -> None:
        self._com_obj.RemoveAllStreams()

    @ts_interface
    def set_active_report(self) -> None:
        self._com_obj.SetActiveReport()

    @ts_interface
    def write_record(self, record: typing.Any, mapping: str = "") -> None:
        self._com_obj.WriteRecord(record, str(mapping))

    @ts_interface
    def write_record_from(self, context: typing.Any, record: list[str]) -> None:
        self._com_obj.WriteRecordFrom(context, record)


class ExecutionOutputRecordStreams(COMWrapper):
    @ts_interface
    def begin_next_uut_or_batch(self) -> None:
        self._com_obj.BeginNextUUTOrBatch()

    @ts_interface
    def close_all(self) -> None:
        self._com_obj.CloseAll()

    @ts_interface
    def close_and_remove_stream(self, stream_name: str) -> None:
        self._com_obj.CloseAndRemoveStream(str(stream_name))

    @ts_interface
    def get_stream(self, stream_name: str) -> ExecutionOutputRecordStream:
        return ExecutionOutputRecordStream(
            self._com_obj.GetStream(str(stream_name)),
            self._engine_ref,
        )

    @ts_interface
    def new_stream(self, stream_name: str) -> ExecutionOutputRecordStream:
        return ExecutionOutputRecordStream(
            self._com_obj.NewStream(str(stream_name)),
            self._engine_ref,
        )

    @ts_interface
    def remove_all(self) -> None:
        self._com_obj.RemoveAll()


class CsvFileOutputRecordStream(COMWrapper):
    @property
    @ts_interface
    def auto_flush(self) -> bool:
        return bool(self._com_obj.AutoFlush)

    @auto_flush.setter
    @ts_interface
    def auto_flush(self, value: bool) -> None:
        self._com_obj.AutoFlush = bool(value)

    @property
    @ts_interface
    def path(self) -> str:
        return str(self._com_obj.Path)

    @property
    @ts_interface
    def separator_char(self) -> str:
        return str(self._com_obj.SeparatorChar)

    @separator_char.setter
    @ts_interface
    def separator_char(self, value: str) -> None:
        self._com_obj.SeparatorChar = str(value)

    @ts_interface
    def open(self, absolute_path: str, open_mode: int | FileOpenMode) -> None:
        self._com_obj.Open(str(absolute_path), int(open_mode))

    @ts_interface
    def write_field_headers(self, fields: typing.Any, mapping: str = "") -> None:
        self._com_obj.WriteFieldHeaders(fields, str(mapping))

    @ts_interface
    def write_line(self, line_string: str) -> None:
        self._com_obj.WriteLine(str(line_string))

    @ts_interface
    def write_record_prototype(self, prototype: typing.Any, mapping: str = "") -> None:
        self._com_obj.WriteRecordPrototype(prototype, str(mapping))


CSVFileOutputRecordStream = CsvFileOutputRecordStream
