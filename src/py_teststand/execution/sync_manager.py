from __future__ import annotations

import typing
from enum import IntEnum
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COMWrapper, ts_interface

if TYPE_CHECKING:
    from py_teststand.core.engine import Engine
    from py_teststand.execution.thread import Thread
    from py_teststand.messaging.output_message import OutputMessage


class BatchSynchronization(IntEnum):
    UseSeqFileSetting = 0
    UseModelSetting = 1
    NoSync = 2
    Serial = 3
    Parallel = 4
    OneThreadOnly = 5


class BatchSyncType(IntEnum):
    NoneValue = 0
    Serial = 1
    Parallel = 2
    OneThreadOnly = 3


class EnqueueResult(IntEnum):
    Enqueued = 0
    DiscardedElement = 1
    NotEnqueued = 2


class SyncObjType(IntEnum):
    NotASyncObj = 0
    Semaphore = 1
    Mutex = 2
    Rendezvous = 3
    Queue = 4
    Notification = 5
    Batch = 6


class SyncState(IntEnum):
    NoneValue = 0
    Blocked = 1
    InUse = 2
    Aborted = 3
    TimedOut = 4


class WaitResult(IntEnum):
    Success = 0
    TimeoutOccurred = 1
    TerminateOrAbortOccurred = 2
    DeadlockDetected = 3


class FullQueueOption(IntEnum):
    Wait = 0
    DiscardFrontElement = 1
    DiscardBackElement = 2
    DoNotEnqueue = 3


class AutoReleaser(COMWrapper):
    @ts_interface
    def early_release(self) -> None:
        self._com_obj.EarlyRelease()

    @ts_interface
    def early_release_ex(self, sequence_context: typing.Any = None) -> typing.Any:
        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        self._com_obj.EarlyReleaseEx(com_context)

    def __enter__(self) -> AutoReleaser:

        return self

    def __exit__(self, exc_type: typing.Any, exc_val: typing.Any, exc_tb: typing.Any) -> None:

        self.early_release()

    @ts_interface
    def release_pending(self) -> bool:
        return bool(self._com_obj.ReleasePending())

    @ts_interface
    def set_releaser_thread_id(self, thread_id: str) -> None:
        self._com_obj.SetReleaserThreadId(thread_id)


class SyncObject(COMWrapper):
    @property
    @ts_interface
    def name(self) -> str:
        return str(self._com_obj.Name)


class Mutex(SyncObject):
    @ts_interface
    def lock_mutex(
        self,
        thread_id: str,
        thread_display_name: str,
        home_sync_mgr: SyncManager,
        timeout_in_seconds: float,
        sequence_context: typing.Any = None,
        process_msgs: bool = False,
        is_part_of_group_lock: bool = False,
    ) -> tuple[AutoReleaser, WaitResult, str]:

        raw_mgr = home_sync_mgr._com_obj
        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        res = self._com_obj.LockMutex(
            thread_id,
            thread_display_name,
            raw_mgr,
            timeout_in_seconds,
            com_context,
            process_msgs,
            is_part_of_group_lock,
        )
        return AutoReleaser(res[0], self._engine_ref), WaitResult(res[1]), str(res[2])

    @ts_interface
    def lock_mutex_group(
        self,
        mutex_array: list[Mutex],
        thread_id: str,
        thread_display_name: str,
        home_sync_mgr: SyncManager,
        timeout_in_seconds: float,
        sequence_context: typing.Any = None,
        process_msgs: bool = False,
    ) -> tuple[list[AutoReleaser], WaitResult, str]:

        raw_mutexes = [m._com_obj for m in mutex_array]
        raw_mgr = home_sync_mgr._com_obj
        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        res = self._com_obj.LockMutexGroup(
            raw_mutexes,
            thread_id,
            thread_display_name,
            raw_mgr,
            timeout_in_seconds,
            com_context,
            process_msgs,
        )
        releasers = [AutoReleaser(com, self._engine_ref) for com in res[0]]
        return releasers, WaitResult(res[1]), str(res[2])

    @ts_interface
    def early_unlock_mutex(self, thread_id: str) -> None:
        self._com_obj.EarlyUnlockMutex(thread_id)

    @ts_interface
    def early_unlock_mutex_ex(
        self, sequence_context: typing.Any = None, thread_id: str = ""
    ) -> None:
        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        self._com_obj.EarlyUnlockMutexEx(com_context, thread_id)

    @ts_interface
    def get_saved_owner_info(self) -> typing.Any:
        res = self._com_obj.GetSavedOwnerInfo()
        return str(res[0]), str(res[1]), SyncManager(res[2], self._engine_ref)

    @ts_interface
    def finalize_for_group_lock(self, home_sync_mgr: SyncManager) -> None:
        self._com_obj.FinalizeForGroupLock(home_sync_mgr._com_obj)

    @ts_interface
    def get_info(self) -> typing.Any:
        return int(self._com_obj.GetInfo())

    @ts_interface
    def get_info_ex(self) -> typing.Any:
        res = self._com_obj.GetInfoEx()
        return int(res[0]), int(res[1]), str(res[2])


