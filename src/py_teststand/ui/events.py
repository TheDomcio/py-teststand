from __future__ import annotations

import logging
import typing
from typing import Callable

try:
    import win32com.client
except ImportError:
    win32com: typing.Any = None

logger = logging.getLogger(__name__)


class UIEventSinkMeta(type):
    def __new__(cls, name, bases, attrs):
        new_attrs = dict(attrs)
        for attr_name, value in attrs.items():
            if attr_name.startswith("on_") and callable(value):
                words = attr_name[3:].split("_")
                camel_name = "On" + "".join(word.capitalize() for word in words)
                new_attrs[camel_name] = value
        return super().__new__(cls, name, bases, new_attrs)


class UIEventSink(metaclass=UIEventSinkMeta):
    def __init__(self):

        self._handlers: dict[str, list[Callable]] = {}
        self._log_events = True

    def _log(self, event_name: str, *args):

        if self._log_events:
            args_str = ", ".join(str(a)[:50] for a in args)
            logger.debug(f"EVENT FIRED: {event_name}({args_str})")

    def on(self, event_name: str, handler: Callable):
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)

        handler_name = handler.__name__ if hasattr(handler, "__name__") else str(handler)
        logger.debug(f"EVENT REGISTERED: {event_name} -> {handler_name}")

    def _trigger(self, event_name: str, *args) -> typing.Any:

        self._log(event_name, *args)
        last_result = None
        for handler in self._handlers.get(event_name, []):
            try:
                res = handler(*args)
                if res is not None:
                    last_result = res
            except TypeError as e:
                import sys

                print(
                    f"DEBUG: TypeError executing {handler} on {args} for {event_name}: {e}",
                    file=sys.stderr,
                )
                logger.exception(f"Error in event handler for {event_name}")
            except Exception:
                logger.exception(f"Error in event handler for {event_name}")
        return last_result


