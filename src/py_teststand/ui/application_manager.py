from __future__ import annotations

import typing
from enum import IntEnum
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.core.engine import EditKind
from py_teststand.execution.execution import ExecutionRunState, ExecutionTerminationState
from py_teststand.ui.styles import CaptionSource, ImageSource, ShortcutModifier

if TYPE_CHECKING:
    from py_teststand.core.engine import Engine
    from py_teststand.messaging.ui_message import UIMessage
    from py_teststand.property.property_object_file import PropertyObjectFile
    from py_teststand.sequence.sequence_file import SequenceFile
    from py_teststand.undo.undo_stack import UndoStack

    from .command import Command, Commands
    from .connections import (
        ApplicationMgrConnections,
        CaptionConnection,
        CommandConnection,
        Executions,
        MRUFiles,
        SequenceFiles,
        Strings,
    )
    from .execution_view_manager import ExecutionViewManager
    from .sequence_file_view_manager import SequenceFileViewManager


class AutomaticallyReloadModifiedFilesOption(IntEnum):
    DoNotReload = 1
    OnTimer = 2
    OnActivateApplication = 3


class CommandKind(IntEnum):
    Abort = 75
    AbortAll = 78
    Break = 71
    BreakAll = 76
    BreakOnFirstStep = 50
    BreakOnSequenceFailure = 52
    BreakOnStepFailure = 51
    BreakpointSubmenu = 85
    BreakResume = 72
    Close = 21
    CloseAll = 22
    CloseCompletedExecutions = 23
    ConfigurationEntryPointDefaultMenuInsertionMarker = 113
    ConfigurationEntryPointInsertionMarker = 112
    ConfigurationEntryPoints_Set = 145
    ConfigureAdapters = 90
    ConfigureEngineEnvironment = 94
    ConfigureExternalViewers = 93
    ConfigureSearchDirectories = 92
    ConfigureSequenceViews = 149
    ConfigureStationOptions = 91
    Container = 1
    Custom = 3
    CustomizeTools = 101
    DefaultConfigureMenu_Set = 124
    DefaultDebugMenu_Set = 123
    DefaultEditMenu_Set = 128
    DefaultExecuteMenu_Set = 121
    DefaultFileMenu_Set = 120
    DefaultHelpMenu_Set = 440
    DefaultListBarContextMenu_Set = 127
    DefaultSequenceListContextMenu_Set = 129
    DefaultSequenceViewContextMenu_Set = 126
    DefaultToolsMenu_Set = 125
    DisplayBreakpointsAndWatchExpressions = 80
    DisplayBreakpointSettings = 81
    Edit_AdvancedSequenceListSubmenu = 451
    Edit_Attributes = 450
    Edit_Copy = 204
    Edit_Cut = 203
    Edit_Delete = 206
    Edit_EditCode = 216
    Edit_EditPaths = 223
    Edit_EditStep = 217
    Edit_EditSteps_Set = 341
    Edit_EditStepsSubmenu = 301
    Edit_EncapsulateSelectedSteps = 224
    Edit_EncapsulateSelectedSteps_Set = 343
    Edit_EncapsulateSelectedStepsSubmenu = 303
    Edit_InsertSequence = 221
    Edit_InsertStep = 207
    Edit_InsertSteps_Set = 340
    Edit_InsertStepsSubmenu = 300
    Edit_NewSequenceFile = 211
    Edit_Paste = 205
    Edit_Preconditions = 218
    Edit_Redo = 201
    Edit_Rename = 202
    Edit_Save = 208
    Edit_SaveAll = 210
    Edit_SaveAs = 209
    Edit_SelectDefaultAdapter = 220
    Edit_SelectDefaultAdapters_Set = 342
    Edit_SelectDefaultAdaptersSubmenu = 302
    Edit_SequenceFileCallbacks = 222
    Edit_SequenceFileProperties = 214
    Edit_SequenceProperties = 213
    Edit_SpecifyModule = 215
    Edit_StepProperties = 212
    Edit_Undo = 200
    ExecutionEntryPointDefaultMenuInsertionMarker = 111
    ExecutionEntryPointInsertionMarker = 110
    ExecutionEntryPoints_Set = 141
    Exit = 30
    LockUnlock = 148
    Login = 25
    LoginLogout = 27
    Logout = 26
    LoopEntryPointOnSelectedSteps = 43
    LoopOnSelectedSteps = 48
    LoopOnSelectedStepsUsingEntryPoints_Set = 144
    LoopOnSelectedStepsUsingEntryPointsSubmenu = 49
    MRUFile = 29
    MRUFiles_Set = 140
    NotACommand = 0
    OpenSequenceFile = 20
    OpenSequenceFiles = 147
    OpenWorkspaceBrowser = 24
    Restart = 40
    Resume = 66
    ResumeAll = 79
    RunCurrentSequence = 44
    RunEntryPoint = 41
    RunEntryPointOnSelectedSteps = 42
    RunModeForceFail = 63
    RunModeForcePass = 62
    RunModeNormal = 65
    RunModeSkip = 64
    RunSelectedSteps = 46
    RunSelectedStepsUsingEntryPoints_Set = 143
    RunSelectedStepsUsingEntryPointsSubmenu = 47
    RunSequences_Set = 142
    RunSpecificSequence = 45
    SelectAll = 219
    Separator = 2
    SequenceViewConfiguration = 116
    SequenceViewConfigurations_Set = 139
    SequenceViewConfigurationsSubmenu = 118
    SetNextStep = 70
    SetRunModeSubmenu = 61
    ShowExamples = 453
    ShowGettingStarted = 454
    ShowGuideToDocumentation = 421
    ShowHelpTopic = 422
    ShowInList = 400
    ShowInVariables = 401
    ShowPatents = 425
    ShowTestStandDiscussionForum = 424
    ShowTestStandHelp = 420
    ShowTestStandWebResources = 423
    ShowUpdateService = 452
    StepInto = 67
    StepOut = 69
    StepOver = 68
    Terminate = 73
    TerminateAll = 77
    TerminateRestart = 74
    ToggleBreakpoint = 60
    ToolItem = 100
    Tools_Set = 146
    TracingEnabled = 53
    UnloadAllModules = 28
    UnloadStepModule = 455


