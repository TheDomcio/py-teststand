from __future__ import annotations

import typing
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COMWrapper, ts_interface

if TYPE_CHECKING:
    from py_teststand.execution.edit_args import EditArgs
    from py_teststand.execution.execution import Execution
    from py_teststand.execution.interactive_args import InteractiveArgs
    from py_teststand.sequence.sequence import Sequence
    from py_teststand.sequence.sequence_context import SequenceContext
    from py_teststand.sequence.sequence_file import SequenceFile
    from py_teststand.undo.undo_stack import UndoStack

    from .application_manager import ApplicationManager
    from .command import Command
    from .connections import (
        CaptionConnection,
        CommandConnection,
        ImageConnection,
        InsertionPaletteConnections,
        SelectedPropertyObjects,
        SelectedSequences,
        SequenceFileListConnection,
        SequenceListConnection,
        SequenceViewConnection,
        StepGroupListConnection,
        VariablesConnection,
    )
    from .entry_point import EntryPoints


from py_teststand.sequence.step_group import StepGroupMode
from py_teststand.ui.connections import SelectedSteps
from py_teststand.ui.styles import CaptionSource, ImageSource


class SequenceFileViewManagerConnections(COMWrapper):
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
    def image(self) -> ImageConnection:
        from .connections import ImageConnection

        return ImageConnection(self._com_obj.Image, self._engine_ref)

    @property
    @ts_interface
    def insertion_palettes(self) -> InsertionPaletteConnections:
        from .connections import InsertionPaletteConnections

        return InsertionPaletteConnections(self._com_obj.InsertionPalettes, self._engine_ref)

    @property
    @ts_interface
    def sequence_file_list(self) -> SequenceFileListConnection:
        from .connections import SequenceFileListConnection

        return SequenceFileListConnection(self._com_obj.SequenceFileList, self._engine_ref)

    @property
    @ts_interface
    def sequence_list(self) -> SequenceListConnection:
        from .connections import SequenceListConnection

        return SequenceListConnection(self._com_obj.SequenceList, self._engine_ref)

    @property
    @ts_interface
    def sequence_view(self) -> SequenceViewConnection:
        from .connections import SequenceViewConnection

        return SequenceViewConnection(self._com_obj.SequenceView, self._engine_ref)

    @property
    @ts_interface
    def step_group_list(self) -> StepGroupListConnection:
        from .connections import StepGroupListConnection

        return StepGroupListConnection(self._com_obj.StepGroupList, self._engine_ref)

    @property
    @ts_interface
    def variables(self) -> VariablesConnection:
        from .connections import VariablesConnection

        return VariablesConnection(self._com_obj.Variables, self._engine_ref)