class ApplicationMgrEventsSink(UIEventSink):
    def on_exit_application(self):
        try:
            self._trigger("ExitApplication")
        except Exception as e:
            logger.error(f"Error in on_exit_application: {e}")

    def on_can_edit(self, edited_file, edit_kind, can_edit_value, edit_denial_reasons):
        try:
            res = self._trigger(
                "CanEdit",
                edited_file,
                edit_kind,
                can_edit_value,
                edit_denial_reasons,
            )
            if isinstance(res, tuple) and len(res) >= 2:
                return res
            if res is not None:
                return (bool(res), edit_denial_reasons)
            return (can_edit_value, edit_denial_reasons)
        except Exception as e:
            logger.error(f"Error in on_can_edit: {e}")
            return (can_edit_value, edit_denial_reasons)

    def on_begin_edit(self, edited_file, edit_kind, objects_to_edit, cancel, edit_denial_reasons):
        try:
            res = self._trigger(
                "BeginEdit",
                edited_file,
                edit_kind,
                objects_to_edit,
                cancel,
                edit_denial_reasons,
            )
            if isinstance(res, tuple) and len(res) >= 2:
                return res
            if res is not None:
                return (bool(res), edit_denial_reasons)
            return (cancel, edit_denial_reasons)
        except Exception as e:
            logger.error(f"Error in on_begin_edit: {e}")
            return (cancel, edit_denial_reasons)

    def on_edit_mode_changed(self):
        try:
            self._trigger("EditModeChanged")
        except Exception as e:
            logger.error(f"Error in on_edit_mode_changed: {e}")

    def on_report_error(self, message, error_code):
        try:
            self._trigger("ReportError", message, error_code)
        except Exception as e:
            logger.error(f"Error in on_report_error: {e}")

    def on_sequence_file_opened(self, file):
        try:
            self._trigger("SequenceFileOpened", file)
        except Exception as e:
            logger.error(f"Error in on_sequence_file_opened: {e}")

    def on_sequence_file_closing(self, file):
        try:
            self._trigger("SequenceFileClosing", file)
        except Exception as e:
            logger.error(f"Error in on_sequence_file_closing: {e}")

    def on_query_reload_sequence_file(self, file, reload_option):
        try:
            res = self._trigger("QueryReloadSequenceFile", file, reload_option)
            return int(res) if res is not None else reload_option
        except Exception as e:
            logger.error(f"Error in on_query_reload_sequence_file: {e}")
            return reload_option

    def on_process_user_command_line_arguments(
        self,
        process_command,
        arguments,
        current_argument,
        error_processing,
        error_message,
    ):
        try:
            res = self._trigger(
                "ProcessUserCommandLineArguments",
                process_command,
                arguments,
                current_argument,
                error_processing,
                error_message,
            )
            if isinstance(res, tuple) and len(res) >= 3:
                return res
            return (current_argument, error_processing, error_message)
        except Exception as e:
            logger.error(f"Error in on_process_user_command_line_arguments: {e}")
            return (current_argument, error_processing, error_message)

    def on_drop_file(self, file_path):
        try:
            self._trigger("DropFile", file_path)
        except Exception as e:
            logger.error(f"Error in on_drop_file: {e}")

    def on_sequence_file_closed(self, file):
        try:
            self._trigger("SequenceFileClosed", file)
        except Exception as e:
            logger.error(f"Error in on_sequence_file_closed: {e}")

    def on_user_changed(self):
        try:
            self._trigger("UserChanged")
        except Exception as e:
            logger.error(f"Error in on_user_changed: {e}")

    def on_wait(self, is_waiting):
        try:
            self._trigger("Wait", is_waiting)
        except Exception as e:
            logger.error(f"Error in on_wait: {e}")

    def on_pre_command_execute(self, command, cancel):
        try:
            res = self._trigger("PreCommandExecute", command, cancel)
            return bool(res) if res is not None else cancel
        except Exception as e:
            logger.error(f"Error in on_pre_command_execute: {e}")
            return cancel

    def on_post_command_execute(self, command):
        try:
            self._trigger("PostCommandExecute", command)
        except Exception as e:
            logger.error(f"Error in on_post_command_execute: {e}")

    def on_query_close_execution(self, execution, run_state, option):
        try:
            res = self._trigger("QueryCloseExecution", execution, run_state, option)
            return int(res) if res is not None else option
        except Exception as e:
            logger.error(f"Error in on_query_close_execution: {e}")
            return option

    def on_execution_closed(self, execution):
        try:
            self._trigger("ExecutionClosed", execution)
        except Exception as e:
            logger.error(f"Error in on_execution_closed: {e}")

    def on_query_close_sequence_file(self, file, cancel):
        try:
            res = self._trigger("QueryCloseSequenceFile", file, cancel)
            return bool(res) if res is not None else cancel
        except Exception as e:
            logger.error(f"Error in on_query_close_sequence_file: {e}")
            return cancel

    def on_query_shutdown(self, cancel):
        try:
            res = self._trigger("QueryShutdown", cancel)
            return bool(res) if res is not None else cancel
        except Exception as e:
            logger.error(f"Error in on_query_shutdown: {e}")
            return cancel

    def on_display_sequence_file(self, file, reason):
        try:
            self._trigger("DisplaySequenceFile", file, reason)
        except Exception as e:
            logger.error(f"Error in on_display_sequence_file: {e}")

    def on_display_execution(self, execution, reason):
        try:
            self._trigger("DisplayExecution", execution, reason)
        except Exception as e:
            logger.error(f"Error in on_display_execution: {e}")

    def on_display_report(self, report):
        try:
            self._trigger("DisplayReport", report)
        except Exception as e:
            logger.error(f"Error in on_display_report: {e}")

    def on_ui_message_event(self, ui_msg, cancel):
        try:
            res = self._trigger("UIMessageEvent", ui_msg, cancel)
            return bool(res) if res is not None else cancel
        except Exception as e:
            logger.error(f"Error in on_ui_message_event: {e}")
            return cancel

    def on_after_ui_message_event(self, ui_msg):
        try:
            self._trigger("AfterUIMessageEvent", ui_msg)
        except Exception as e:
            logger.error(f"Error in on_after_ui_message_event: {e}")

    def on_shut_down_completed(self):
        try:
            self._trigger("ShutDownCompleted")
        except Exception as e:
            logger.error(f"Error in on_shut_down_completed: {e}")

    def on_shut_down_cancelled(self):
        try:
            self._trigger("ShutDownCancelled")
        except Exception as e:
            logger.error(f"Error in on_shut_down_cancelled: {e}")

    def on_start_execution(self, execution):
        try:
            self._trigger("StartExecution", execution)
        except Exception as e:
            logger.error(f"Error in on_start_execution: {e}")

    def on_end_execution(self, execution):
        try:
            self._trigger("EndExecution", execution)
        except Exception as e:
            logger.error(f"Error in on_end_execution: {e}")

    def on_end_edit(self, edited_file, edit_kind, edited_objects, cancelled):
        try:
            self._trigger("EndEdit", edited_file, edit_kind, edited_objects, cancelled)
        except Exception as e:
            logger.error(f"Error in on_end_edit: {e}")

    def on_break_on_run_time_error(
        self,
        execution,
        initiating_thread,
        show_dialog,
        break_execution,
    ):
        try:
            res = self._trigger(
                "BreakOnRunTimeError",
                execution,
                initiating_thread,
                show_dialog,
                break_execution,
            )
            if isinstance(res, tuple) and len(res) >= 2:
                return res
            return (show_dialog, break_execution)
        except Exception as e:
            logger.error(f"Error in on_break_on_run_time_error: {e}")
            return (show_dialog, break_execution)

    def on_user_message(self, ui_msg):
        try:
            self._trigger("UserMessage", ui_msg)
        except Exception as e:
            logger.error(f"Error in on_user_message: {e}")

    def on_refresh_windows(self):
        try:
            self._trigger("RefreshWindows")
        except Exception as e:
            logger.error(f"Error in on_refresh_windows: {e}")

    def on_break(self, execution, thread, sequence_context):
        try:
            self._trigger("Break", execution, thread, sequence_context)
        except Exception as e:
            logger.error(f"Error in on_break: {e}")

    def on_display_custom_run_time_error_dialog(
        self,
        ctxt,
        break_exec,
        do_not_show_again_for_execution,
        do_not_show_again_for_batch,
        rte_option,
        show_default_dialog,
    ):
        try:
            res = self._trigger(
                "DisplayCustomRunTimeErrorDialog",
                ctxt,
                break_exec,
                do_not_show_again_for_execution,
                do_not_show_again_for_batch,
                rte_option,
                show_default_dialog,
            )
            if isinstance(res, tuple) and len(res) >= 5:
                return res
            return (
                break_exec,
                do_not_show_again_for_execution,
                do_not_show_again_for_batch,
                rte_option,
                show_default_dialog,
            )
        except Exception as e:
            logger.error(f"Error in on_display_custom_run_time_error_dialog: {e}")
            return (
                break_exec,
                do_not_show_again_for_execution,
                do_not_show_again_for_batch,
                rte_option,
                show_default_dialog,
            )


