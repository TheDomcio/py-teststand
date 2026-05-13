from __future__ import annotations

import logging
import queue
import threading
import time
import typing
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    import pythoncom
    import win32com.client
else:
    try:
        import pythoncom
        import win32com.client
    except ImportError:
        pythoncom = None
        win32com = None

from py_teststand.messaging.ui_message import UIMessage, UIMessageCode

logger = logging.getLogger(__name__)

Callback = Callable[[UIMessage], None]


class UIMessageHandler:
    def __init__(self, engine: typing.Any):
        self._engine_wrapper = engine
        self._callbacks: dict[int, list[Callback]] = {}
        self._global_callbacks: list[Callback] = []
        self._callbacks_lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._queue: queue.Queue = queue.Queue()
        self._executor: ThreadPoolExecutor | None = None
        self._worker_thread: threading.Thread | None = None

        self._trace_count = 0
        self._trace_window_start = 0.0
        self._last_trace_msg: UIMessage | None = None
        self._trace_lock = threading.Lock()

    def on(self, event_code: int, callback: Callback) -> None:
        with self._callbacks_lock:
            if event_code not in self._callbacks:
                self._callbacks[event_code] = []
            self._callbacks[event_code].append(callback)

    def on_all(self, callback: Callback) -> None:
        with self._callbacks_lock:
            self._global_callbacks.append(callback)

    def handle_execution(self, execution_id: int, on_complete: Callable[[], None]) -> None:
        def _check_exec(msg: UIMessage) -> None:
            if msg.execution and msg.execution.id == execution_id:
                if msg.event == UIMessageCode.EndExecution:
                    on_complete()

        self.on(UIMessageCode.EndExecution, _check_exec)

    def _dispatch(self, message_com: typing.Any) -> None:
        msg = UIMessage(message_com, self._engine_wrapper._engine_ref)

        if msg.event == UIMessageCode.Trace:
            with self._trace_lock:
                now = time.time()
                if now - self._trace_window_start > 0.1:
                    self._trace_window_start = now
                    self._trace_count = 0

                self._trace_count += 1
                if self._trace_count > 50:
                    self._last_trace_msg = msg
                    return

                self._last_trace_msg = msg

        self._queue.put(msg)

    def _process_queue(self) -> None:
        while not self._stop_event.is_set():
            try:
                msg = self._queue.get(timeout=0.1)
            except queue.Empty:
                continue

            if self._executor:
                self._executor.submit(self._execute_callbacks, msg)
            self._queue.task_done()

    def _execute_callbacks(self, msg: UIMessage) -> None:
        code = msg.event

        with self._callbacks_lock:
            per_code = list(self._callbacks.get(code, []))
            global_cbs = list(self._global_callbacks)

        for cb in per_code:
            try:
                cb(msg)
            except Exception:
                logger.exception("Error executing UI message callback")

        for cb in global_cbs:
            try:
                cb(msg)
            except Exception:
                logger.exception("Error executing UI message callback")

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return

        self._stop_event.clear()
        self._executor = ThreadPoolExecutor(max_workers=4)

        self._worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self._worker_thread.start()

        raw_engine = self._engine_wrapper._com_obj
        is_live_com = pythoncom is not None and "Mock" not in str(type(raw_engine))

        if is_live_com:
            stream_id = pythoncom.CoMarshalInterThreadInterfaceInStream(
                pythoncom.IID_IDispatch, raw_engine
            )
        else:
            stream_id = raw_engine

        self._thread = threading.Thread(
            target=self._run_pump, args=(stream_id, is_live_com), daemon=True
        )
        self._thread.start()

    def _run_pump(self, stream_id: typing.Any, is_live_com: bool) -> None:
        if pythoncom is None:
            while not self._stop_event.wait(0.01):
                pass
            return
        pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)
        try:
            if is_live_com:
                raw_engine = pythoncom.CoGetInterfaceAndReleaseStream(
                    stream_id, pythoncom.IID_IDispatch
                )
                engine_dispatch = win32com.client.Dispatch(raw_engine)
            else:
                engine_dispatch = stream_id

            class _EngineSink:
                def OnUIMessage(self, message: typing.Any) -> None:  # noqa: N802
                    if hasattr(self, "handler"):
                        typing.cast(typing.Any, self.handler)._dispatch(message)

                def OnEvent(self, message: typing.Any) -> None:  # noqa: N802
                    if hasattr(self, "handler"):
                        typing.cast(typing.Any, self.handler)._dispatch(message)

            if is_live_com:
                try:
                    connected = False
                    try:
                        sink = win32com.client.WithEvents(engine_dispatch, _EngineSink)
                        sink.handler = self
                        connected = True
                    except Exception:
                        pass

                    if not connected:
                        try:
                            if hasattr(engine_dispatch, "UIMessageEvent"):
                                sink = win32com.client.WithEvents(
                                    engine_dispatch.UIMessageEvent, _EngineSink
                                )
                                sink.handler = self
                        except Exception:
                            pass

                    if not connected:
                        logger.error("Could not connect to any TestStand engine events.")
                except Exception as e:
                    logger.error(f"Failed to connect events: {e}")

            while not self._stop_event.is_set():
                if is_live_com:
                    pythoncom.PumpWaitingMessages()

                    try:
                        while True:
                            msg_com = engine_dispatch.GetUIMessage()
                            if not msg_com:
                                break
                            self._dispatch(msg_com)
                    except Exception:
                        pass

                if self._stop_event.wait(0.01):
                    break
        finally:
            pythoncom.CoUninitialize()

    def stop(self) -> None:
        self._stop_event.set()

        if self._thread:
            self._thread.join(timeout=1.0)

        if self._worker_thread:
            try:
                self._queue.join()
            except Exception:
                pass
            self._worker_thread.join(timeout=1.0)

        if self._executor:
            self._executor.shutdown(wait=True)
            self._executor = None