class SequenceFileViewManager(COMWrapper):
    @property
    def events(self) -> typing.Any:
        from .events import SequenceFileViewMgrEventsSink, connect_events

        return connect_events(self, SequenceFileViewMgrEventsSink)

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
    def connections(self) -> SequenceFileViewManagerConnections:
        return SequenceFileViewManagerConnections(self._com_obj.Connections, self._engine_ref)

    @property
    @ts_interface
    def execution_entry_points(self) -> EntryPoints:
        from .entry_point import EntryPoints

        return EntryPoints(self._com_obj.ExecutionEntryPoints, self._engine_ref)

    @property
    @ts_interface
    def replace_sequence_file_on_close(self) -> bool:
        return bool(self._com_obj.ReplaceSequenceFileOnClose)

    @replace_sequence_file_on_close.setter
    @ts_interface
    def replace_sequence_file_on_close(self, value: bool) -> None:
        self._com_obj.ReplaceSequenceFileOnClose = value

    @property
    @ts_interface
    def selected_property_objects(self) -> SelectedPropertyObjects:
        from .connections import SelectedPropertyObjects

        return SelectedPropertyObjects(self._com_obj.SelectedPropertyObjects, self._engine_ref)

    @property
    @ts_interface
    def selected_sequences(self) -> SelectedSequences:
        from .connections import SelectedSequences

        return SelectedSequences(self._com_obj.SelectedSequences, self._engine_ref)

    @property
    @ts_interface
    def selected_steps(self) -> SelectedSteps:
        return SelectedSteps(self._com_obj.SelectedSteps, self._engine_ref)

    @property
    @ts_interface
    def sequence(self) -> Sequence | None:
        from py_teststand.sequence.sequence import Sequence

        com_seq = self._com_obj.Sequence
        return Sequence(com_seq, self._engine_ref) if com_seq else None

    @sequence.setter
    @ts_interface
    def sequence(self, value: Sequence | None) -> None:
        self._com_obj.Sequence = getattr(value, "_com_obj", value)

    @property
    @ts_interface
    def sequence_file(self) -> SequenceFile | None:
        from py_teststand.sequence.sequence_file import SequenceFile

        com_file = self._com_obj.SequenceFile
        return SequenceFile(com_file, self._engine_ref) if com_file else None

    @sequence_file.setter
    @ts_interface
    def sequence_file(self, value: SequenceFile | None) -> None:
        self._com_obj.SequenceFile = getattr(value, "_com_obj", value)

    @property
    @ts_interface
    def step_group(self) -> int:
        return int(self._com_obj.StepGroup)

    @step_group.setter
    @ts_interface
    def step_group(self, value: int) -> None:
        self._com_obj.StepGroup = value

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
    def undo_stack(self) -> UndoStack | None:
        from py_teststand.undo.undo_stack import UndoStack

        com_undo = self._com_obj.UndoStack
        return UndoStack(com_undo, self._engine_ref) if com_undo else None

    @property
    @ts_interface
    def user_data(self) -> typing.Any:
        return self._com_obj.UserData

    @user_data.setter
    @ts_interface
    def user_data(self, value: typing.Any) -> None:
        self._com_obj.UserData = value

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
        button_action_style: int = 0,
    ) -> CommandConnection:
        from .connections import CommandConnection

        return CommandConnection(
            self._com_obj.ConnectCommand(
                control,
                command_kind,
                index,
                options,
                button_action_style,
            ),
            self._engine_ref,
        )

    @ts_interface
    def connect_image(self, control: typing.Any, source: int | ImageSource) -> ImageConnection:
        from .connections import ImageConnection

        return ImageConnection(self._com_obj.ConnectImage(control, int(source)), self._engine_ref)

    @ts_interface
    def connect_insertion_palette(self, control: typing.Any) -> typing.Any:
        return self._com_obj.ConnectInsertionPalette(control)

    @ts_interface
    def connect_sequence_file_list(self, control: typing.Any) -> SequenceFileListConnection:
        from .connections import SequenceFileListConnection

        return SequenceFileListConnection(
            self._com_obj.ConnectSequenceFileList(control),
            self._engine_ref,
        )

    @ts_interface
    def connect_sequence_list(self, control: typing.Any) -> SequenceListConnection:
        from .connections import SequenceListConnection

        return SequenceListConnection(self._com_obj.ConnectSequenceList(control), self._engine_ref)

    @ts_interface
    def connect_sequence_view(self, control: typing.Any) -> SequenceViewConnection:
        from .connections import SequenceViewConnection

        return SequenceViewConnection(self._com_obj.ConnectSequenceView(control), self._engine_ref)

    @ts_interface
    def connect_step_group_list(self, control: typing.Any) -> StepGroupListConnection:
        from .connections import StepGroupListConnection

        return StepGroupListConnection(
            self._com_obj.ConnectStepGroupList(control),
            self._engine_ref,
        )

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
    def run(self) -> Execution:
        from py_teststand.execution.execution import Execution

        return Execution(self._com_obj.Run(), self._engine_ref)

    @ts_interface
    def run_selected_steps(self, interactive_args: InteractiveArgs | None = None) -> Execution:
        from py_teststand.execution.execution import Execution

        raw_args = (
            getattr(interactive_args, "_com_obj", interactive_args) if interactive_args else None
        )
        return Execution(self._com_obj.RunSelectedSteps(raw_args), self._engine_ref)

    @ts_interface
    def set_sequence_and_group(self, sequence: Sequence, group: int) -> None:
        raw_seq = getattr(sequence, "_com_obj", sequence)
        self._com_obj.SetSequenceAndGroup(raw_seq, group)