class Semaphore(SyncObject):
    @ts_interface
    def acquire_semaphore(
        self,
        timeout_in_seconds: float,
        sequence_context: typing.Any,
        process_msgs: bool,
    ) -> WaitResult:

        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        return WaitResult(
            self._com_obj.AcquireSemaphore(timeout_in_seconds, com_context, process_msgs)
        )

    @ts_interface
    def acquire_semaphore_with_auto_releaser(
        self,
        timeout_in_seconds: float,
        sequence_context: typing.Any,
        process_msgs: bool,
    ) -> tuple[AutoReleaser, WaitResult]:

        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        res = self._com_obj.AcquireSemaphoreWithAutoReleaser(
            timeout_in_seconds, com_context, process_msgs
        )
        return AutoReleaser(res[0], self._engine_ref), WaitResult(res[1])

    @ts_interface
    def get_info(self) -> typing.Any:
        res = self._com_obj.GetInfo()
        return int(res[0]), int(res[1]), int(res[2]), int(res[3])

    @ts_interface
    def release_semaphore(self) -> None:
        self._com_obj.ReleaseSemaphore()

    @ts_interface
    def release_semaphore_ex(
        self, sequence_context: typing.Any = None, thread_id: str = ""
    ) -> None:
        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        self._com_obj.ReleaseSemaphoreEx(com_context, thread_id)


class Batch(SyncObject):
    @property
    @ts_interface
    def default_batch_synchronization(self) -> typing.Any:

        return BatchSyncType(self._com_obj.DefaultBatchSynchronization)

    @default_batch_synchronization.setter
    @ts_interface
    def default_batch_synchronization(self, value: int | BatchSyncType) -> None:
        self._com_obj.DefaultBatchSynchronization = int(value)

    @ts_interface
    def add_thread(self, engine: Engine, thread: Thread, order_number: int) -> typing.Any:
        self._com_obj.AddThread(engine._com_obj, thread._com_obj, order_number)

    @ts_interface
    def remove_thread(self, engine: Engine, thread: Thread) -> typing.Any:
        self._com_obj.RemoveThread(engine._com_obj, thread._com_obj)

    @ts_interface
    def get_batch_threads(self) -> list[Thread]:
        from py_teststand.execution.thread import Thread

        com_threads = self._com_obj.GetBatchThreads()
        return [Thread(t, self._engine_ref) for t in com_threads]

    @ts_interface
    def get_info(self) -> typing.Any:
        res = self._com_obj.GetInfo()
        return int(res[0]), int(res[1])

    @ts_interface
    def enter_synchronized_section(
        self,
        section_name: str,
        batch_sync_type: int,
        timeout_in_seconds: float,
        sequence_context: typing.Any = None,
        process_msgs: bool = False,
    ) -> tuple[WaitResult, bool]:

        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        res = self._com_obj.EnterSynchronizedSection(
            section_name, batch_sync_type, timeout_in_seconds, com_context, process_msgs
        )
        return WaitResult(res[0]), bool(res[1])

    @ts_interface
    def exit_synchronized_section(
        self,
        section_name: str,
        timeout_in_seconds: float,
        sequence_context: typing.Any = None,
        process_msgs: bool = False,
        rte_occurred: bool = False,
    ) -> WaitResult:

        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        return WaitResult(
            self._com_obj.ExitSynchronizedSection(
                section_name, timeout_in_seconds, com_context, process_msgs, rte_occurred
            )
        )

    @ts_interface
    def exit_all_synchronized_sections_in_current_sequence(
        self,
        timeout_in_seconds: float,
        sequence_context: typing.Any = None,
        process_msgs: bool = False,
        rte_occurred: bool = False,
    ) -> WaitResult:

        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        return WaitResult(
            self._com_obj.ExitAllSynchronizedSectionsInCurrentSequence(
                timeout_in_seconds, com_context, process_msgs, rte_occurred
            )
        )

    @ts_interface
    def report_rte_occurred(self, sequence_context: typing.Any = None) -> None:
        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        self._com_obj.ReportRTEOccurred(com_context)