RunStates = ExecutionRunState
TerminationStates = ExecutionTerminationState


class QueryCloseExecutionOption(IntEnum):
    Abort = 2
    AutoCloseWhenDone = 3
    Cancel = 4
    Hide = 5
    ShowDialog = 0
    Terminate = 1


class QueryReloadSequenceFileOption(IntEnum):
    Cancel = 2
    Prompt = 0
    Reload = 1


class QueryShutdownOption(IntEnum):
    Cancel = 2
    Continue = 1
    ShowDialog = 0


class ApplicationManager(COMWrapper):
    def __enter__(self) -> ApplicationManager:
        return self

    def __exit__(self, exc_type: typing.Any, exc_val: typing.Any, exc_tb: typing.Any) -> None:
        try:
            self.shutdown()
        except Exception:
            pass
        self.release()

    @property
    def events(self) -> typing.Any:
        from .events import ApplicationMgrEventsSink, connect_events

        return connect_events(self, ApplicationMgrEventsSink)

    @property
    @ts_interface
    def is_started(self) -> bool:
        return bool(self._com_obj.IsStarted)

    @property
    @ts_interface
    def login_on_start(self) -> bool:
        return bool(self._com_obj.LoginOnStart)

    @login_on_start.setter
    @ts_interface
    def login_on_start(self, value: bool) -> None:
        self._com_obj.LoginOnStart = value

    @property
    @ts_interface
    def login_logout_running(self) -> bool:
        return bool(self._com_obj.LoginLogoutRunning)

    @property
    @ts_interface
    def login_running(self) -> bool:
        return bool(self._com_obj.LoginRunning)

    @property
    @ts_interface
    def logout_running(self) -> bool:
        return bool(self._com_obj.LogoutRunning)

    @property
    @ts_interface
    def is_editor(self) -> bool:
        return bool(self._com_obj.IsEditor)

    @is_editor.setter
    @ts_interface
    def is_editor(self, value: bool) -> None:
        self._com_obj.IsEditor = value

    @property
    @ts_interface
    def executing(self) -> bool:
        return bool(self._com_obj.Executing)

    @property
    @ts_interface
    def is_shutting_down(self) -> bool:
        return bool(self._com_obj.IsShuttingDown)

    @property
    @ts_interface
    def use_step_list_configurations(self) -> bool:
        return bool(self._com_obj.UseStepListConfigurations)

    @use_step_list_configurations.setter
    @ts_interface
    def use_step_list_configurations(self, value: bool) -> None:
        self._com_obj.UseStepListConfigurations = value

    @property
    @ts_interface
    def command_line_can_change_edit_mode(self) -> bool:
        return bool(self._com_obj.CommandLineCanChangeEditMode)

    @command_line_can_change_edit_mode.setter
    @ts_interface
    def command_line_can_change_edit_mode(self, value: bool) -> None:
        self._com_obj.CommandLineCanChangeEditMode = value

    @property
    @ts_interface
    def edit_mode_shortcut_key(self) -> int:
        return int(self._com_obj.EditModeShortcutKey)

    @edit_mode_shortcut_key.setter
    @ts_interface
    def edit_mode_shortcut_key(self, value: int) -> None:
        self._com_obj.EditModeShortcutKey = value

    @property
    @ts_interface
    def edit_mode_shortcut_modifier(self) -> ShortcutModifier:
        return ShortcutModifier(self._com_obj.EditModeShortcutModifier)

    @edit_mode_shortcut_modifier.setter
    @ts_interface
    def edit_mode_shortcut_modifier(self, value: ShortcutModifier | int) -> None:
        self._com_obj.EditModeShortcutModifier = int(value)

    @property
    @ts_interface
    def exit_code(self) -> int:
        return int(self._com_obj.ExitCode)

    @property
    @ts_interface
    def command_line_arguments(self) -> Strings:
        from .connections import Strings

        return Strings(self._com_obj.CommandLineArguments, self._engine_ref)

    @property
    @ts_interface
    def config_file_path(self) -> str:
        return str(self._com_obj.ConfigFilePath)

    @config_file_path.setter
    @ts_interface
    def config_file_path(self, value: str) -> None:
        self._com_obj.ConfigFilePath = value

    @property
    @ts_interface
    def break_on_first_step(self) -> bool:
        return bool(self._com_obj.BreakOnFirstStep)

    @break_on_first_step.setter
    @ts_interface
    def break_on_first_step(self, value: bool) -> None:
        self._com_obj.BreakOnFirstStep = value

    @property
    @ts_interface
    def break_on_step_failure(self) -> bool:
        return bool(self._com_obj.BreakOnStepFailure)

    @break_on_step_failure.setter
    @ts_interface
    def break_on_step_failure(self, value: bool) -> None:
        self._com_obj.BreakOnStepFailure = value

    @property
    @ts_interface
    def break_on_sequence_failure(self) -> bool:
        return bool(self._com_obj.BreakOnSequenceFailure)

    @break_on_sequence_failure.setter
    @ts_interface
    def break_on_sequence_failure(self, value: bool) -> None:
        self._com_obj.BreakOnSequenceFailure = value

    @property
    @ts_interface
    def automatically_reload_modified_files(self) -> AutomaticallyReloadModifiedFilesOption:
        return AutomaticallyReloadModifiedFilesOption(
            self._com_obj.AutomaticallyReloadModifiedFiles,
        )

    @automatically_reload_modified_files.setter
    @ts_interface
    def automatically_reload_modified_files(
        self,
        value: AutomaticallyReloadModifiedFilesOption | int,
    ) -> None:
        self._com_obj.AutomaticallyReloadModifiedFiles = int(value)

    @property
    @ts_interface
    def reload_modified_files_interval(self) -> float:
        return float(self._com_obj.ReloadModifiedFilesInterval)

    @reload_modified_files_interval.setter
    @ts_interface
    def reload_modified_files_interval(self, value: float) -> None:
        self._com_obj.ReloadModifiedFilesInterval = value

    @property
    @ts_interface
    def save_on_close(self) -> bool:
        return bool(self._com_obj.SaveOnClose)

    @save_on_close.setter
    @ts_interface
    def save_on_close(self, value: bool) -> None:
        self._com_obj.SaveOnClose = value

    @property
    @ts_interface
    def config_file(self) -> PropertyObjectFile:
        from py_teststand.property.property_object_file import PropertyObjectFile

        return PropertyObjectFile(self._com_obj.ConfigFile, self._engine_ref)

    @property
    @ts_interface
    def edit_read_only_files(self) -> bool:
        return bool(self._com_obj.EditReadOnlyFiles)

    @edit_read_only_files.setter
    @ts_interface
    def edit_read_only_files(self, value: bool) -> None:
        self._com_obj.EditReadOnlyFiles = value

    @property
    @ts_interface
    def make_step_names_unique(self) -> bool:
        return bool(self._com_obj.MakeStepNamesUnique)

    @make_step_names_unique.setter
    @ts_interface
    def make_step_names_unique(self, value: bool) -> None:
        self._com_obj.MakeStepNamesUnique = value

    @property
    @ts_interface
    def prompt_for_overwrite(self) -> bool:
        return bool(self._com_obj.PromptForOverwrite)

    @prompt_for_overwrite.setter
    @ts_interface
    def prompt_for_overwrite(self, value: bool) -> None:
        self._com_obj.PromptForOverwrite = value

    @property
    @ts_interface
    def create_empty_sequence_file_on_start(self) -> bool:
        return bool(self._com_obj.CreateEmptySequenceFileOnStart)

    @create_empty_sequence_file_on_start.setter
    @ts_interface
    def create_empty_sequence_file_on_start(self, value: bool) -> None:
        self._com_obj.CreateEmptySequenceFileOnStart = value

    @property
    @ts_interface
    def reload_sequence_files_on_start(self) -> bool:
        return bool(self._com_obj.ReloadSequenceFilesOnStart)

    @reload_sequence_files_on_start.setter
    @ts_interface
    def reload_sequence_files_on_start(self, value: bool) -> None:
        self._com_obj.ReloadSequenceFilesOnStart = value

    @property
    @ts_interface
    def mru_files(self) -> MRUFiles:
        from .connections import MRUFiles

        return MRUFiles(self._com_obj.MRUFiles, self._engine_ref)

    @property
    @ts_interface
    def connections(self) -> ApplicationMgrConnections:
        from .connections import ApplicationMgrConnections

        return ApplicationMgrConnections(self._com_obj.Connections, self._engine_ref)

    @property
    @ts_interface
    def executions(self) -> Executions:
        from .connections import Executions

        return Executions(self._com_obj.Executions, self._engine_ref)

    @property
    @ts_interface
    def sequence_files(self) -> SequenceFiles:
        from .connections import SequenceFiles

        return SequenceFiles(self._com_obj.SequenceFiles, self._engine_ref)

    @property
    @ts_interface
    def execution_entry_points(self) -> Commands:
        from .command import Commands

        return Commands(self._com_obj.ExecutionEntryPoints, self._engine_ref)

    @property
    @ts_interface
    def configuration_entry_points(self) -> Commands:
        from .command import Commands

        return Commands(self._com_obj.ConfigurationEntryPoints, self._engine_ref)

    @property
    @ts_interface
    def undo_stack(self) -> UndoStack | None:
        from py_teststand.undo.undo_stack import UndoStack

        com_undo = self._com_obj.UndoStack
        return UndoStack(com_undo, self._engine_ref) if com_undo else None

    @property
    @ts_interface
    def current_ui_message(self) -> UIMessage | None:
        from py_teststand.messaging.ui_message import UIMessage

        com_msg = self._com_obj.CurrentUIMessage
        return UIMessage(com_msg, self._engine_ref) if com_msg else None

    @property
    @ts_interface
    def logout_closes_seq_files_and_execs(self) -> bool:
        return bool(self._com_obj.LogoutClosesSeqFilesAndExecs)

    @logout_closes_seq_files_and_execs.setter
    @ts_interface
    def logout_closes_seq_files_and_execs(self, value: bool) -> None:
        self._com_obj.LogoutClosesSeqFilesAndExecs = value

    @property
    @ts_interface
    def user_data(self) -> typing.Any:
        return self._com_obj.UserData

    @user_data.setter
    @ts_interface
    def user_data(self, value: typing.Any) -> None:
        self._com_obj.UserData = value

    @property
    @ts_interface
    def application_will_exit_on_start(self) -> bool:
        return bool(self._com_obj.ApplicationWillExitOnStart)

    @ts_interface
    def add_command_line_arguments_help(self) -> None:
        self._com_obj.AddCommandLineArgumentsHelp()

    @ts_interface
    def begin_edit(
        self,
        edited_file: PropertyObjectFile | None,
        edit_kind: EditKind | int,
        objects_to_edit: typing.Any,
    ) -> bool:
        raw_file = edited_file._com_obj if edited_file else None
        return bool(self._com_obj.BeginEdit(raw_file, int(edit_kind), objects_to_edit))

    @ts_interface
    def can_edit(self, edited_file: PropertyObjectFile | None, edit_kind: EditKind | int) -> bool:
        raw_file = edited_file._com_obj if edited_file else None
        return bool(self._com_obj.CanEdit(raw_file, int(edit_kind)))

    @ts_interface
    def close_all_executions(self) -> None:
        self._com_obj.CloseAllExecutions()

    @ts_interface
    def close_all_sequence_files(self) -> None:
        self._com_obj.CloseAllSequenceFiles()

    @ts_interface
    def close_execution(self, execution: typing.Any) -> None:
        raw_exec = getattr(execution, "_com_obj", execution)
        self._com_obj.CloseExecution(raw_exec)

    @ts_interface
    def close_sequence_file(self, sequence_file: SequenceFile) -> None:
        raw_file = sequence_file._com_obj if hasattr(sequence_file, "_com_obj") else sequence_file
        self._com_obj.CloseSequenceFile(raw_file)

    @ts_interface
    def connect_adapter_list(self, control: typing.Any) -> typing.Any:
        return self._com_obj.ConnectAdapterList(control)

    @ts_interface
    def connect_caption(
        self,
        control: typing.Any,
        source: CaptionSource | int,
        long_name: bool = False,
    ) -> CaptionConnection:
        from .connections import CaptionConnection

        return CaptionConnection(
            self._com_obj.ConnectCaption(control, int(source), long_name),
            self._engine_ref,
        )

    @ts_interface
    def connect_command(
        self,
        command_kind: CommandKind | int,
        control: typing.Any,
        index: int = 0,
        options: int = 0,
    ) -> CommandConnection:
        from .connections import CommandConnection

        return CommandConnection(
            self._com_obj.ConnectCommand(int(command_kind), control, index, options),
            self._engine_ref,
        )

    @ts_interface
    def end_edit(
        self,
        edited_file: PropertyObjectFile | None,
        edit_kind: EditKind | int,
        edited_objects: typing.Any,
        cancelled: bool,
    ) -> None:
        raw_file = edited_file._com_obj if edited_file else None
        self._com_obj.EndEdit(raw_file, int(edit_kind), edited_objects, bool(cancelled))

    @ts_interface
    def get_auto_close_execution(self) -> bool:
        return bool(self._com_obj.GetAutoCloseExecution())

    @ts_interface
    def get_caption_text(
        self,
        caption_source: CaptionSource | int,
        long_name: bool,
        format_expression: str = "",
    ) -> str:
        return str(self._com_obj.GetCaptionText(int(caption_source), long_name, format_expression))

    @ts_interface
    def get_command(self, command_kind: CommandKind | int, index: int = 0) -> Command | None:
        from .command import Command

        com_cmd = self._com_obj.GetCommand(int(command_kind), index)
        return Command(com_cmd, self._engine_ref) if com_cmd else None

    @ts_interface
    def get_engine(self) -> Engine:
        from py_teststand.core.engine import Engine

        return Engine(self._com_obj.GetEngine())

    @ts_interface
    def get_execution_view_mgr(self) -> ExecutionViewManager | None:
        from .execution_view_manager import ExecutionViewManager

        com_mgr = self._com_obj.GetExecutionViewMgr()
        return ExecutionViewManager(com_mgr, self._engine_ref) if com_mgr else None

    @ts_interface
    def get_image_name(self, image_source: ImageSource | int) -> str:
        return str(self._com_obj.GetImageName(int(image_source)))

    @ts_interface
    def get_model_file(self) -> SequenceFile | None:
        from py_teststand.sequence.sequence_file import SequenceFile

        com_file = self._com_obj.GetModelFile()
        return SequenceFile(com_file, self._engine_ref) if com_file else None

    @ts_interface
    def get_run_state(self) -> RunStates:
        return RunStates(self._com_obj.GetRunState())

    @ts_interface
    def get_sequence_file_view_mgr(self) -> SequenceFileViewManager | None:
        from .sequence_file_view_manager import SequenceFileViewManager

        com_mgr = self._com_obj.GetSequenceFileViewMgr()
        return SequenceFileViewManager(com_mgr, self._engine_ref) if com_mgr else None

    @ts_interface
    def get_termination_state(self) -> TerminationStates:
        return TerminationStates(self._com_obj.GetTerminationState())

    @ts_interface
    def get_visible(self, execution: typing.Any) -> bool:
        raw_exec = getattr(execution, "_com_obj", execution)
        return bool(self._com_obj.GetVisible(raw_exec))

    @ts_interface
    def localize_all_controls(self, section_name: str) -> None:
        self._com_obj.LocalizeAllControls(section_name)

    @ts_interface
    def login(self) -> None:
        self._com_obj.Login()

    @ts_interface
    def logout(self, close_files_and_execs: bool = True) -> None:
        self._com_obj.Logout(close_files_and_execs)

    @ts_interface
    def new_commands(self) -> Commands:
        from .command import Commands

        return Commands(self._com_obj.NewCommands(), self._engine_ref)

    @ts_interface
    def open_sequence_file(self, path: str) -> SequenceFile | None:
        from py_teststand.sequence.sequence_file import SequenceFile

        com_file = self._com_obj.OpenSequenceFile(path)
        return SequenceFile(com_file, self._engine_ref) if com_file else None

    @ts_interface
    def open_sequence_file_dialog(
        self,
        title: str = "",
        initial_path: str = "",
        filter: str = "",
        options: int = 0,
    ) -> str:
        return str(self._com_obj.OpenSequenceFileDialog(title, initial_path, filter, options))

    @ts_interface
    def open_sequence_files_dialog(
        self,
        title: str = "",
        initial_path: str = "",
        filter: str = "",
        allow_multi_select: bool = True,
        allow_edit_only: bool = False,
        options: int = 0,
    ) -> list[str]:
        return list(
            self._com_obj.OpenSequenceFilesDialog(
                title,
                initial_path,
                filter,
                allow_multi_select,
                allow_edit_only,
                options,
            ),
        )

    @ts_interface
    def raise_error(self, code: int, message: str) -> None:
        self._com_obj.RaiseError(code, message)

    @ts_interface
    def refresh(self) -> None:
        self._com_obj.Refresh()

    @ts_interface
    def refresh_all_view_mgrs(self) -> None:
        self._com_obj.RefreshAllViewMgrs()

    @ts_interface
    def refresh_file(self, file: typing.Any) -> None:
        raw_file = getattr(file, "_com_obj", file)
        self._com_obj.RefreshFile(raw_file)

    @ts_interface
    def reload_config_file(self) -> None:
        self._com_obj.ReloadConfigFile()

    @ts_interface
    def reload_file(self, file: typing.Any) -> None:
        raw_file = getattr(file, "_com_obj", file)
        self._com_obj.ReloadFile(raw_file)

    @ts_interface
    def reload_modified_sequence_files(self) -> None:
        self._com_obj.ReloadModifiedSequenceFiles()

    @ts_interface
    def reload_modified_sequence_files_ex(self, options: int) -> None:
        self._com_obj.ReloadModifiedSequenceFilesEx(options)

    @ts_interface
    def set_auto_close_execution(self, value: bool) -> None:
        self._com_obj.SetAutoCloseExecution(value)

    @ts_interface
    def set_visible(self, value: bool) -> None:
        self._com_obj.SetVisible(value)

    @ts_interface
    def shutdown(self) -> None:
        self._com_obj.Shutdown()

    @ts_interface
    def start(self) -> None:
        self._com_obj.Start()
