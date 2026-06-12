from __future__ import annotations

import typing
from enum import IntEnum
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COMWrapper, ts_interface

if TYPE_CHECKING:
    from py_teststand.execution.edit_args import EditArgs
    from py_teststand.execution.execution import Execution
    from py_teststand.execution.interactive_args import InteractiveArgs
    from py_teststand.execution.thread import Thread
    from py_teststand.sequence.sequence_context import SequenceContext

    from .application_manager import ApplicationManager, RunStates, TerminationStates
    from .command import Command
    from .connections import (
        CallStackConnection,
        CaptionConnection,
        CommandConnection,
        ExecutionListConnection,
        ExecutionViewConnection,
        ImageConnection,
        NumericConnection,
        ReportViewConnection,
        SelectedPropertyObjects,
        ThreadListConnection,
        VariablesConnection,
    )
    from .entry_point import EntryPoints


from py_teststand.sequence.step_group import StepGroupMode
from py_teststand.ui.command import ExecutionViewConnectionOption
from py_teststand.ui.connections import SelectedSteps
from py_teststand.ui.styles import CaptionSource, ImageSource, NumericSource


class ButtonActionStyle(IntEnum):
    PushButton = 0
    ToggleButton = 1


class ExecutionViewManagerConnections(COMWrapper):
    @property
    @ts_interface
    def call_stack(self) -> CallStackConnection:
        from .connections import CallStackConnection

        return CallStackConnection(self._com_obj.CallStack, self._engine_ref)

    @property
    @ts_interface
    def caption(self) -> CaptionConnection:
        from .connections import CaptionConnection

        return CaptionConnection(self._com_obj.Caption, self._engine_ref)

    @property
    @ts_interface
    def command(self) -> CommandConnection:
        from .connections import CommandConnection

        return CommandConnection(self._com_obj.Command, self._engine_ref)

    @property
    @ts_interface
    def execution_list(self) -> ExecutionListConnection:
        from .connections import ExecutionListConnection

        return ExecutionListConnection(self._com_obj.ExecutionList, self._engine_ref)

    @property
    @ts_interface
    def execution_view(self) -> ExecutionViewConnection:
        from .connections import ExecutionViewConnection

        return ExecutionViewConnection(self._com_obj.ExecutionView, self._engine_ref)

    @property
    @ts_interface
    def image(self) -> ImageConnection:
        from .connections import ImageConnection

        return ImageConnection(self._com_obj.Image, self._engine_ref)

    @property
    @ts_interface
    def numeric(self) -> NumericConnection:
        from .connections import NumericConnection

        return NumericConnection(self._com_obj.Numeric, self._engine_ref)

    @property
    @ts_interface
    def report_view(self) -> ReportViewConnection:
        from .connections import ReportViewConnection

        return ReportViewConnection(self._com_obj.ReportView, self._engine_ref)

    @property
    @ts_interface
    def thread_list(self) -> ThreadListConnection:
        from .connections import ThreadListConnection

        return ThreadListConnection(self._com_obj.ThreadList, self._engine_ref)

    @property
    @ts_interface
    def variables(self) -> VariablesConnection:
        from .connections import VariablesConnection

        return VariablesConnection(self._com_obj.Variables, self._engine_ref)


