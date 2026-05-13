from __future__ import annotations

import functools
import typing
from enum import IntEnum, IntFlag
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.property.property_object import PropertyObject

if TYPE_CHECKING:
    from py_teststand.adapters.sequence import NewThreadOption
    from py_teststand.core.engine import RTEOption
    from py_teststand.execution.output_record_stream import ExecutionOutputRecordStreams
    from py_teststand.execution.thread import Thread
    from py_teststand.sequence.sequence import Sequence
    from py_teststand.sequence.sequence_file import SequenceFile


class CallbackType(IntFlag):
    ModelPostError = 0x0
    ModelPostFail = 0x1
    ModelPostInteractive = 0x2
    ModelPostResult = 0x3
    ModelPostStep = 0x4
    ModelPreInteractive = 0x5
    ModelPreStep = 0x6
    SeqFilePostError = 0x7
    SeqFilePostFail = 0x8
    SeqFilePostInteractive = 0x9
    SeqFilePostResult = 0xA
    SeqFilePostStep = 0xB
    SeqFilePreInteractive = 0xC
    SeqFilePreStep = 0xD
    StationPostError = 0xE
    StationPostFail = 0xF
    StationPostInteractive = 0x10
    StationPostResult = 0x11
    StationPostStep = 0x12
    StationPreInteractive = 0x13
    StationPreStep = 0x14
    ModelPostResults = 0x15
    SeqFilePostResults = 0x16
    StationPostResults = 0x17


class RestartOption(IntFlag):
    NoneValue = 0
    BreakOnEntry = 1
    OverrideNotRestartable = 2
    BreakOnStepFailure = 4
    BreakOnSequenceFailure = 8


class PostResultsCallbackOption(IntFlag):
    NoneValue = 0
    CallAfterProvisionalResult = 1


class PostResultsCallbackMaskOption(IntFlag):
    NoneValue = 0
    PreStep = 1
    PostStep = 2
    PreInteractive = 4
    PostInteractive = 8
    PostResultListEntry = 16
    PostStepRuntimeError = 32
    PostStepFailure = 64
    PostAction = 128
    SequenceCall = 256
    All = -1


class ExecutionTypeMask(IntFlag):
    Normal = 0x0
    InitiallyHidden = 0x1
    TracingInitiallyOff = 0x2
    InitiallySuspended = 0x4
    NotRestartable = 0x8
    CloseWindowWhenDone = 0x10
    BreakOnStepFailure = 0x20
    BreakOnSequenceFailure = 0x40
    AutoWaitAtEndOfSequence = 0x80
    UseSTA = 0x100
    DisplayPreloadProgress = 0x200
    DiscardArgumentsWhenDone = 0x400


class ExecutionMask(IntFlag):
    BreakpointsEnabled = 0x1
    BreakWhileTerminating = 0x2
    BreakOnRunTimeError = 0x4
    TracingEnabled = 0x8
    TraceIntoSetupCleanup = 0x10
    TraceIntoPrePostCallbacks = 0x20
    TraceIntoPostActionCallbacks = 0x40
    TraceIntoSeparateExecutionCallbacks = 0x80
    TraceIntoEntryPoints = 0x100
    TraceIntoSequenceCallsMarkedAsTraceOff = 0x200
    TraceAllThreads = 0x800
    InteractiveRunSetupCleanup = 0x2000
    InteractiveRecordResults = 0x1000
    InteractiveEvaluatePreconditions = 0x4000
    AllowBreakWhileInCodeModules = 0x8000


class ExecutionRunState(IntEnum):
    Running = 1
    Paused = 2
    Stopped = 3


class ExecutionTerminationState(IntEnum):
    Normal = 1
    Terminating = 2
    TerminatingInteractive = 3
    Aborting = 4
    KillingThreads = 5


class ThreadTermination(IntEnum):
    Normal = 0
    Prompt = 1
    Never = 2


