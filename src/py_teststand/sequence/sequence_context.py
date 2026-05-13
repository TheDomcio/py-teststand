from __future__ import annotations

import typing
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import ts_interface
from py_teststand.execution.interactive_args import InteractiveContext
from py_teststand.property.property_object import PropertyObject
from py_teststand.sequence.sequence import Sequence
from py_teststand.sequence.sequence_file import SequenceFile

if TYPE_CHECKING:
    from py_teststand.core.engine import Engine
    from py_teststand.execution.execution import Execution
    from py_teststand.execution.report import Report
    from py_teststand.execution.thread import Thread
    from py_teststand.sequence.step import Step


class SequenceContext(PropertyObject):
    def __init__(self, com_obj: typing.Any, engine: typing.Any = None) -> None:

        super().__init__(com_obj, engine)

    @property
    @ts_interface
    def engine(self) -> Engine:
        resolved = self._engine_ref() if self._engine_ref is not None else None
        if resolved is not None:
            return typing.cast("Engine", resolved)
        from py_teststand.core.engine import Engine

        return Engine(self._com_obj.Engine)

    @property
    @ts_interface
    def engine_as_dispatch(self) -> typing.Any:
        return self._com_obj.EngineAsDispatch

    @property
    @ts_interface
    def execution(self) -> Execution:
        from py_teststand.execution.execution import Execution

        return Execution(self._com_obj.Execution, self._engine_ref)

    @property
    @ts_interface
    def call_stack_name(self) -> str:
        return str(self._com_obj.CallStackName)

    @property
    @ts_interface
    def caller_discards_results(self) -> bool:
        return bool(self._com_obj.CallerDiscardsResults)

    @ts_interface
    def get_run_time_error_message_ex(self) -> tuple[str, str, str]:
        return self._com_obj.GetRunTimeErrorMessageEx()

    @ts_interface
    def get_run_time_error_win_help_info(self) -> typing.Any:
        return str(self._com_obj.GetRunTimeErrorWinHelpInfo())

    @property
    @ts_interface
    def error_reported(self) -> bool:
        return bool(self._com_obj.ErrorReported)

    @error_reported.setter
    @ts_interface
    def error_reported(self, value: bool) -> None:
        self._com_obj.ErrorReported = value

    @property
    @ts_interface
    def application_is_editor(self) -> bool:
        return bool(self._com_obj.ApplicationIsEditor)

    @property
    @ts_interface
    def call_stack_depth(self) -> int:
        return int(self._com_obj.CallStackDepth)

    @property
    @ts_interface
    def goto_cleanup(self) -> bool:
        return bool(self._com_obj.GotoCleanup)

    @goto_cleanup.setter
    @ts_interface
    def goto_cleanup(self, value: bool) -> None:
        self._com_obj.GotoCleanup = value

    @ts_interface
    def is_interactive_step(self, step_index: int) -> bool:
        return bool(self._com_obj.IsInteractiveStep(int(step_index)))

    @ts_interface
    def is_step_excluded_from_execution(self, step: Step) -> bool:
        return bool(self._com_obj.IsStepExcludedFromExecution(step._com_obj))

    @ts_interface
    def new_execution(
        self,
        sequence_file: typing.Any,
        sequence_name: str,
        process_model: typing.Any = None,
        break_at_first_step: bool = False,
        synchronous: bool = False,
        execution_type_mask: int = 0,
        sequence_args: typing.Any = None,
    ) -> Execution:
        from py_teststand.execution.execution import Execution

        sf_com = getattr(sequence_file, "_com_obj", sequence_file) if sequence_file else None
        pm_com = getattr(process_model, "_com_obj", process_model) if process_model else None
        sa_com = getattr(sequence_args, "_com_obj", sequence_args) if sequence_args else None

        raw_exec = self._com_obj.NewExecution(
            sf_com,
            sequence_name,
            pm_com,
            break_at_first_step,
            synchronous,
            execution_type_mask,
            sa_com,
        )
        return Execution(raw_exec, self._engine_ref)

    @ts_interface
    def get_multiple_values(self, lookup_string: str, elem: int = 0) -> int:
        return int(self._com_obj.GetMultipleValues(str(lookup_string), int(elem)))

    @ts_interface
    def set_multiple_values(self, lookup_string: str, elem: int, multiple_values: int) -> None:
        self._com_obj.SetMultipleValues(str(lookup_string), int(elem), int(multiple_values))

    @property
    @ts_interface
    def is_process_model(self) -> bool:
        return bool(self._com_obj.IsProcessModel)

    @property
    @ts_interface
    def in_interactive_mode(self) -> bool:
        return bool(self._com_obj.InInteractiveMode)

    @property
    @ts_interface
    def loop_index(self) -> typing.Any:
        return int(self._com_obj.LoopIndex)

    @property
    @ts_interface
    def loop_num_failed(self) -> int:
        return int(self._com_obj.LoopNumFailed)

    @property
    @ts_interface
    def loop_num_iterations(self) -> int:
        return int(self._com_obj.LoopNumIterations)

    @property
    @ts_interface
    def loop_num_passed(self) -> int:
        return int(self._com_obj.LoopNumPassed)

    @property
    @ts_interface
    def main(self) -> SequenceContext:
        return SequenceContext(self._com_obj.Main, self._engine_ref)

    @property
    @ts_interface
    def report(self) -> Report:
        from py_teststand.execution.report import Report

        return Report(self._com_obj.Report, self._engine_ref)

    @property
    @ts_interface
    def can_trace(self) -> bool:
        return bool(self._com_obj.CanTrace)

    @property
    @ts_interface
    def sequence_index(self) -> int:
        return int(self._com_obj.SequenceIndex)

    @property
    @ts_interface
    def step_index(self) -> int:
        return int(self._com_obj.StepIndex)

    @property
    @ts_interface
    def next_step(self) -> Step:
        from py_teststand.sequence.step import Step

        return Step(self._com_obj.NextStep, engine=self._engine_ref)

    @property
    @ts_interface
    def next_step_index(self) -> int:
        return int(self._com_obj.NextStepIndex)

    @property
    @ts_interface
    def num_steps_executed(self) -> int:
        return int(self._com_obj.NumStepsExecuted)

    @property
    @ts_interface
    def previous_step_index(self) -> int:
        return int(self._com_obj.PreviousStepIndex)

    @property
    @ts_interface
    def previous_step(self) -> Step:
        from py_teststand.sequence.step import Step

        return Step(self._com_obj.PreviousStep, engine=self._engine_ref)

    @property
    @ts_interface
    def process_model_client(self) -> SequenceFile:
        return SequenceFile(self._com_obj.ProcessModelClient, engine=self._engine_ref)

    @property
    @ts_interface
    def selected_execution(self) -> Execution | None:
        from py_teststand.execution.execution import Execution

        com_exec = self._com_obj.SelectedExecution
        return Execution(com_exec, self._engine_ref) if com_exec else None

    @property
    @ts_interface
    def selected_file(self) -> SequenceFile | None:
        com_file = self._com_obj.SelectedFile
        return SequenceFile(com_file, engine=self._engine_ref) if com_file else None

    @property
    @ts_interface
    def selected_property_object_file(self) -> typing.Any:
        return self._com_obj.SelectedPropertyObjectFile

    @property
    @ts_interface
    def selected_property_objects(self) -> list[PropertyObject]:
        raw = self._com_obj.SelectedPropertyObjects
        if raw is None:
            return []
        return [PropertyObject(obj, self._engine_ref) for obj in raw]

    @property
    @ts_interface
    def selected_sequences(self) -> list[Sequence]:
        raw = self._com_obj.SelectedSequences
        if raw is None:
            return []
        return [Sequence(obj, engine=self._engine_ref) for obj in raw]

    @property
    @ts_interface
    def selected_step_group(self) -> typing.Any:
        return int(self._com_obj.SelectedStepGroup)

    @property
    @ts_interface
    def selected_steps(self) -> list[Step]:
        from py_teststand.sequence.step import Step

        raw = self._com_obj.SelectedSteps
        if raw is None:
            return []
        return [Step(obj, engine=self._engine_ref) for obj in raw]

    @property
    @ts_interface
    def id(self) -> typing.Any:
        return self._com_obj.Id

    @property
    @ts_interface
    def thread(self) -> Thread:
        from py_teststand.execution.thread import Thread

        return Thread(self._com_obj.Thread, self._engine_ref)

    @property
    @ts_interface
    def caller(self) -> SequenceContext | None:
        com_caller = getattr(self._com_obj, "Caller", None)
        return SequenceContext(com_caller, self._engine_ref) if com_caller else None

    @property
    @ts_interface
    def sequence(self) -> Sequence:
        return Sequence(self._com_obj.Sequence, engine=self._engine_ref)

    @property
    @ts_interface
    def sequence_file(self) -> SequenceFile:
        return SequenceFile(self._com_obj.SequenceFile, engine=self._engine_ref)

    @property
    @ts_interface
    def root(self) -> SequenceContext:
        return SequenceContext(self._com_obj.Root, self._engine_ref)

    @property
    @ts_interface
    def run_time_error_message(self) -> str:
        return str(self._com_obj.RunTimeErrorMessage)

    @property
    @ts_interface
    def interactive_context(self) -> InteractiveContext:
        return InteractiveContext(self._com_obj.InteractiveContext, self._engine_ref)

    @property
    @ts_interface
    def run_state(self) -> PropertyObject:
        return PropertyObject(self._com_obj.RunState, self._engine_ref)

    @property
    @ts_interface
    def locals(self) -> PropertyObject:
        return PropertyObject(self._com_obj.Locals, self._engine_ref)

    @property
    @ts_interface
    def parameters(self) -> PropertyObject:
        return PropertyObject(self._com_obj.Parameters, self._engine_ref)

    @property
    @ts_interface
    def file_globals(self) -> PropertyObject:
        return PropertyObject(self._com_obj.FileGlobals, self._engine_ref)

    @property
    @ts_interface
    def sequence_error_code(self) -> int:
        return int(self._com_obj.SequenceErrorCode)

    @sequence_error_code.setter
    @ts_interface
    def sequence_error_code(self, value: int) -> None:
        self._com_obj.SequenceErrorCode = value

    @property
    @ts_interface
    def sequence_error_message(self) -> str:
        return str(self._com_obj.SequenceErrorMessage)

    @sequence_error_message.setter
    @ts_interface
    def sequence_error_message(self, value: str) -> None:
        self._com_obj.SequenceErrorMessage = value

    @property
    @ts_interface
    def sequence_error_occurred(self) -> bool:
        return bool(self._com_obj.SequenceErrorOccurred)

    @sequence_error_occurred.setter
    @ts_interface
    def sequence_error_occurred(self, value: bool) -> None:
        self._com_obj.SequenceErrorOccurred = value

    @property
    @ts_interface
    def sequence_failed(self) -> bool:
        return bool(self._com_obj.SequenceFailed)

    @sequence_failed.setter
    @ts_interface
    def sequence_failed(self, value: bool) -> None:
        self._com_obj.SequenceFailed = value

    @property
    @ts_interface
    def station_globals(self) -> PropertyObject:
        return PropertyObject(self._com_obj.StationGlobals, self._engine_ref)

    @property
    @ts_interface
    def calling_step(self) -> Step | None:
        from py_teststand.sequence.step import Step

        com_step = self._com_obj.CallingStep
        return Step(com_step, self._engine_ref) if com_step else None

    @ts_interface
    def get_internal_option(self, option: int) -> typing.Any:
        return self._com_obj.GetInternalOption(option)

    @ts_interface
    def set_internal_option(self, option: int, value: typing.Any) -> None:
        self._com_obj.SetInternalOption(option, value)

    @ts_interface
    def set_step_index(self, group: int, index: int) -> None:
        self._com_obj.SetStepIndex(int(group), index)

    @property
    @ts_interface
    def step_group(self) -> typing.Any:
        return int(self._com_obj.StepGroup)

    @step_group.setter
    @ts_interface
    def step_group(self, value: int) -> None:
        self._com_obj.StepGroup = value

    @property
    @ts_interface
    def step_group_started_interactive_exe(self) -> bool:
        return bool(self._com_obj.StepGroupStartedInteractiveExe)

    @property
    @ts_interface
    def tracing(self) -> bool:
        return bool(self._com_obj.Tracing)

    @tracing.setter
    @ts_interface
    def tracing(self, value: bool) -> None:
        self._com_obj.Tracing = value

    @property
    @ts_interface
    def step(self) -> Step:
        from py_teststand.sequence.step import Step

        return Step(self._com_obj.Step, engine=self._engine_ref)