class Notification(SyncObject):
    @ts_interface
    def set(self, data_prop_obj: typing.Any = None, by_ref: bool = False) -> typing.Any:
        raw_data = getattr(data_prop_obj, "_com_obj", data_prop_obj)
        self._com_obj.Set(raw_data, by_ref)

    @ts_interface
    def set_ex(
        self,
        sequence_context: typing.Any = None,
        data_prop_obj: typing.Any = None,
        by_ref: bool = False,
        auto_clear: bool = False,
    ) -> None:
        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        raw_data = getattr(data_prop_obj, "_com_obj", data_prop_obj)
        self._com_obj.SetEx(com_context, raw_data, by_ref, auto_clear)

    @ts_interface
    def pulse(self, data_prop_obj: typing.Any = None, by_ref: bool = False) -> typing.Any:
        raw_data = getattr(data_prop_obj, "_com_obj", data_prop_obj)
        self._com_obj.Pulse(raw_data, by_ref)

    @ts_interface
    def pulse_ex(
        self,
        sequence_context: typing.Any = None,
        data_prop_obj: typing.Any = None,
        by_ref: bool = False,
        apply_to_all_waiters: bool = False,
    ) -> None:
        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        raw_data = getattr(data_prop_obj, "_com_obj", data_prop_obj)
        self._com_obj.PulseEx(com_context, raw_data, by_ref, apply_to_all_waiters)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def clear_ex(self, sequence_context: typing.Any = None) -> typing.Any:
        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        self._com_obj.ClearEx(com_context)

    @ts_interface
    def get_info(self) -> typing.Any:
        res = self._com_obj.GetInfo()
        return int(res[0]), bool(res[1])

    @ts_interface
    def wait(
        self,
        destination_prop_obj: typing.Any = None,
        timeout_in_seconds: float = -1.0,
        sequence_context: typing.Any = None,
        process_msgs: bool = False,
    ) -> tuple[typing.Any, WaitResult]:

        raw_dest = getattr(destination_prop_obj, "_com_obj", destination_prop_obj)
        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        res = self._com_obj.Wait(raw_dest, timeout_in_seconds, com_context, process_msgs)
        return res[0], WaitResult(res[1])

    @ts_interface
    def wait_multiple(
        self,
        notifications: list[Notification],
        wait_all: bool,
        timeout_in_seconds: float,
        sequence_context: typing.Any = None,
        process_msgs: bool = False,
    ) -> tuple[int, WaitResult]:

        raw_notifications = [n._com_obj for n in notifications]
        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        res = self._com_obj.WaitMultiple(
            raw_notifications, wait_all, timeout_in_seconds, com_context, process_msgs
        )
        return int(res[0]), WaitResult(res[1])

    @ts_interface
    def begin_wait_for_multi_wait(
        self,
        notification_count: int,
        sequence_context: typing.Any = None,
    ) -> None:
        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        self._com_obj.BeginWaitForMultiWait(notification_count, com_context)

    @ts_interface
    def do_wait_for_multi_wait(
        self,
        notifications: list[Notification],
        wait_all: bool,
        timeout_in_seconds: float,
        sequence_context: typing.Any = None,
        process_msgs: bool = False,
    ) -> tuple[int, WaitResult]:

        raw_notifications = [n._com_obj for n in notifications]
        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        res = self._com_obj.DoWaitForMultiWait(
            raw_notifications, wait_all, timeout_in_seconds, com_context, process_msgs
        )
        return int(res[0]), WaitResult(res[1])

    @ts_interface
    def end_wait_for_multi_wait(self, wait_succeeded: bool) -> None:
        self._com_obj.EndWaitForMultiWait(wait_succeeded)


class Rendezvous(SyncObject):
    @ts_interface
    def get_info(self) -> typing.Any:
        res = self._com_obj.GetInfo()
        return int(res[0]), int(res[1])

    @ts_interface
    def rendezvous(
        self,
        timeout_in_seconds: float,
        sequence_context: typing.Any = None,
        process_msgs: bool = False,
    ) -> tuple[int, WaitResult]:

        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        res = self._com_obj.Rendezvous(timeout_in_seconds, com_context, process_msgs)
        return int(res[0]), WaitResult(res[1])