class Execution(COMWrapper):
    def __enter__(self) -> Execution:

        return self

    def __exit__(self, exc_type: typing.Any, exc_val: typing.Any, exc_tb: typing.Any) -> None:

        if exc_type is not None:
            try:
                self.abort()
            except Exception:
                pass
        self.release()

    @property
    @ts_interface
    def break_on_entry(self) -> bool:
        return bool(self._com_obj.BreakOnEntry)

    @property
    @ts_interface
    def client_file(self) -> SequenceFile | None:
        from py_teststand.sequence.sequence_file import SequenceFile

        com_file = getattr(self._com_obj, "ClientFile", None)
        return SequenceFile(com_file, self._engine_ref) if com_file else None

    @client_file.setter
    @ts_interface
    def client_file(self, value: SequenceFile | None) -> None:
        self._com_obj.ClientFile = value._com_obj if value else None

    @property
    @ts_interface
    def disable_results(self) -> bool:
        return bool(self._com_obj.DisableResults)

    @disable_results.setter
    @ts_interface
    def disable_results(self, value: bool) -> None:
        self._com_obj.DisableResults = bool(value)

    @property
    @ts_interface
    def discard_results(self) -> bool:
        return bool(self._com_obj.DiscardResults)

    @discard_results.setter
    @ts_interface
    def discard_results(self, value: bool) -> None:
        self._com_obj.DiscardResults = bool(value)

    @property
    @ts_interface
    def display_name(self) -> str:
        return str(self._com_obj.DisplayName)

    @property
    @ts_interface
    def error_object(self) -> PropertyObject:
        return PropertyObject(self._com_obj.ErrorObject, self._engine_ref)

    @property
    @ts_interface
    def foreground_thread(self) -> Thread:
        from py_teststand.execution.thread import Thread

        return Thread(self._com_obj.ForegroundThread, self._engine_ref)

    @foreground_thread.setter
    @ts_interface
    def foreground_thread(self, value: Thread) -> None:
        self._com_obj.ForegroundThread = value._com_obj

    @property
    @ts_interface
    def foreground_thread_index(self) -> int:
        return int(self._com_obj.ForegroundThreadIndex)

    @foreground_thread_index.setter
    @ts_interface
    def foreground_thread_index(self, value: int) -> None:
        self._com_obj.ForegroundThreadIndex = int(value)

    @functools.cached_property
    @ts_interface
    def id(self) -> int:
        return int(self._com_obj.Id)

    @property
    @ts_interface
    def in_interactive_mode(self) -> bool:
        return bool(self._com_obj.InInteractiveMode)

    @property
    @ts_interface
    def is_controller(self) -> bool:
        return bool(self._com_obj.IsController)

    @is_controller.setter
    @ts_interface
    def is_controller(self, value: bool) -> None:
        self._com_obj.IsController = bool(value)

    @property
    @ts_interface
    def is_root_execution(self) -> bool:
        return bool(self._com_obj.IsRootExecution)

    @property
    @ts_interface
    def maximum_results_per_post_results_callback(self) -> int:
        return int(self._com_obj.MaximumResultsPerPostResultsCallback)

    @maximum_results_per_post_results_callback.setter
    @ts_interface
    def maximum_results_per_post_results_callback(self, value: int) -> None:
        self._com_obj.MaximumResultsPerPostResultsCallback = int(value)

    @property
    @ts_interface
    def model_sequence_file_path(self) -> str:
        return str(self._com_obj.ModelSequenceFilePath)

    @property
    @ts_interface
    def num_threads(self) -> int:
        return int(self._com_obj.NumThreads)

    @property
    @ts_interface
    def parent_execution_id(self) -> int:
        return int(self._com_obj.ParentExecutionId)

    @parent_execution_id.setter
    @ts_interface
    def parent_execution_id(self, value: int) -> None:
        self._com_obj.ParentExecutionId = int(value)

    @property
    @ts_interface
    def child_execution_ids(self) -> list[int]:
        return list(self._com_obj.ChildExecutionIds)

    @property
    @ts_interface
    def output_record_streams(self) -> ExecutionOutputRecordStreams:
        from py_teststand.execution.output_record_stream import (
            ExecutionOutputRecordStreams,
        )

        return ExecutionOutputRecordStreams(self._com_obj.OutputRecordStreams, self._engine_ref)

    @property
    @ts_interface
    def override_non_terminatable_threads(self) -> bool:
        return bool(self._com_obj.OverrideNonTerminatableThreads)

    @override_non_terminatable_threads.setter
    @ts_interface
    def override_non_terminatable_threads(self, value: bool) -> None:
        self._com_obj.OverrideNonTerminatableThreads = bool(value)

    @property
    @ts_interface
    def post_results_callback_post_flush_mask(self) -> PostResultsCallbackMaskOption:

        return PostResultsCallbackMaskOption(int(self._com_obj.PostResultsCallback_PostFlushMask))

    @post_results_callback_post_flush_mask.setter
    @ts_interface
    def post_results_callback_post_flush_mask(
        self, value: PostResultsCallbackMaskOption | int
    ) -> None:
        self._com_obj.PostResultsCallback_PostFlushMask = int(value)

    @property
    @ts_interface
    def post_results_callback_pre_flush_mask(self) -> PostResultsCallbackMaskOption:

        return PostResultsCallbackMaskOption(int(self._com_obj.PostResultsCallback_PreFlushMask))

    @post_results_callback_pre_flush_mask.setter
    @ts_interface
    def post_results_callback_pre_flush_mask(
        self, value: PostResultsCallbackMaskOption | int
    ) -> None:
        self._com_obj.PostResultsCallback_PreFlushMask = int(value)

    @property
    @ts_interface
    def post_results_callback_interval(self) -> float:
        return float(self._com_obj.PostResultsCallbackInterval)

    @post_results_callback_interval.setter
    @ts_interface
    def post_results_callback_interval(self, value: float) -> None:
        self._com_obj.PostResultsCallbackInterval = float(value)

    @property
    @ts_interface
    def post_results_callback_mask(self) -> PostResultsCallbackMaskOption:

        return PostResultsCallbackMaskOption(int(self._com_obj.PostResultsCallbackMask))

    @post_results_callback_mask.setter
    @ts_interface
    def post_results_callback_mask(self, value: PostResultsCallbackMaskOption | int) -> None:
        self._com_obj.PostResultsCallbackMask = int(value)

    @property
    @ts_interface
    def post_results_callback_options(self) -> PostResultsCallbackOption:

        return PostResultsCallbackOption(int(self._com_obj.PostResultsCallbackOption))

    @post_results_callback_options.setter
    @ts_interface
    def post_results_callback_options(self, value: PostResultsCallbackOption | int) -> None:
        self._com_obj.PostResultsCallbackOption = int(value)

    @property
    @ts_interface
    def report(self) -> typing.Any:
        return self._com_obj.Report

    @property
    @ts_interface
    def reports(self) -> typing.Any:
        return self._com_obj.Reports

    @property
    @ts_interface
    def result_object(self) -> PropertyObject:
        return PropertyObject(self._com_obj.ResultObject, self._engine_ref)

    @property
    @ts_interface
    def result_status(self) -> str:
        return str(self._com_obj.ResultStatus)

    @result_status.setter
    @ts_interface
    def result_status(self, value: str) -> None:
        self._com_obj.ResultStatus = str(value)

    @property
    @ts_interface
    def rte_option_for_this_execution(self) -> typing.Any:
        from py_teststand.core.engine import RTEOption

        return RTEOption(int(self._com_obj.RTEOptionForThisExecution))

    @rte_option_for_this_execution.setter
    @ts_interface
    def rte_option_for_this_execution(self, value: RTEOption | int) -> None:
        self._com_obj.RTEOptionForThisExecution = int(value)

    @property
    @ts_interface
    def run_time_variables(self) -> PropertyObject:
        return PropertyObject(self._com_obj.RunTimeVariables, self._engine_ref)

    @property
    @ts_interface
    def seconds_at_start(self) -> float:
        return float(self._com_obj.SecondsAtStart)

    @property
    @ts_interface
    def seconds_executing(self) -> float:
        return float(self._com_obj.SecondsExecuting)

    @property
    @ts_interface
    def seconds_suspended(self) -> float:
        return float(self._com_obj.SecondsSuspended)

    @property
    @ts_interface
    def sequence_file_path(self) -> str:
        return str(self._com_obj.SequenceFilePath)

    @property
    @ts_interface
    def standard_results_enabled(self) -> bool:
        return bool(self._com_obj.StandardResultsEnabled)

    @standard_results_enabled.setter
    @ts_interface
    def standard_results_enabled(self, value: bool) -> None:
        self._com_obj.StandardResultsEnabled = bool(value)

    @property
    @ts_interface
    def start_count(self) -> int:
        return int(self._com_obj.StartCount)

    @property
    @ts_interface
    def terminate_non_terminatable_threads_prompt(self) -> str:
        return str(self._com_obj.TerminateNonTerminatableThreadsPrompt)

    @terminate_non_terminatable_threads_prompt.setter
    @ts_interface
    def terminate_non_terminatable_threads_prompt(self, value: str) -> None:
        self._com_obj.TerminateNonTerminatableThreadsPrompt = str(value)

    @property
    @ts_interface
    def thread_ids(self) -> list[int]:
        return list(self._com_obj.ThreadIds)

    @property
    @ts_interface
    def time_results_enabled(self) -> bool:
        return bool(self._com_obj.TimeResultsEnabled)

    @time_results_enabled.setter
    @ts_interface
    def time_results_enabled(self, value: bool) -> None:
        self._com_obj.TimeResultsEnabled = bool(value)

    @property
    @ts_interface
    def tracing_disabled(self) -> bool:
        return bool(self._com_obj.TracingDisabled)

    @tracing_disabled.setter
    @ts_interface
    def tracing_disabled(self, value: bool) -> None:
        self._com_obj.TracingDisabled = bool(value)

    @property
    @ts_interface
    def type_mask(self) -> ExecutionTypeMask:

        return ExecutionTypeMask(int(self._com_obj.TypeMask))

    @ts_interface
    def abort(self) -> None:
        self._com_obj.Abort()

    @ts_interface
    def add_extra_result(self, property_name: str, result_property_name: str) -> None:
        self._com_obj.AddExtraResult(str(property_name), str(result_property_name))

    @ts_interface
    def add_post_step_custom_ui_message(
        self,
        message_code: int,
        expression: str,
        custom_ui_message_options: int = 0,
    ) -> None:
        self._com_obj.AddPostStepCustomUIMessage(
            int(message_code), str(expression), int(custom_ui_message_options)
        )

    @ts_interface
    def as_property_object(self) -> PropertyObject:
        return PropertyObject(self._com_obj.AsPropertyObject(), self._engine_ref)

    @ts_interface
    def break_execution(self) -> None:
        self._com_obj.Break()

    @ts_interface
    def cancel_termination(self) -> None:
        self._com_obj.CancelTermination()

    @ts_interface
    def clear_extra_result_list(self) -> None:
        self._com_obj.ClearExtraResultList()

    @ts_interface
    def clear_sequence_default_values(
        self,
        orig_sequence: Sequence | None = None,
        default_value_type: int = 1,  # SeqDefaultValScope_Execution
    ) -> None:
        com_seq = orig_sequence._com_obj if orig_sequence else None
        self._com_obj.ClearSequenceDefaultValues(com_seq, int(default_value_type))

    @ts_interface
    def clear_temporary_breakpoints(self) -> None:
        self._com_obj.ClearTemporaryBreakpoints()

    @ts_interface
    def delete_extra_result(self, property_name: str) -> None:
        self._com_obj.DeleteExtraResult(str(property_name))

    @ts_interface
    def enable_callback(self, callback_type: CallbackType | int, enabled: bool) -> None:
        self._com_obj.EnableCallback(int(callback_type), bool(enabled))

    @ts_interface
    def get_file_globals(self, sequence_file: SequenceFile) -> PropertyObject:
        return PropertyObject(
            self._com_obj.GetFileGlobals(sequence_file._com_obj), self._engine_ref
        )

    @ts_interface
    def get_model_sequence_file(self) -> typing.Any | None:
        from py_teststand.sequence.sequence_file import SequenceFile

        model_com = self._com_obj.GetModelSequenceFile()
        return SequenceFile(model_com, self._engine_ref) if model_com else None

    @ts_interface
    def get_sequence_default_values(
        self,
        orig_sequence: Sequence,
        default_value_type: int = 1,  # SeqDefaultValScope_Execution
    ) -> Sequence | None:
        from py_teststand.sequence.sequence import Sequence

        ret_com = self._com_obj.GetSequenceDefaultValues(
            orig_sequence._com_obj, int(default_value_type)
        )
        return Sequence(ret_com, self._engine_ref) if ret_com else None

    @ts_interface
    def get_sequence_file(self) -> SequenceFile:
        from py_teststand.sequence.sequence_file import SequenceFile

        return SequenceFile(self._com_obj.GetSequenceFile(), self._engine_ref)

    @ts_interface
    def get_states(self) -> typing.Any:

        run_state = 0
        term_state = 0
        run_state, term_state = self._com_obj.GetStates(run_state, term_state)
        return ExecutionRunState(int(run_state)), ExecutionTerminationState(int(term_state))

    @ts_interface
    def get_termination_monitor_status(
        self,
        termination_monitor_data: PropertyObject,
        sequence_context: typing.Any | None = None,
    ) -> bool:
        ctx_com = sequence_context._com_obj if sequence_context else None
        return bool(
            self._com_obj.GetTerminationMonitorStatus(termination_monitor_data._com_obj, ctx_com)
        )

    @ts_interface
    def get_thread(self, thread_id: int) -> typing.Any:
        from py_teststand.execution.thread import Thread

        return Thread(self._com_obj.GetThread(int(thread_id)), self._engine_ref)

    @ts_interface
    def init_termination_monitor(self) -> PropertyObject:
        return PropertyObject(self._com_obj.InitTerminationMonitor(), self._engine_ref)

    @ts_interface
    def is_callback_enabled(self, callback_type: CallbackType | int) -> bool:
        return bool(self._com_obj.IsCallbackEnabled(int(callback_type)))

    @ts_interface
    def new_sequence_default_values(self, orig_sequence: Sequence) -> Sequence:
        from py_teststand.sequence.sequence import Sequence

        return Sequence(
            self._com_obj.NewSequenceDefaultValues(orig_sequence._com_obj), self._engine_ref
        )

    @ts_interface
    def new_thread(
        self,
        sequence_file: SequenceFile,
        sequence_name: str,
        options: NewThreadOption | int,
        sequence_context: typing.Any | None = None,
        sequence_args: PropertyObject | None = None,
    ) -> Thread:
        from py_teststand.execution.thread import Thread

        ctx_com = sequence_context._com_obj if sequence_context else None
        args_com = sequence_args._com_obj if sequence_args else None
        return Thread(
            self._com_obj.NewThread(
                sequence_file._com_obj, str(sequence_name), int(options), ctx_com, args_com
            ),
            self._engine_ref,
        )

    @ts_interface
    def remove_post_step_custom_ui_message(self, message_id: int) -> None:
        self._com_obj.RemovePostStepCustomUIMessage(int(message_id))

    @ts_interface
    def restart_ex(self, options: int = 0) -> None:
        self._com_obj.RestartEx(int(options))

    @ts_interface
    def restart_with_new_arguments(
        self,
        restart_options: int,
        sequence_args: PropertyObject | None = None,
    ) -> None:
        args_com = sequence_args._com_obj if sequence_args else None
        self._com_obj.RestartWithNewArguments(int(restart_options), args_com)

    @ts_interface
    def resume(self) -> None:
        self._com_obj.Resume()

    @ts_interface
    def set_sequence_default_values(
        self,
        def_val_sequence: Sequence,
        default_value_scope: int = 1,  # SeqDefaultValScope_Execution
    ) -> None:
        self._com_obj.SetSequenceDefaultValues(def_val_sequence._com_obj, int(default_value_scope))

    @ts_interface
    def step_into(self) -> None:
        self._com_obj.StepInto()

    @ts_interface
    def step_out(self) -> None:
        self._com_obj.StepOut()

    @ts_interface
    def step_over(self) -> None:
        self._com_obj.StepOver()

    @ts_interface
    def terminate(self) -> None:
        self._com_obj.Terminate()

    @ts_interface
    def terminate_interactive_execution(self) -> None:
        self._com_obj.TerminateInteractiveExecution()

    @ts_interface
    def wait_for_end_ex(
        self,
        timeout_ms: int = -1,
        process_windows_msgs: bool = True,
        step_to_store_results_in: typing.Any | None = None,
        calling_sequence_context: typing.Any | None = None,
    ) -> bool:
        import pythoncom

        step_com = (
            step_to_store_results_in._com_obj if step_to_store_results_in else pythoncom.Missing
        )
        ctx_com = (
            calling_sequence_context._com_obj if calling_sequence_context else pythoncom.Missing
        )
        res = self._com_obj.WaitForEndEx(
            int(timeout_ms), bool(process_windows_msgs), step_com, ctx_com
        )
        if isinstance(res, tuple):
            return bool(res[0])
        return bool(res)

    @property
    @ts_interface
    def is_done(self) -> bool:

        run_state, _ = self.get_states()
        return run_state == ExecutionRunState.Stopped

    @ts_interface
    def wait(self, timeout_ms: int = -1) -> bool:
        return self.wait_for_end_ex(timeout_ms)

    @ts_interface
    def restart(self) -> typing.Any:

        return self._com_obj.Restart()

    @ts_interface
    def wait_for_end(self) -> typing.Any:

        return self._com_obj.WaitForEnd()

    @property
    @ts_interface
    def break_on_rte_for_this_execution(self) -> bool:
        return bool(self._com_obj.BreakOnRTEForThisExecution)

    @break_on_rte_for_this_execution.setter
    @ts_interface
    def break_on_rte_for_this_execution(self, value: bool) -> None:
        self._com_obj.BreakOnRTEForThisExecution = bool(value)

    @property
    @ts_interface
    def model_post_error_callback_enabled(self) -> bool:
        return bool(self._com_obj.ModelPostErrorCallbackEnabled)

    @model_post_error_callback_enabled.setter
    @ts_interface
    def model_post_error_callback_enabled(self, value: bool) -> None:
        self._com_obj.ModelPostErrorCallbackEnabled = bool(value)

    @property
    @ts_interface
    def model_post_fail_callback_enabled(self) -> bool:
        return bool(self._com_obj.ModelPostFailCallbackEnabled)

    @model_post_fail_callback_enabled.setter
    @ts_interface
    def model_post_fail_callback_enabled(self, value: bool) -> None:
        self._com_obj.ModelPostFailCallbackEnabled = bool(value)

    @property
    @ts_interface
    def model_post_interactive_callback_enabled(self) -> bool:
        return bool(self._com_obj.ModelPostInteractiveCallbackEnabled)

    @model_post_interactive_callback_enabled.setter
    @ts_interface
    def model_post_interactive_callback_enabled(self, value: bool) -> None:
        self._com_obj.ModelPostInteractiveCallbackEnabled = bool(value)

    @property
    @ts_interface
    def model_post_result_callback_enabled(self) -> bool:
        return bool(self._com_obj.ModelPostResultCallbackEnabled)

    @model_post_result_callback_enabled.setter
    @ts_interface
    def model_post_result_callback_enabled(self, value: bool) -> None:
        self._com_obj.ModelPostResultCallbackEnabled = bool(value)

    @property
    @ts_interface
    def model_post_step_callback_enabled(self) -> bool:
        return bool(self._com_obj.ModelPostStepCallbackEnabled)

    @model_post_step_callback_enabled.setter
    @ts_interface
    def model_post_step_callback_enabled(self, value: bool) -> None:
        self._com_obj.ModelPostStepCallbackEnabled = bool(value)

    @property
    @ts_interface
    def model_pre_interactive_callback_enabled(self) -> bool:
        return bool(self._com_obj.ModelPreInteractiveCallbackEnabled)

    @model_pre_interactive_callback_enabled.setter
    @ts_interface
    def model_pre_interactive_callback_enabled(self, value: bool) -> None:
        self._com_obj.ModelPreInteractiveCallbackEnabled = bool(value)

    @property
    @ts_interface
    def model_pre_step_callback_enabled(self) -> bool:
        return bool(self._com_obj.ModelPreStepCallbackEnabled)

    @model_pre_step_callback_enabled.setter
    @ts_interface
    def model_pre_step_callback_enabled(self, value: bool) -> None:
        self._com_obj.ModelPreStepCallbackEnabled = bool(value)

    @property
    @ts_interface
    def seq_file_post_error_callback_enabled(self) -> bool:
        return bool(self._com_obj.SeqFilePostErrorCallbackEnabled)

    @seq_file_post_error_callback_enabled.setter
    @ts_interface
    def seq_file_post_error_callback_enabled(self, value: bool) -> None:
        self._com_obj.SeqFilePostErrorCallbackEnabled = bool(value)

    @property
    @ts_interface
    def seq_file_post_fail_callback_enabled(self) -> bool:
        return bool(self._com_obj.SeqFilePostFailCallbackEnabled)

    @seq_file_post_fail_callback_enabled.setter
    @ts_interface
    def seq_file_post_fail_callback_enabled(self, value: bool) -> None:
        self._com_obj.SeqFilePostFailCallbackEnabled = bool(value)

    @property
    @ts_interface
    def seq_file_post_interactive_callback_enabled(self) -> bool:
        return bool(self._com_obj.SeqFilePostInteractiveCallbackEnabled)

    @seq_file_post_interactive_callback_enabled.setter
    @ts_interface
    def seq_file_post_interactive_callback_enabled(self, value: bool) -> None:
        self._com_obj.SeqFilePostInteractiveCallbackEnabled = bool(value)

    @property
    @ts_interface
    def seq_file_post_result_callback_enabled(self) -> bool:
        return bool(self._com_obj.SeqFilePostResultCallbackEnabled)

    @seq_file_post_result_callback_enabled.setter
    @ts_interface
    def seq_file_post_result_callback_enabled(self, value: bool) -> None:
        self._com_obj.SeqFilePostResultCallbackEnabled = bool(value)

    @property
    @ts_interface
    def seq_file_post_step_callback_enabled(self) -> bool:
        return bool(self._com_obj.SeqFilePostStepCallbackEnabled)

    @seq_file_post_step_callback_enabled.setter
    @ts_interface
    def seq_file_post_step_callback_enabled(self, value: bool) -> None:
        self._com_obj.SeqFilePostStepCallbackEnabled = bool(value)

    @property
    @ts_interface
    def seq_file_pre_interactive_callback_enabled(self) -> bool:
        return bool(self._com_obj.SeqFilePreInteractiveCallbackEnabled)

    @seq_file_pre_interactive_callback_enabled.setter
    @ts_interface
    def seq_file_pre_interactive_callback_enabled(self, value: bool) -> None:
        self._com_obj.SeqFilePreInteractiveCallbackEnabled = bool(value)

    @property
    @ts_interface
    def seq_file_pre_step_callback_enabled(self) -> bool:
        return bool(self._com_obj.SeqFilePreStepCallbackEnabled)

    @seq_file_pre_step_callback_enabled.setter
    @ts_interface
    def seq_file_pre_step_callback_enabled(self, value: bool) -> None:
        self._com_obj.SeqFilePreStepCallbackEnabled = bool(value)

    @property
    @ts_interface
    def station_post_error_callback_enabled(self) -> bool:
        return bool(self._com_obj.StationPostErrorCallbackEnabled)

    @station_post_error_callback_enabled.setter
    @ts_interface
    def station_post_error_callback_enabled(self, value: bool) -> None:
        self._com_obj.StationPostErrorCallbackEnabled = bool(value)

    @property
    @ts_interface
    def station_post_fail_callback_enabled(self) -> bool:
        return bool(self._com_obj.StationPostFailCallbackEnabled)

    @station_post_fail_callback_enabled.setter
    @ts_interface
    def station_post_fail_callback_enabled(self, value: bool) -> None:
        self._com_obj.StationPostFailCallbackEnabled = bool(value)

    @property
    @ts_interface
    def station_post_interactive_callback_enabled(self) -> bool:
        return bool(self._com_obj.StationPostInteractiveCallbackEnabled)

    @station_post_interactive_callback_enabled.setter
    @ts_interface
    def station_post_interactive_callback_enabled(self, value: bool) -> None:
        self._com_obj.StationPostInteractiveCallbackEnabled = bool(value)

    @property
    @ts_interface
    def station_post_result_callback_enabled(self) -> bool:
        return bool(self._com_obj.StationPostResultCallbackEnabled)

    @station_post_result_callback_enabled.setter
    @ts_interface
    def station_post_result_callback_enabled(self, value: bool) -> None:
        self._com_obj.StationPostResultCallbackEnabled = bool(value)

    @property
    @ts_interface
    def station_post_step_callback_enabled(self) -> bool:
        return bool(self._com_obj.StationPostStepCallbackEnabled)

    @station_post_step_callback_enabled.setter
    @ts_interface
    def station_post_step_callback_enabled(self, value: bool) -> None:
        self._com_obj.StationPostStepCallbackEnabled = bool(value)

    @property
    @ts_interface
    def station_pre_interactive_callback_enabled(self) -> bool:
        return bool(self._com_obj.StationPreInteractiveCallbackEnabled)

    @station_pre_interactive_callback_enabled.setter
    @ts_interface
    def station_pre_interactive_callback_enabled(self, value: bool) -> None:
        self._com_obj.StationPreInteractiveCallbackEnabled = bool(value)

    @property
    @ts_interface
    def station_pre_step_callback_enabled(self) -> bool:
        return bool(self._com_obj.StationPreStepCallbackEnabled)

    @station_pre_step_callback_enabled.setter
    @ts_interface
    def station_pre_step_callback_enabled(self, value: bool) -> None:
        self._com_obj.StationPreStepCallbackEnabled = bool(value)
