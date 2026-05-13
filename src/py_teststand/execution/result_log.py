from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.property.property_object import PropertyObject

if TYPE_CHECKING:
    from py_teststand.execution.thread import Thread


class ResultLogRecordType(IntEnum):
    BatchDone = 9
    BatchStart = 3
    Begin = 1
    Deleted = 12
    End = 11
    NotARecordType = 0
    OnTheFlyStepResults = 6
    PostBatch = 10
    PostUUT = 8
    PreBatch = 2
    PreUUT = 4
    UUTDone = 7
    UUTStart = 5


class ResultLog(COMWrapper):
    @ts_interface
    def open(self, path: str) -> None:
        self._com_obj.Open(str(path))

    @ts_interface
    def close(self) -> None:
        self._com_obj.Close()

    @ts_interface
    def read_next_record(self) -> bool:
        return bool(self._com_obj.ReadNextRecord())

    @ts_interface
    def set_report_paths(self, path_string_array: PropertyObject) -> None:
        self._com_obj.SetReportPaths(path_string_array._com_obj)

    @ts_interface
    def get_report_paths(self) -> PropertyObject:
        return PropertyObject(self._com_obj.GetReportPaths(), self._engine_ref)

    @property
    @ts_interface
    def closed_when_written(self) -> bool:
        return bool(self._com_obj.ClosedWhenWritten)

    @property
    @ts_interface
    def file_saved_with_features_toggled(self) -> bool:
        return bool(self._com_obj.FileSavedWithFeaturesToggled)

    @property
    @ts_interface
    def on_the_fly(self) -> bool:
        return bool(self._com_obj.OnTheFly)

    @property
    @ts_interface
    def path(self) -> str:
        return str(self._com_obj.Path)

    @property
    @ts_interface
    def seconds_at_start_in1970_universal_coordinated_time(self) -> float:
        return float(self._com_obj.SecondsAtStartIn1970UniversalCoordinatedTime)

    @property
    @ts_interface
    def simulate_on_the_fly(self) -> bool:
        return bool(self._com_obj.SimulateOnTheFly)

    @simulate_on_the_fly.setter
    @ts_interface
    def simulate_on_the_fly(self, value: bool) -> None:
        self._com_obj.SimulateOnTheFly = bool(value)

    @property
    @ts_interface
    def unique_id(self) -> str:
        return str(self._com_obj.UniqueId)