class Queue(SyncObject):
    @ts_interface
    def enqueue(
        self,
        data_prop_obj: typing.Any,
        enqueue_location: int,
        timeout_in_seconds: float,
        sequence_context: typing.Any = None,
        process_msgs: bool = False,
    ) -> tuple[EnqueueResult, int]:

        raw_data = getattr(data_prop_obj, "_com_obj", data_prop_obj)
        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        res = self._com_obj.Enqueue(
            raw_data, enqueue_location, timeout_in_seconds, com_context, process_msgs
        )
        return EnqueueResult(res[0]), int(res[1])

    @ts_interface
    def dequeue(
        self,
        destination_prop_obj: typing.Any,
        timeout_in_seconds: float,
        sequence_context: typing.Any = None,
        process_msgs: bool = False,
    ) -> tuple[typing.Any, WaitResult, int]:

        raw_dest = getattr(destination_prop_obj, "_com_obj", destination_prop_obj)
        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        res = self._com_obj.Dequeue(raw_dest, timeout_in_seconds, com_context, process_msgs)
        return res[0], WaitResult(res[1]), int(res[2])

    @ts_interface
    def dequeue_multiple(
        self,
        destination_prop_objs: list[typing.Any],
        timeout_in_seconds: float,
        sequence_context: typing.Any = None,
        process_msgs: bool = False,
    ) -> tuple[list[typing.Any], WaitResult]:

        raw_dests = [getattr(p, "_com_obj", p) for p in destination_prop_objs]
        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        res = self._com_obj.DequeueMultiple(
            raw_dests, timeout_in_seconds, com_context, process_msgs
        )
        return list(res[0]), WaitResult(res[1])

    @ts_interface
    def flush(self, sequence_context: typing.Any = None) -> typing.Any:
        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        return list(self._com_obj.Flush(com_context))

    @ts_interface
    def get_info(self) -> typing.Any:
        res = self._com_obj.GetInfo()
        return int(res[0]), int(res[1]), int(res[2])

    @ts_interface
    def begin_dequeue_for_multi_dequeue(
        self,
        dequeue_count: int,
        sequence_context: typing.Any = None,
    ) -> None:
        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        self._com_obj.BeginDequeueForMultiDequeue(dequeue_count, com_context)

    @ts_interface
    def do_dequeue_for_multi_dequeue(
        self,
        destination_prop_objs: list[typing.Any],
        timeout_in_seconds: float,
        sequence_context: typing.Any = None,
        process_msgs: bool = False,
    ) -> tuple[list[typing.Any], WaitResult]:

        raw_dests = [getattr(p, "_com_obj", p) for p in destination_prop_objs]
        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        res = self._com_obj.DoDequeueForMultiDequeue(
            raw_dests, timeout_in_seconds, com_context, process_msgs
        )
        return list(res[0]), WaitResult(res[1])

    @ts_interface
    def end_dequeue_for_multi_dequeue(self, wait_succeeded: bool) -> None:
        self._com_obj.EndDequeueForMultiDequeue(wait_succeeded)


