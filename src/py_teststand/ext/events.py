"""Headless delivery of TestStand UI messages.

A sequence tells its host application what is happening by posting UI messages:
progress updates, custom codes above UIMsg_UserMessageBase carrying
numeric/string/object data, and the engine's own lifecycle notifications
(StartExecution, EndExecution, Trace, ...). A GUI receives them through the
TestStand UI controls; a headless host enables
Engine.UIMessagePollingEnabled and polls Engine.GetUIMessage.

UIMessageHandler wraps that polling. All processing happens on the thread that
owns the engine: the engine is apartment-threaded, so a COM call made from
another thread is serviced by the owning thread's message pump, and a host
whose main thread blocks inside an engine call while a worker polls deadlocks.
Drive the handler from the engine thread instead, either by calling
process_pending() inside your own loop or by letting wait_for_execution() run
the loop for you.

Every message is acknowledged after its callbacks run. Acknowledging is what
unblocks the sequence thread when a message was posted synchronously, so a
host that stops draining the queue hangs synchronous posters.
"""

from __future__ import annotations

import threading
import time
import typing
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    import pythoncom
else:
    try:
        import pythoncom
    except ImportError:
        pythoncom = None

import logging

from py_teststand.messaging.ui_message import UIMessage, UIMessageCode

logger = logging.getLogger(__name__)

Callback = Callable[[UIMessage], None]


class UIMessageHandler:
    """Drains the engine's UI-message queue and dispatches messages to callbacks.

    Use it from the thread that created the engine:

        handler = engine.ui_handler
        handler.on(my_code, my_callback)
        with engine.new_execution(sequence_file, "MainSequence") as execution:
            handler.wait_for_execution(execution)

    Callbacks run on the calling thread, in arrival order. The COM message is
    only valid until it is acknowledged (which happens right after the
    callbacks return), so read the data you need inside the callback instead
    of storing the message object.
    """

    def __init__(self, engine: typing.Any):
        self._engine_wrapper = engine
        self._callbacks: dict[int, list[Callback]] = {}
        self._global_callbacks: list[Callback] = []
        self._callbacks_lock = threading.Lock()
        self._polling_enabled = False

    def on(self, event_code: int, callback: Callback | None = None) -> typing.Any:
        """Register a callback for one event code (UIMessageCode or a custom code).

        Usable directly (``handler.on(code, callback)``) or as a decorator::

            @handler.on(UIMessageCode.UserMessageBase + 1)
            def on_stage(message): ...
        """
        if callback is None:

            def register(decorated: Callback) -> Callback:
                self.on(event_code, decorated)
                return decorated

            return register
        with self._callbacks_lock:
            self._callbacks.setdefault(int(event_code), []).append(callback)
        return callback

    def off(self, event_code: int, callback: Callback) -> bool:
        """Unregister a callback; True if it was registered."""
        with self._callbacks_lock:
            try:
                self._callbacks.get(int(event_code), []).remove(callback)
            except ValueError:
                return False
            return True

    def on_all(self, callback: Callback) -> None:
        """Register a callback that receives every message."""
        with self._callbacks_lock:
            self._global_callbacks.append(callback)

    def handle_execution(self, execution_id: int, on_complete: Callable[[], None]) -> None:
        """Invoke on_complete when the execution with the given id ends."""

        def _check_exec(msg: UIMessage) -> None:
            if msg.execution and msg.execution.id == execution_id:
                on_complete()

        self.on(UIMessageCode.EndExecution, _check_exec)

    def start(self) -> None:
        """Enable UI-message polling on the engine (idempotent)."""
        if not self._polling_enabled:
            self._engine_wrapper.ui_message_polling_enabled = True
            self._polling_enabled = True

    def stop(self) -> None:
        """Drop registered callbacks. The engine keeps queueing until shutdown."""
        with self._callbacks_lock:
            self._callbacks.clear()
            self._global_callbacks.clear()

    def process_pending(self) -> int:
        """Dispatch and acknowledge every queued message; return how many."""
        self.start()
        handled = 0
        for message in self._pending_messages():
            self._dispatch(message)
            handled += 1
        return handled

    def messages(
        self,
        execution: typing.Any,
        timeout_seconds: float | None = None,
        poll_interval: float = 0.01,
    ) -> typing.Iterator[UIMessage]:
        """Yield each UI message while the execution runs (pull-style alternative
        to callbacks)::

            for message in engine.ui_handler.messages(execution):
                print(message.event, message.string_data)

        Each message is acknowledged after your loop body finishes with it, so
        read the data inside the loop instead of storing the message. Iteration
        ends when the execution ends (after a final drain of the queue) or when
        the timeout elapses.
        """
        self.start()
        deadline = None if timeout_seconds is None else time.monotonic() + timeout_seconds
        while True:
            if pythoncom is not None:
                pythoncom.PumpWaitingMessages()
            yield from self._acknowledged(self._pending_messages())
            if execution.wait_for_end_ex(0):
                yield from self._acknowledged(self._pending_messages())
                return
            if deadline is not None and time.monotonic() > deadline:
                return
            time.sleep(poll_interval)

    def _pending_messages(self) -> typing.Iterator[UIMessage]:
        """Pop messages off the engine queue until it reports empty."""
        while not self._engine_wrapper.is_ui_message_queue_empty:
            message = self._engine_wrapper.get_ui_message()
            if message is None:
                return
            yield message

    def _acknowledged(self, pending: typing.Iterator[UIMessage]) -> typing.Iterator[UIMessage]:
        """Yield each message, acknowledging it once the consumer is done with it."""
        for message in pending:
            try:
                yield message
            finally:
                try:
                    message.acknowledge()
                except Exception:
                    logger.exception("Failed to acknowledge UI message")

    def wait_for_execution(
        self,
        execution: typing.Any,
        timeout_seconds: float | None = None,
        poll_interval: float = 0.01,
    ) -> bool:
        """Pump messages until the execution ends; True if it ended in time.

        Drains the queue once more after the execution ends, so messages
        posted by the final steps still reach their callbacks.
        """
        self.start()
        deadline = None if timeout_seconds is None else time.monotonic() + timeout_seconds
        while True:
            if pythoncom is not None:
                pythoncom.PumpWaitingMessages()
            self.process_pending()
            if execution.wait_for_end_ex(0):
                self.process_pending()
                return True
            if deadline is not None and time.monotonic() > deadline:
                return False
            time.sleep(poll_interval)

    def _dispatch(self, message: UIMessage) -> None:
        """Run the callbacks for one message, then acknowledge it.

        Acknowledge runs even when a callback raises: a synchronous poster
        stays blocked until the message is acknowledged.
        """
        try:
            self._run_callbacks(message)
        finally:
            try:
                message.acknowledge()
            except Exception:
                logger.exception("Failed to acknowledge UI message")

    def _run_callbacks(self, message: UIMessage) -> None:
        code = int(message.event)
        with self._callbacks_lock:
            callbacks = list(self._callbacks.get(code, [])) + list(self._global_callbacks)
        for callback in callbacks:
            try:
                callback(message)
            except Exception:
                logger.exception("Error in UI message callback for event %s", code)
