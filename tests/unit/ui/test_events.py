from __future__ import annotations

import time
from unittest.mock import MagicMock, patch

from py_teststand.ext.events import UIMessageHandler
from py_teststand.messaging.ui_message import UIMessage


class MockUIMsg:
    def __init__(self, event):

        self.Event = event

        self.Execution = None

        self.Thread = None

        self.ActiveXControl = None

        self.UserParameter = None

    def AsPropertyObject(self):  # noqa: N802

        return MagicMock()




def test_ui_message_handler_dispatch():

    handler = UIMessageHandler(MagicMock())

    calls = []

    def my_cb(msg):

        calls.append(msg.event)

    handler.on(100, my_cb)

    handler._execute_callbacks(UIMessage(MockUIMsg(100)))

    assert len(calls) == 1

    assert calls[0] == 100

    global_calls = []

    handler.on_all(lambda msg: global_calls.append(msg.event))

    handler._execute_callbacks(UIMessage(MockUIMsg(200)))

    assert len(global_calls) == 1

    assert global_calls[0] == 200

    assert len(calls) == 1


def test_ui_message_handler_non_blocking_processing():

    with patch("win32com.client.WithEvents"), patch("pythoncom.CoInitializeEx"):
        handler = UIMessageHandler(MagicMock())

        calls = []

        def slow_cb(msg):

            time.sleep(0.1)

            calls.append(msg.event)

        handler.on(1, slow_cb)

        handler.start()

        try:
            handler._dispatch(MockUIMsg(1))

            assert len(calls) == 0

            for _ in range(20):
                if len(calls) == 1:
                    break

                time.sleep(0.05)

            assert len(calls) == 1

            assert calls[0] == 1

        finally:
            handler.stop()


def test_ui_message_handler_queue_ordering():

    with patch("win32com.client.WithEvents"), patch("pythoncom.CoInitializeEx"):
        handler = UIMessageHandler(MagicMock())

        calls = []

        def cb(msg):

            calls.append(msg.event)

        handler.on_all(cb)

        handler.start()

        try:
            for i in range(10):
                handler._dispatch(MockUIMsg(i))

            time.sleep(0.5)

            assert len(calls) == 10

        finally:
            handler.stop()


def test_ui_message_handler_stop_cleans_up():

    with patch("win32com.client.WithEvents"), patch("pythoncom.CoInitializeEx"):
        handler = UIMessageHandler(MagicMock())

        handler.start()

        assert handler._executor is not None

        assert handler._worker_thread is not None

        assert handler._worker_thread.is_alive()

        handler.stop()

        assert handler._executor is None

        assert handler._stop_event.is_set()