class ExecutionViewManager(COMWrapper):
    @property
    @ts_interface
    def application_mgr(self) -> ApplicationManager:
        from .application_manager import ApplicationManager

        return ApplicationManager(self._com_obj.ApplicationMgr, self._engine_ref)

    @property
    @ts_interface
    def configuration_entry_points(self) -> EntryPoints:
        from .entry_point import EntryPoints

        return EntryPoints(self._com_obj.ConfigurationEntryPoints, self._engine_ref)

    @property
    @ts_interface
    def connections(self) -> ExecutionViewManagerConnections:
        return ExecutionViewManagerConnections(self._com_obj.Connections, self._engine_ref)

    @property
    @ts_interface
    def execution(self) -> Execution | None:
        from py_teststand.execution.execution import Execution

        com_exec = self._com_obj.Execution
        return Execution(com_exec, self._engine_ref) if com_exec else None

    @execution.setter
    @ts_interface
    def execution(self, value: Execution | None) -> None:
        self._com_obj.Execution = getattr(value, "_com_obj", value)

    @property
    @ts_interface
    def execution_entry_points(self) -> EntryPoints:
        from .entry_point import EntryPoints

        return EntryPoints(self._com_obj.ExecutionEntryPoints, self._engine_ref)

    @property
    @ts_interface
    def replace_execution_on_close(self) -> bool:
        return bool(self._com_obj.ReplaceExecutionOnClose)

    @replace_execution_on_close.setter
    @ts_interface
    def replace_execution_on_close(self, value: bool) -> None:
        self._com_obj.ReplaceExecutionOnClose = value

    @property
    @ts_interface
    def run_state(self) -> RunStates:
        from .application_manager import RunStates

        return RunStates(self._com_obj.RunState)

    @property
    @ts_interface
    def selected_property_objects(self) -> SelectedPropertyObjects:
        from .connections import SelectedPropertyObjects

        return SelectedPropertyObjects(self._com_obj.SelectedPropertyObjects, self._engine_ref)

    @property
    @ts_interface
    def selected_steps(self) -> SelectedSteps:
        return SelectedSteps(self._com_obj.SelectedSteps, self._engine_ref)

    @property
    @ts_interface
    def sequence_context(self) -> SequenceContext | None:
        from py_teststand.sequence.sequence_context import SequenceContext

        com_ctx = self._com_obj.SequenceContext
        return SequenceContext(com_ctx, self._engine_ref) if com_ctx else None

    @sequence_context.setter
    @ts_interface
    def sequence_context(self, value: SequenceContext | None) -> None:
        self._com_obj.SequenceContext = getattr(value, "_com_obj", value)

    @property
    @ts_interface
    def step_group_mode(self) -> StepGroupMode:
        return StepGroupMode(self._com_obj.StepGroupMode)

    @step_group_mode.setter
    @ts_interface
    def step_group_mode(self, value: StepGroupMode | int) -> None:
        self._com_obj.StepGroupMode = int(value)

    @property
    @ts_interface
    def termination_state(self) -> TerminationStates:
        from .application_manager import TerminationStates

        return TerminationStates(self._com_obj.TerminationState)

    @property
    @ts_interface
    def thread(self) -> Thread | None:
        from py_teststand.execution.thread import Thread

        com_thread = self._com_obj.Thread
        return Thread(com_thread, self._engine_ref) if com_thread else None

    @thread.setter
    @ts_interface
    def thread(self, value: Thread | None) -> None:
        self._com_obj.Thread = getattr(value, "_com_obj", value)

    @property
    @ts_interface
    def user_data(self) -> typing.Any:
        return self._com_obj.UserData

    @user_data.setter
    @ts_interface
    def user_data(self, value: typing.Any) -> None:
        self._com_obj.UserData = value

    @ts_interface
    def abort_execution(self) -> None:
        self._com_obj.AbortExecution()

    @ts_interface
    def break_execution(self) -> None:
        self._com_obj.BreakExecution()

    @ts_interface
    def build_edit_args(self) -> EditArgs:
        from py_teststand.execution.edit_args import EditArgs

        return EditArgs(self._com_obj.BuildEditArgs(), self._engine_ref)

    @ts_interface
    def build_interactive_args(
        self,
        create_loop_args: bool,
        cancel: bool = False,
    ) -> tuple[InteractiveArgs, bool]:
        from py_teststand.execution.interactive_args import InteractiveArgs

        res, cancel_out = self._com_obj.BuildInteractiveArgs(create_loop_args, cancel)
        return InteractiveArgs(res, self._engine_ref), bool(cancel_out)

    @ts_interface
    def connect_call_stack(self, control: typing.Any) -> CallStackConnection:
        from .connections import CallStackConnection

        return CallStackConnection(self._com_obj.ConnectCallStack(control), self._engine_ref)

    @ts_interface
    def connect_caption(
        self,
        control: typing.Any,
        source: int | CaptionSource,
    ) -> CaptionConnection:
        from .connections import CaptionConnection

        return CaptionConnection(
            self._com_obj.ConnectCaption(control, int(source)),
            self._engine_ref,
        )

    @ts_interface
    def connect_command(
        self,
        control: typing.Any,
        command_kind: int,
        index: int = 0,
        options: int = 0,
        button_action_style: ButtonActionStyle | int = 0,
    ) -> CommandConnection:
        from .connections import CommandConnection

        return CommandConnection(
            self._com_obj.ConnectCommand(
                control,
                command_kind,
                index,
                options,
                int(button_action_style),
            ),
            self._engine_ref,
        )

    @ts_interface
    def connect_execution_list(self, control: typing.Any) -> ExecutionListConnection:
        from .connections import ExecutionListConnection

        return ExecutionListConnection(
            self._com_obj.ConnectExecutionList(control),
            self._engine_ref,
        )

    @ts_interface
    def connect_execution_view(
        self,
        control: typing.Any,
        options: ExecutionViewConnectionOption | int = 0,
    ) -> ExecutionViewConnection:
        from .connections import ExecutionViewConnection

        return ExecutionViewConnection(
            self._com_obj.ConnectExecutionView(control, int(options)),
            self._engine_ref,
        )

    @ts_interface
    def connect_image(self, control: typing.Any, source: int | ImageSource) -> ImageConnection:
        from .connections import ImageConnection

        return ImageConnection(self._com_obj.ConnectImage(control, int(source)), self._engine_ref)

    @ts_interface
    def connect_numeric(
        self,
        control: typing.Any,
        source: int | NumericSource,
    ) -> NumericConnection:
        from .connections import NumericConnection

        return NumericConnection(
            self._com_obj.ConnectNumeric(control, int(source)),
            self._engine_ref,
        )

    @ts_interface
    def connect_report_view(self, control: typing.Any) -> ReportViewConnection:
        from .connections import ReportViewConnection

        return ReportViewConnection(self._com_obj.ConnectReportView(control), self._engine_ref)

    @ts_interface
    def connect_thread_list(self, control: typing.Any) -> ThreadListConnection:
        from .connections import ThreadListConnection

        return ThreadListConnection(self._com_obj.ConnectThreadList(control), self._engine_ref)

    @ts_interface
    def connect_variables(self, control: typing.Any) -> VariablesConnection:
        from .connections import VariablesConnection

        return VariablesConnection(self._com_obj.ConnectVariables(control), self._engine_ref)

    @ts_interface
    def get_caption_text(
        self,
        caption_source: int | CaptionSource,
        long_name: bool,
        format_expression: str = "",
    ) -> str:
        return str(self._com_obj.GetCaptionText(int(caption_source), long_name, format_expression))

    @ts_interface
    def get_command(self, command_kind: int, index: int = 0) -> Command | None:
        from .command import Command

        com_cmd = self._com_obj.GetCommand(command_kind, index)
        return Command(com_cmd, self._engine_ref) if com_cmd else None

    @ts_interface
    def get_image_name(self, image_source: int | ImageSource) -> str:
        return str(self._com_obj.GetImageName(int(image_source)))

    @ts_interface
    def get_numeric_value(self, numeric_source: int | NumericSource) -> float:
        return float(self._com_obj.GetNumericValue(int(numeric_source)))

    @ts_interface
    def loop_on_selected_steps(self, interactive_args: InteractiveArgs | None = None) -> Execution:
        from py_teststand.execution.execution import Execution

        raw_args = (
            getattr(interactive_args, "_com_obj", interactive_args) if interactive_args else None
        )
        return Execution(self._com_obj.LoopOnSelectedSteps(raw_args), self._engine_ref)

    @ts_interface
    def new_edit_context(self) -> SequenceContext:
        from py_teststand.sequence.sequence_context import SequenceContext

        return SequenceContext(self._com_obj.NewEditContext(), self._engine_ref)

    @ts_interface
    def refresh(self) -> None:
        self._com_obj.Refresh()

    @ts_interface
    def refresh_step(self, reserved: int = 0) -> None:
        self._com_obj.RefreshStep(reserved)

    @ts_interface
    def refresh_step_ex(self, update_type: int, reserved: int = 0) -> None:
        self._com_obj.RefreshStepEx(update_type, reserved)

    @ts_interface
    def restart_execution(self) -> None:
        self._com_obj.RestartExecution()

    @ts_interface
    def resume_execution(self) -> None:
        self._com_obj.ResumeExecution()

    @ts_interface
    def run_selected_steps(self, interactive_args: InteractiveArgs | None = None) -> Execution:
        from py_teststand.execution.execution import Execution

        raw_args = (
            getattr(interactive_args, "_com_obj", interactive_args) if interactive_args else None
        )
        return Execution(self._com_obj.RunSelectedSteps(raw_args), self._engine_ref)

    @ts_interface
    def terminate_execution(self) -> None:
        self._com_obj.TerminateExecution()