class ResultLogger(COMWrapper):
    @ts_interface
    def open(self, path: str, is_on_the_fly: bool, log_in_separate_thread: bool) -> None:
        self._com_obj.Open(str(path), bool(is_on_the_fly), bool(log_in_separate_thread))

    @ts_interface
    def close(self) -> None:
        self._com_obj.Close()

    @ts_interface
    def continue_in_new_file(self, path: str) -> None:
        self._com_obj.ContinueInNewFile(str(path))

    @ts_interface
    def deferrable_rename(self, path: str) -> bool:
        return bool(self._com_obj.DeferrableRename(str(path)))

    @ts_interface
    def flush(self) -> None:
        self._com_obj.Flush()

    @ts_interface
    def get_files_written(self, clear: bool) -> PropertyObject:
        return PropertyObject(self._com_obj.GetFilesWritten(bool(clear)), self._engine_ref)

    @ts_interface
    def log_begin(
        self,
        thread: Thread,
        parent_thread: Thread,
        model_thread_type: PropertyObject,
        model_data: PropertyObject,
        process_model_client_path: str,
        number_of_sockets: int,
        socket_index: int,
    ) -> None:
        self._com_obj.LogBegin(
            thread._com_obj,
            parent_thread._com_obj,
            model_thread_type._com_obj,
            model_data._com_obj,
            str(process_model_client_path),
            int(number_of_sockets),
            int(socket_index),
        )

    @ts_interface
    def log_pre_batch(
        self,
        thread: Thread,
        model_thread_type: PropertyObject,
        model_data: PropertyObject,
        process_model_client_path: str,
        start_date: PropertyObject,
        start_time: PropertyObject,
        uut: PropertyObject,
        continue_testing: bool,
    ) -> None:
        self._com_obj.LogPreBatch(
            thread._com_obj,
            model_thread_type._com_obj,
            model_data._com_obj,
            str(process_model_client_path),
            start_date._com_obj,
            start_time._com_obj,
            uut._com_obj,
            bool(continue_testing),
        )

    @ts_interface
    def log_batch_start(
        self,
        thread: Thread,
        model_thread_type: PropertyObject,
        model_data: PropertyObject,
        process_model_client_path: str,
        start_date: PropertyObject,
        start_time: PropertyObject,
        uut: PropertyObject,
    ) -> None:
        self._com_obj.LogBatchStart(
            thread._com_obj,
            model_thread_type._com_obj,
            model_data._com_obj,
            str(process_model_client_path),
            start_date._com_obj,
            start_time._com_obj,
            uut._com_obj,
        )

    @ts_interface
    def log_pre_uut(
        self,
        thread: Thread,
        model_thread_type: PropertyObject,
        model_data: PropertyObject,
        process_model_client_path: str,
        start_date: PropertyObject,
        start_time: PropertyObject,
        uut: PropertyObject,
        continue_testing: bool,
    ) -> None:
        self._com_obj.LogPreUUT(
            thread._com_obj,
            model_thread_type._com_obj,
            model_data._com_obj,
            str(process_model_client_path),
            start_date._com_obj,
            start_time._com_obj,
            uut._com_obj,
            bool(continue_testing),
        )

    @ts_interface
    def log_uut_start(
        self,
        thread: Thread,
        model_thread_type: PropertyObject,
        model_data: PropertyObject,
        process_model_client_path: str,
        start_date: PropertyObject,
        start_time: PropertyObject,
        uut: PropertyObject,
    ) -> None:
        self._com_obj.LogUUTStart(
            thread._com_obj,
            model_thread_type._com_obj,
            model_data._com_obj,
            str(process_model_client_path),
            start_date._com_obj,
            start_time._com_obj,
            uut._com_obj,
        )

    @ts_interface
    def log_on_the_fly_step_results(
        self,
        thread: Thread,
        uut: PropertyObject,
        steps: PropertyObject,
        results: PropertyObject,
        callback_names: PropertyObject,
        parent_ids: PropertyObject,
    ) -> None:
        self._com_obj.LogOnTheFlyStepResults(
            thread._com_obj,
            uut._com_obj,
            steps._com_obj,
            results._com_obj,
            callback_names._com_obj,
            parent_ids._com_obj,
        )

    @ts_interface
    def log_uut_done(
        self,
        thread: Thread,
        model_data: PropertyObject,
        uut: PropertyObject,
        uut_status: str,
        uut_result: PropertyObject,
    ) -> None:
        self._com_obj.LogUUTDone(
            thread._com_obj,
            model_data._com_obj,
            uut._com_obj,
            str(uut_status),
            uut_result._com_obj,
        )

    @ts_interface
    def log_post_uut(
        self,
        thread: Thread,
        model_data: PropertyObject,
        uut: PropertyObject,
        uut_status: str,
    ) -> None:
        self._com_obj.LogPostUUT(
            thread._com_obj,
            model_data._com_obj,
            uut._com_obj,
            str(uut_status),
        )

    @ts_interface
    def log_post_batch(
        self,
        thread: Thread,
        model_data: PropertyObject,
        uut: PropertyObject,
        uut_status: str,
    ) -> None:
        self._com_obj.LogPostBatch(
            thread._com_obj,
            model_data._com_obj,
            uut._com_obj,
            str(uut_status),
        )

    @ts_interface
    def log_batch_done(
        self,
        thread: Thread,
        model_data: PropertyObject,
        uut: PropertyObject,
        uut_status: str,
    ) -> None:
        self._com_obj.LogBatchDone(
            thread._com_obj,
            model_data._com_obj,
            uut._com_obj,
            str(uut_status),
        )

    @ts_interface
    def log_end(self, thread: Thread, model_data: PropertyObject) -> None:
        self._com_obj.LogEnd(thread._com_obj, model_data._com_obj)

    @property
    @ts_interface
    def path(self) -> str:
        return str(self._com_obj.Path)

    @path.setter
    @ts_interface
    def path(self, value: str) -> None:
        self._com_obj.Path = str(value)

    @property
    @ts_interface
    def record_files_written(self) -> bool:
        return bool(self._com_obj.RecordFilesWritten)

    @record_files_written.setter
    @ts_interface
    def record_files_written(self, value: bool) -> None:
        self._com_obj.RecordFilesWritten = bool(value)