class SequenceFileViewMgrEventsSink(UIEventSink):
    def on_sequence_file_changed(self, file):
        try:
            self._trigger("SequenceFileChanged", file)
        except Exception as e:
            logger.error(f"Error in on_sequence_file_changed: {e}")

    def on_selection_changed(self):
        try:
            self._trigger("SelectionChanged")
        except Exception as e:
            logger.error(f"Error in on_selection_changed: {e}")

    def on_sequence_changed(self, sequence):
        try:
            self._trigger("SequenceChanged", sequence)
        except Exception as e:
            logger.error(f"Error in on_sequence_changed: {e}")

    def on_step_group_changed(self, step_group):
        try:
            self._trigger("StepGroupChanged", step_group)
        except Exception as e:
            logger.error(f"Error in on_step_group_changed: {e}")

    def on_refresh_window(self):
        try:
            self._trigger("RefreshWindow")
        except Exception as e:
            logger.error(f"Error in on_refresh_window: {e}")

    def on_sequence_selection_changed(self):
        try:
            self._trigger("SequenceSelectionChanged")
        except Exception as e:
            logger.error(f"Error in on_sequence_selection_changed: {e}")

    def on_property_object_selection_changed(self):
        try:
            self._trigger("PropertyObjectSelectionChanged")
        except Exception as e:
            logger.error(f"Error in on_property_object_selection_changed: {e}")


class ExecutionViewMgrEventsSink(UIEventSink):
    def on_execution_changed(self, execution):
        try:
            self._trigger("ExecutionChanged", execution)
        except Exception as e:
            logger.error(f"Error in on_execution_changed: {e}")

    def on_run_state_changed(self, new_run_state):
        try:
            self._trigger("RunStateChanged", new_run_state)
        except Exception as e:
            logger.error(f"Error in on_run_state_changed: {e}")

    def on_end_execution(self, execution):
        try:
            self._trigger("EndExecution", execution)
        except Exception as e:
            logger.error(f"Error in on_end_execution: {e}")

    def on_termination_state_changed(self, new_term_state):
        try:
            self._trigger("TerminationStateChanged", new_term_state)
        except Exception as e:
            logger.error(f"Error in on_termination_state_changed: {e}")

    def on_selection_changed(self):
        try:
            self._trigger("SelectionChanged")
        except Exception as e:
            logger.error(f"Error in on_selection_changed: {e}")

    def on_user_message(self, ui_msg):
        try:
            self._trigger("UserMessage", ui_msg)
        except Exception as e:
            logger.error(f"Error in on_user_message: {e}")

    def on_refresh_window(self):
        try:
            self._trigger("RefreshWindow")
        except Exception as e:
            logger.error(f"Error in on_refresh_window: {e}")

    def on_break(self, execution, thread, sequence_context):
        try:
            self._trigger("Break", execution, thread, sequence_context)
        except Exception as e:
            logger.error(f"Error in on_break: {e}")

    def on_trace(self, execution, thread, sequence_context):
        try:
            self._trigger("Trace", execution, thread, sequence_context)
        except Exception as e:
            logger.error(f"Error in on_trace: {e}")

    def on_display_report(self, report):
        try:
            self._trigger("DisplayReport", report)
        except Exception as e:
            logger.error(f"Error in on_display_report: {e}")

    def on_context_changed(self, sequence_context):
        try:
            self._trigger("ContextChanged", sequence_context)
        except Exception as e:
            logger.error(f"Error in on_context_changed: {e}")

    def on_thread_changed(self, thread):
        try:
            self._trigger("ThreadChanged", thread)
        except Exception as e:
            logger.error(f"Error in on_thread_changed: {e}")

    def on_property_object_selection_changed(self):
        try:
            self._trigger("PropertyObjectSelectionChanged")
        except Exception as e:
            logger.error(f"Error in on_property_object_selection_changed: {e}")


def connect_events(mgr_wrapper: typing.Any, sink_class: type[UIEventSink]) -> UIEventSink:

    if win32com is None:
        raise ImportError("win32com is required to connect events")
    return win32com.client.WithEvents(mgr_wrapper._com_obj, sink_class)