class SyncManager(COMWrapper):
    @ts_interface
    def create_mutex(self, name: str) -> typing.Any:
        res = self._com_obj.CreateMutex(name)
        if isinstance(res, (list, tuple)):
            return Mutex(res[0], self._engine_ref), bool(res[1])
        return Mutex(res, self._engine_ref), False

    @ts_interface
    def create_semaphore(
        self, name: str, initial_count: int = 1, max_count: int = 1
    ) -> tuple[Semaphore, bool]:
        res = self._com_obj.CreateSemaphore(name, initial_count, max_count)
        if isinstance(res, (list, tuple)):
            return Semaphore(res[0], self._engine_ref), bool(res[1])
        return Semaphore(res, self._engine_ref), False

    @ts_interface
    def create_batch(self, name: str) -> typing.Any:
        res = self._com_obj.CreateBatch(name)
        if isinstance(res, (list, tuple)):
            return Batch(res[0], self._engine_ref), bool(res[1])
        return Batch(res, self._engine_ref), False

    @ts_interface
    def create_notification(self, name: str) -> typing.Any:
        res = self._com_obj.CreateNotification(name)
        if isinstance(res, (list, tuple)):
            return Notification(res[0], self._engine_ref), bool(res[1])
        return Notification(res, self._engine_ref), False

    @ts_interface
    def create_queue(self, name: str, size_limit: int = 0) -> typing.Any:
        res = self._com_obj.CreateQueue(name, size_limit)
        if isinstance(res, (list, tuple)):
            return Queue(res[0], self._engine_ref), bool(res[1])
        return Queue(res, self._engine_ref), False

    @ts_interface
    def create_rendezvous(self, name: str, rendezvous_count: int = 1) -> typing.Any:
        res = self._com_obj.CreateRendezvous(name, rendezvous_count)
        if isinstance(res, (list, tuple)):
            return Rendezvous(res[0], self._engine_ref), bool(res[1])
        return Rendezvous(res, self._engine_ref), False

    @ts_interface
    def get_mutex(self, name: str) -> typing.Any:
        return Mutex(self._com_obj.GetMutex(name), self._engine_ref)

    @ts_interface
    def get_semaphore(self, name: str) -> typing.Any:
        return Semaphore(self._com_obj.GetSemaphore(name), self._engine_ref)

    @ts_interface
    def get_batch(self, name: str) -> typing.Any:
        return Batch(self._com_obj.GetBatch(name), self._engine_ref)

    @ts_interface
    def get_notification(self, name: str) -> typing.Any:
        return Notification(self._com_obj.GetNotification(name), self._engine_ref)

    @ts_interface
    def get_queue(self, name: str) -> typing.Any:
        return Queue(self._com_obj.GetQueue(name), self._engine_ref)

    @ts_interface
    def get_rendezvous(self, name: str) -> typing.Any:
        return Rendezvous(self._com_obj.GetRendezvous(name), self._engine_ref)

    @property
    @ts_interface
    def logging_enabled(self) -> bool:
        return bool(self._com_obj.LoggingEnabled)

    @property
    @ts_interface
    def logging_output_message_category_name(self) -> str:
        return str(self._com_obj.LoggingOutputMessageCategoryName)

    @property
    @ts_interface
    def machine_id(self) -> str:
        return str(self._com_obj.MachineID)

    @property
    @ts_interface
    def process_id(self) -> int:
        return int(self._com_obj.ProcessID)

    @ts_interface
    def begin_logging(self) -> int:
        return int(self._com_obj.BeginLogging())

    @ts_interface
    def end_logging(self) -> int:
        return int(self._com_obj.EndLogging())

    @ts_interface
    def is_alive(self) -> bool:
        return bool(self._com_obj.IsAlive())

    @ts_interface
    def log_action(
        self,
        synchronization_mechanism: str,
        sequence_context: typing.Any,
        thread_id: str,
        thread_display_name: str,
        resource_name: str,
        sync_state: int,
        operation: str,
        timeout: float,
        post_message: bool,
        reserved: typing.Any = None,
    ) -> OutputMessage | None:
        from py_teststand.messaging.output_message import OutputMessage

        com_context = getattr(sequence_context, "_com_obj", sequence_context)
        res = self._com_obj.LogAction(
            synchronization_mechanism,
            com_context,
            thread_id,
            thread_display_name,
            resource_name,
            sync_state,
            operation,
            timeout,
            post_message,
            reserved,
        )
        return OutputMessage(res, self._engine_ref) if res else None

    @ts_interface
    def release_server_on_destruct(self, server_to_release: typing.Any) -> None:
        self._com_obj.ReleaseServerOnDestruct(server_to_release)

    @ts_interface
    def get_sync_object(self, name: str, sync_obj_type: int) -> typing.Any:
        res = self._com_obj.GetSyncObject(name, sync_obj_type)
        if res is None:
            return None

        if sync_obj_type == SyncObjType.Mutex:
            return Mutex(res, self._engine_ref)
        elif sync_obj_type == SyncObjType.Semaphore:
            return Semaphore(res, self._engine_ref)
        elif sync_obj_type == SyncObjType.Queue:
            return Queue(res, self._engine_ref)
        elif sync_obj_type == SyncObjType.Notification:
            return Notification(res, self._engine_ref)
        elif sync_obj_type == SyncObjType.Rendezvous:
            return Rendezvous(res, self._engine_ref)
        elif sync_obj_type == SyncObjType.Batch:
            return Batch(res, self._engine_ref)

        return SyncObject(res, self._engine_ref)

    @ts_interface
    def get_mutex_owner_info(self, mutex_name: str) -> typing.Any:
        res = self._com_obj.GetMutexOwnerInfo(mutex_name)
        return str(res[0]), str(res[1]), SyncManager(res[2], self._engine_ref)

    @ts_interface
    def get_lock_mutex_thread_is_waiting_for(self, thread_id: str) -> typing.Any:
        res = self._com_obj.GetLockMutexThreadIsWaitingFor(thread_id)
        return str(res[0]), SyncManager(res[1], self._engine_ref)

    @ts_interface
    def record_thread_waiting_for_lock_mutex(
        self, thread_id: str, thread_display_name: str, mutex_name: str, mutex_sync_mgr: SyncManager
    ) -> None:
        self._com_obj.RecordThreadWaitingForLockMutex(
            thread_id, thread_display_name, mutex_name, mutex_sync_mgr._com_obj
        )

    @ts_interface
    def record_thread_nolonger_waiting_for_lock_mutex(self, thread_id: str) -> None:
        self._com_obj.RecordThreadNolongerWaitingForLockMutex(thread_id)
