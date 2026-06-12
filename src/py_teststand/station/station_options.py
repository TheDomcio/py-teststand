from __future__ import annotations

import typing
from enum import IntEnum, IntFlag

from py_teststand.core.com_wrapper import ts_interface
from py_teststand.property.property_object import PropertyObject

if typing.TYPE_CHECKING:
    from py_teststand.core.engine import RTEOption


class DebugOption(IntFlag):
    NoneValue = 0
    StackChecking = 1
    BufferChecking = 2
    ReportObjectLeaks = 4
    SendOutputMessagesToDebugger = 8
    ReportKnownOSandComponentProblems = 16


class FileModificationIndicatorPolicy(IntEnum):
    DefaultPolicy = 0
    ExcludeTestStandVersionUpgrade = 1


class StationOptions(PropertyObject):
    def __init__(self, com_obj: typing.Any, engine: typing.Any = None) -> None:

        super().__init__(com_obj, engine)

    def release(self) -> None:

        object.__setattr__(self, "_com_obj", None)

    @property
    @ts_interface
    def user_file_path(self) -> str:
        return str(self._com_obj.UserFilePath)

    @user_file_path.setter
    @ts_interface
    def user_file_path(self, value: str) -> None:
        self._com_obj.UserFilePath = value

    @property
    @ts_interface
    def enable_user_privilege_checking(self) -> bool:
        return bool(self._com_obj.EnableUserPrivilegeChecking)

    @enable_user_privilege_checking.setter
    @ts_interface
    def enable_user_privilege_checking(self, value: bool) -> None:
        self._com_obj.EnableUserPrivilegeChecking = value

    @property
    @ts_interface
    def auto_login_system_user(self) -> bool:
        return bool(self._com_obj.AutoLoginSystemUser)

    @auto_login_system_user.setter
    @ts_interface
    def auto_login_system_user(self, value: bool) -> None:
        self._com_obj.AutoLoginSystemUser = value

    @property
    @ts_interface
    def require_user_login(self) -> bool:
        return bool(self._com_obj.RequireUserLogin)

    @require_user_login.setter
    @ts_interface
    def require_user_login(self, value: bool) -> None:
        self._com_obj.RequireUserLogin = value

    @property
    @ts_interface
    def rte_option(self) -> RTEOption:
        from py_teststand.core.engine import RTEOption

        return RTEOption(int(self._com_obj.RTEOption))

    @rte_option.setter
    @ts_interface
    def rte_option(self, value: RTEOption | int) -> None:
        self._com_obj.RTEOption = int(value)

    @property
    @ts_interface
    def tracing_enabled(self) -> bool:
        return bool(self._com_obj.TracingEnabled)

    @tracing_enabled.setter
    @ts_interface
    def tracing_enabled(self, value: bool) -> None:
        self._com_obj.TracingEnabled = value

    @property
    @ts_interface
    def breakpoints_enabled(self) -> bool:
        return bool(self._com_obj.BreakpointsEnabled)

    @breakpoints_enabled.setter
    @ts_interface
    def breakpoints_enabled(self, value: bool) -> None:
        self._com_obj.BreakpointsEnabled = value

    @property
    @ts_interface
    def disable_results(self) -> bool:
        return bool(self._com_obj.DisableResults)

    @disable_results.setter
    @ts_interface
    def disable_results(self, value: bool) -> None:
        self._com_obj.DisableResults = value

    @property
    @ts_interface
    def always_goto_cleanup_on_failure(self) -> bool:
        return bool(self._com_obj.AlwaysGotoCleanupOnFailure)

    @always_goto_cleanup_on_failure.setter
    @ts_interface
    def always_goto_cleanup_on_failure(self, value: bool) -> None:
        self._com_obj.AlwaysGotoCleanupOnFailure = value

    @property
    @ts_interface
    def auto_create_variable_location(self) -> typing.Any:
        from py_teststand.sequence.location import AutoCreateVariableLocation

        return AutoCreateVariableLocation(int(self._com_obj.AutoCreateVariableLocation))

    @auto_create_variable_location.setter
    @ts_interface
    def auto_create_variable_location(self, value: int) -> None:
        self._com_obj.AutoCreateVariableLocation = int(value)

    @property
    @ts_interface
    def execution_mask(self) -> int:
        return int(self._com_obj.ExecutionMask)

    @execution_mask.setter
    @ts_interface
    def execution_mask(self, value: int) -> None:
        self._com_obj.ExecutionMask = value

    @property
    @ts_interface
    def interactive_branch_mode(self) -> typing.Any:
        return int(self._com_obj.InteractiveBranchMode)

    @interactive_branch_mode.setter
    @ts_interface
    def interactive_branch_mode(self, value: int) -> None:
        self._com_obj.InteractiveBranchMode = int(value)

    @property
    @ts_interface
    def show_hidden_properties(self) -> bool:
        return bool(self._com_obj.ShowHiddenProperties)

    @show_hidden_properties.setter
    @ts_interface
    def show_hidden_properties(self, value: bool) -> None:
        self._com_obj.ShowHiddenProperties = value

    @property
    @ts_interface
    def prompt_to_find_files(self) -> bool:
        return bool(self._com_obj.PromptToFindFiles)

    @prompt_to_find_files.setter
    @ts_interface
    def prompt_to_find_files(self, value: bool) -> None:
        self._com_obj.PromptToFindFiles = value

    @property
    @ts_interface
    def seq_file_version_auto_increment_opt(self) -> typing.Any:
        return int(self._com_obj.SeqFileVersionAutoIncrementOpt)

    @seq_file_version_auto_increment_opt.setter
    @ts_interface
    def seq_file_version_auto_increment_opt(self, value: int) -> None:
        self._com_obj.SeqFileVersionAutoIncrementOpt = value

    @property
    @ts_interface
    def type_version_auto_increment_opt(self) -> typing.Any:
        return int(self._com_obj.TypeVersionAutoIncrementOpt)

    @type_version_auto_increment_opt.setter
    @ts_interface
    def type_version_auto_increment_opt(self, value: int) -> None:
        self._com_obj.TypeVersionAutoIncrementOpt = value

    @property
    @ts_interface
    def type_version_auto_increment_prompt_opt(self) -> bool:
        return bool(self._com_obj.TypeVersionAutoIncrementPromptOpt)

    @type_version_auto_increment_prompt_opt.setter
    @ts_interface
    def type_version_auto_increment_prompt_opt(self, value: bool) -> None:
        self._com_obj.TypeVersionAutoIncrementPromptOpt = value

    @property
    @ts_interface
    def reload_docs_when_opening_workspace(self) -> bool:
        return bool(self._com_obj.ReloadDocsWhenOpeningWorkspace)

    @reload_docs_when_opening_workspace.setter
    @ts_interface
    def reload_docs_when_opening_workspace(self, value: bool) -> None:
        self._com_obj.ReloadDocsWhenOpeningWorkspace = value

    @property
    @ts_interface
    def reload_workspace_at_startup(self) -> bool:
        return bool(self._com_obj.ReloadWorkspaceAtStartup)

    @reload_workspace_at_startup.setter
    @ts_interface
    def reload_workspace_at_startup(self, value: bool) -> None:
        self._com_obj.ReloadWorkspaceAtStartup = value

    @property
    @ts_interface
    def station_id(self) -> str:
        return str(self._com_obj.StationID)

    @station_id.setter
    @ts_interface
    def station_id(self, value: str) -> None:
        self._com_obj.StationID = value

    @property
    @ts_interface
    def specify_steps_by_unique_id_in_expressions(self) -> typing.Any:
        return int(self._com_obj.SpecifyStepsByUniqueIdInExpressions)

    @specify_steps_by_unique_id_in_expressions.setter
    @ts_interface
    def specify_steps_by_unique_id_in_expressions(self, value: int) -> None:
        self._com_obj.SpecifyStepsByUniqueIdInExpressions = value

    @property
    @ts_interface
    def use_station_model(self) -> bool:
        return bool(self._com_obj.UseStationModel)

    @use_station_model.setter
    @ts_interface
    def use_station_model(self, value: bool) -> None:
        self._com_obj.UseStationModel = value

    @property
    @ts_interface
    def allow_other_models(self) -> bool:
        return bool(self._com_obj.AllowOtherModels)

    @allow_other_models.setter
    @ts_interface
    def allow_other_models(self, value: bool) -> None:
        self._com_obj.AllowOtherModels = value

    @property
    @ts_interface
    def station_model_sequence_file_path(self) -> str:
        return str(self._com_obj.StationModelSequenceFilePath)

    @station_model_sequence_file_path.setter
    @ts_interface
    def station_model_sequence_file_path(self, value: str) -> None:
        self._com_obj.StationModelSequenceFilePath = value

    @property
    @ts_interface
    def language(self) -> str:
        return str(self._com_obj.Language)

    @language.setter
    @ts_interface
    def language(self, value: str) -> None:
        self._com_obj.Language = value

    @property
    @ts_interface
    def use_localized_decimal_point(self) -> bool:
        return bool(self._com_obj.UseLocalizedDecimalPoint)

    @use_localized_decimal_point.setter
    @ts_interface
    def use_localized_decimal_point(self, value: bool) -> None:
        self._com_obj.UseLocalizedDecimalPoint = value

    @property
    @ts_interface
    def recognize_mb_chars(self) -> bool:
        return bool(self._com_obj.RecognizeMBChars)

    @recognize_mb_chars.setter
    @ts_interface
    def recognize_mb_chars(self, value: bool) -> None:
        self._com_obj.RecognizeMBChars = value

    @property
    @ts_interface
    def allow_sequence_calls_from_remote_machine(self) -> bool:
        return bool(self._com_obj.AllowSequenceCallsFromRemoteMachine)

    @allow_sequence_calls_from_remote_machine.setter
    @ts_interface
    def allow_sequence_calls_from_remote_machine(self, value: bool) -> None:
        self._com_obj.AllowSequenceCallsFromRemoteMachine = value

    @property
    @ts_interface
    def allow_all_users_access_from_remote_machine(self) -> bool:
        return bool(self._com_obj.AllowAllUsersAccessFromRemoteMachine)

    @allow_all_users_access_from_remote_machine.setter
    @ts_interface
    def allow_all_users_access_from_remote_machine(self, value: bool) -> None:
        self._com_obj.AllowAllUsersAccessFromRemoteMachine = value

    @property
    @ts_interface
    def show_engine_tray_icon_on_remote_stations(self) -> bool:
        return bool(self._com_obj.ShowEngineTrayIconOnRemoteStations)

    @show_engine_tray_icon_on_remote_stations.setter
    @ts_interface
    def show_engine_tray_icon_on_remote_stations(self, value: bool) -> None:
        self._com_obj.ShowEngineTrayIconOnRemoteStations = value

    @property
    @ts_interface
    def check_out_files_when_edited(self) -> bool:
        return bool(self._com_obj.CheckOutFilesWhenEdited)

    @check_out_files_when_edited.setter
    @ts_interface
    def check_out_files_when_edited(self, value: bool) -> None:
        self._com_obj.CheckOutFilesWhenEdited = value

    @property
    @ts_interface
    def prompt_when_adding_files_to_sc(self) -> bool:
        return bool(self._com_obj.PromptWhenAddingFilesToSC)

    @prompt_when_adding_files_to_sc.setter
    @ts_interface
    def prompt_when_adding_files_to_sc(self, value: bool) -> None:
        self._com_obj.PromptWhenAddingFilesToSC = value

    @property
    @ts_interface
    def use_dialog_for_check_out(self) -> bool:
        return bool(self._com_obj.UseDialogForCheckOut)

    @use_dialog_for_check_out.setter
    @ts_interface
    def use_dialog_for_check_out(self, value: bool) -> None:
        self._com_obj.UseDialogForCheckOut = value

    @property
    @ts_interface
    def check_out_only_selected_files(self) -> bool:
        return bool(self._com_obj.CheckOutOnlySelectedFiles)

    @check_out_only_selected_files.setter
    @ts_interface
    def check_out_only_selected_files(self, value: bool) -> None:
        self._com_obj.CheckOutOnlySelectedFiles = value

    @property
    @ts_interface
    def system_default_source_code_control_provider(self) -> typing.Any:
        return str(self._com_obj.SystemDefaultSourceCodeControlProvider)

    @system_default_source_code_control_provider.setter
    @ts_interface
    def system_default_source_code_control_provider(self, value: str) -> None:
        self._com_obj.SystemDefaultSourceCodeControlProvider = value

    @property
    @ts_interface
    def ui_message_delay(self) -> int:
        return int(self._com_obj.UIMessageDelay)

    @ui_message_delay.setter
    @ts_interface
    def ui_message_delay(self, value: int) -> None:
        self._com_obj.UIMessageDelay = value

    @property
    @ts_interface
    def ui_message_min_delay(self) -> int:
        return int(self._com_obj.UIMessageMinDelay)

    @ui_message_min_delay.setter
    @ts_interface
    def ui_message_min_delay(self, value: int) -> None:
        self._com_obj.UIMessageMinDelay = value

    @property
    @ts_interface
    def interactive_exe_propagate_status(self) -> bool:
        return bool(self._com_obj.InteractiveExePropagateStatus)

    @interactive_exe_propagate_status.setter
    @ts_interface
    def interactive_exe_propagate_status(self, value: bool) -> None:
        self._com_obj.InteractiveExePropagateStatus = value

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
    def debug_options(self) -> int:
        return int(self._com_obj.DebugOptions)

    @debug_options.setter
    @ts_interface
    def debug_options(self, value: int) -> None:
        self._com_obj.DebugOptions = value

    @property
    @ts_interface
    def default_file_writing_format(self) -> typing.Any:
        return int(self._com_obj.DefaultFileWritingFormat)

    @default_file_writing_format.setter
    @ts_interface
    def default_file_writing_format(self, value: int) -> None:
        self._com_obj.DefaultFileWritingFormat = int(value)

    @property
    @ts_interface
    def allow_automatic_type_conflict_resolution(self) -> typing.Any:
        from py_teststand.core.engine import AllowAutomaticTypeConflictResolution

        return AllowAutomaticTypeConflictResolution(
            int(self._com_obj.AllowAutomaticTypeConflictResolution),
        )

    @allow_automatic_type_conflict_resolution.setter
    @ts_interface
    def allow_automatic_type_conflict_resolution(self, value: int) -> None:
        self._com_obj.AllowAutomaticTypeConflictResolution = int(value)

    @property
    @ts_interface
    def file_modification_indicator_policy(self) -> int:
        return int(self._com_obj.FileModificationIndicatorPolicy)

    @file_modification_indicator_policy.setter
    @ts_interface
    def file_modification_indicator_policy(self, value: int) -> None:
        self._com_obj.FileModificationIndicatorPolicy = value

    @property
    @ts_interface
    def preload_progress_delay(self) -> float:
        return float(self._com_obj.PreloadProgressDelay)

    @preload_progress_delay.setter
    @ts_interface
    def preload_progress_delay(self, value: float) -> None:
        self._com_obj.PreloadProgressDelay = value

    @property
    @ts_interface
    def allow_cancelling_preload_expression(self) -> typing.Any:
        return str(self._com_obj.AllowCancellingPreloadExpression)

    @allow_cancelling_preload_expression.setter
    @ts_interface
    def allow_cancelling_preload_expression(self, value: str) -> None:
        self._com_obj.AllowCancellingPreloadExpression = value

    @property
    @ts_interface
    def default_cpu_affinity_for_threads_ex(self) -> int:
        return int(self._com_obj.DefaultCPUAffinityForThreadsEx)

    @default_cpu_affinity_for_threads_ex.setter
    @ts_interface
    def default_cpu_affinity_for_threads_ex(self, value: int) -> None:
        self._com_obj.DefaultCPUAffinityForThreadsEx = int(value)

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
    def default_cpu_affinity_for_threads(self) -> typing.Any:
        return int(self._com_obj.DefaultCPUAffinityForThreads)

    @default_cpu_affinity_for_threads.setter
    @ts_interface
    def default_cpu_affinity_for_threads(self, value: int) -> None:
        self._com_obj.DefaultCPUAffinityForThreads = value

    @ts_interface
    def get_languages(self) -> list[str]:
        return list(self._com_obj.GetLanguages())

    @ts_interface
    def get_time_limit(self, type: int, operation: int) -> typing.Any:
        return float(self._com_obj.GetTimeLimit(type, operation))

    @ts_interface
    def set_time_limit(self, type: int, operation: int, value: float) -> typing.Any:
        self._com_obj.SetTimeLimit(type, operation, value)

    @ts_interface
    def get_time_limit_enabled(self, type: int, operation: int) -> typing.Any:
        return bool(self._com_obj.GetTimeLimitEnabled(type, operation))

    @ts_interface
    def set_time_limit_enabled(self, type: int, operation: int, value: bool) -> typing.Any:
        self._com_obj.SetTimeLimitEnabled(type, operation, value)

    @ts_interface
    def get_time_limit_action(self, type: int, operation: int) -> typing.Any:
        return int(self._com_obj.GetTimeLimitAction(type, operation))

    @ts_interface
    def set_time_limit_action(self, type: int, operation: int, value: int) -> typing.Any:
        self._com_obj.SetTimeLimitAction(type, operation, value)


class TimeLimitAction(IntEnum):
    Abort = 0
    KillThreads = 1
    Prompt = 2
    Terminate = 3


class InteractiveBranchMode(IntEnum):
    NoneValue = 0
    Ignore = 1
    GotoEnd = 2
    RaiseRTE = 3
    AllowAll = 4


class SpecifyStepsByUniqueId(IntEnum):
    Ask = 1
    Yes = 2
    No = 3


class TypeVersionAutoIncrement(IntEnum):
    def __str__(self) -> str:
        return str(self.value)

    NoneValue = 0
    Major = 1
    Minor = 2
    Revision = 3
    Build = 4
