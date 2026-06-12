"""Contract tests for the headless UI-message handler.

Pin the dispatch behavior a headless host depends on: callbacks routed by event
code, global callbacks seeing everything, every message acknowledged exactly
once after its callbacks run (a synchronous poster stays blocked until then),
acknowledgement surviving a raising callback, arrival-order dispatch, queue
draining via process_pending, and wait_for_execution pumping until the
execution ends. A mock engine stands in for COM, so these run with no
TestStand installed.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from py_teststand.ext.events import UIMessageHandler
from py_teststand.messaging.ui_message import UIMessage, UIMessageCode


class MockUIMsg:
    def __init__(self, event, execution=None):
        self.Event = event
        self.Execution = execution
        self.Thread = None
        self.NumericData = 0.0
        self.StringData = ""
        self.acknowledge_count = 0

    def Acknowledge(self):  # noqa: N802
        self.acknowledge_count += 1


def _make_engine_with_queue(messages):
    """Mock engine wrapper whose UI-message queue yields the given messages."""
    engine = MagicMock()
    pending = [UIMessage(m) for m in messages]
    type(engine).is_ui_message_queue_empty = property(lambda _self: not pending)
    engine.get_ui_message.side_effect = lambda: pending.pop(0)
    return engine


def test_dispatch_routes_by_event_code_and_to_global_callbacks():
    handler = UIMessageHandler(MagicMock())
    per_code = []
    all_events = []
    handler.on(100, lambda msg: per_code.append(msg.event))
    handler.on_all(lambda msg: all_events.append(msg.event))

    handler._dispatch(UIMessage(MockUIMsg(100)))
    handler._dispatch(UIMessage(MockUIMsg(200)))

    assert per_code == [100]
    assert all_events == [100, 200]


def test_every_message_is_acknowledged_after_callbacks():
    handler = UIMessageHandler(MagicMock())
    seen_at_callback_time = []
    message = MockUIMsg(100)
    handler.on(100, lambda _msg: seen_at_callback_time.append(message.acknowledge_count))

    handler._dispatch(UIMessage(message))

    # Acknowledged exactly once, and only after the callback ran.
    assert message.acknowledge_count == 1
    assert seen_at_callback_time == [0]


def test_message_is_acknowledged_even_when_callback_raises():
    handler = UIMessageHandler(MagicMock())

    def failing_callback(_msg):
        raise RuntimeError("callback bug")

    handler.on(100, failing_callback)
    message = MockUIMsg(100)

    handler._dispatch(UIMessage(message))

    assert message.acknowledge_count == 1


def test_process_pending_drains_queue_in_arrival_order():
    raw_messages = [MockUIMsg(code) for code in range(5)]
    engine = _make_engine_with_queue(raw_messages)
    handler = UIMessageHandler(engine)
    order = []
    handler.on_all(lambda msg: order.append(msg.event))

    handled = handler.process_pending()

    assert handled == 5
    assert order == [0, 1, 2, 3, 4]
    assert all(m.acknowledge_count == 1 for m in raw_messages)


def test_start_enables_engine_polling_once():
    engine = MagicMock()
    handler = UIMessageHandler(engine)

    handler.start()
    handler.start()

    assert engine.ui_message_polling_enabled is True


def test_wait_for_execution_pumps_until_end_and_drains_after():
    raw_messages = [MockUIMsg(10), MockUIMsg(8)]
    engine = _make_engine_with_queue(raw_messages)
    handler = UIMessageHandler(engine)
    seen = []
    handler.on_all(lambda msg: seen.append(msg.event))

    execution = MagicMock()
    # Not ended on the first poll, ended on the second.
    execution.wait_for_end_ex.side_effect = [False, True]

    ended = handler.wait_for_execution(execution, timeout_seconds=5)

    assert ended is True
    assert seen == [10, 8]
    assert all(m.acknowledge_count == 1 for m in raw_messages)


def test_wait_for_execution_times_out_when_execution_never_ends():
    engine = _make_engine_with_queue([])
    handler = UIMessageHandler(engine)
    execution = MagicMock()
    execution.wait_for_end_ex.return_value = False

    ended = handler.wait_for_execution(execution, timeout_seconds=0.05, poll_interval=0.01)

    assert ended is False


def test_handle_execution_fires_only_for_matching_execution_id():
    handler = UIMessageHandler(MagicMock())
    completed = []
    handler.handle_execution(42, lambda: completed.append(True))

    # UIMessage.execution wraps the raw COM object; Execution.id reads .Id from it.
    other_execution = MagicMock()
    other_execution.Id = 7
    matching_execution = MagicMock()
    matching_execution.Id = 42

    handler._dispatch(
        UIMessage(MockUIMsg(int(UIMessageCode.EndExecution), execution=other_execution))
    )
    assert completed == []

    handler._dispatch(
        UIMessage(MockUIMsg(int(UIMessageCode.EndExecution), execution=matching_execution))
    )
    assert completed == [True]


def test_on_works_as_decorator_and_off_unregisters():
    handler = UIMessageHandler(MagicMock())
    calls = []

    @handler.on(100)
    def on_hundred(msg):
        calls.append(msg.event)

    handler._dispatch(UIMessage(MockUIMsg(100)))
    assert calls == [100]

    assert handler.off(100, on_hundred) is True
    assert handler.off(100, on_hundred) is False  # already removed
    handler._dispatch(UIMessage(MockUIMsg(100)))
    assert calls == [100]


def test_messages_iterator_yields_and_acknowledges_after_loop_body():
    raw_messages = [MockUIMsg(10), MockUIMsg(11)]
    engine = _make_engine_with_queue(raw_messages)
    handler = UIMessageHandler(engine)
    execution = MagicMock()
    execution.wait_for_end_ex.return_value = True

    acknowledged_when_seen = []
    events = []
    for message in handler.messages(execution, timeout_seconds=5):
        events.append(message.event)
        acknowledged_when_seen.append([m.acknowledge_count for m in raw_messages])

    assert events == [10, 11]
    # First message not yet acknowledged while its body ran; acknowledged before the second's body.
    assert acknowledged_when_seen == [[0, 0], [1, 0]]
    assert all(m.acknowledge_count == 1 for m in raw_messages)


def test_stop_drops_registered_callbacks():
    handler = UIMessageHandler(MagicMock())
    calls = []
    handler.on(100, lambda msg: calls.append(msg.event))
    handler.on_all(lambda msg: calls.append(msg.event))

    handler.stop()
    handler._dispatch(UIMessage(MockUIMsg(100)))

    assert calls == []
