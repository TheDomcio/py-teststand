"""Provision TestStand station options programmatically.

Demonstrates the "TestStand station as code" workflow: open the engine,
acquire its StationOptions object via a context manager, set a broad
range of station-level settings (tracing, debug flags, RTE behaviour,
locale, file write format, time limits, remote-call policy, etc.), and
commit the configuration to disk so it persists across engine sessions.

This is the kind of script intended to be driven from a deployment tool
(Ansible, Chef, custom bootstrap) to replace manual point-and-click
station setup with a version-controlled configuration source.
"""

from __future__ import annotations

from py_teststand import Engine, RTEOption
from py_teststand.core.engine import AllowAutomaticTypeConflictResolution
from py_teststand.property.property_object_file import FileWritingFormat
from py_teststand.sequence.location import AutoCreateVariableLocation
from py_teststand.station.station_options import (
    DebugOption,
    InteractiveBranchMode,
    TimeLimitAction,
)


def main() -> None:
    with Engine() as engine:
        with engine.station_options as station_options:
            station_options.tracing_enabled = True
            station_options.disable_results = False
            station_options.breakpoints_enabled = True
            station_options.require_user_login = False
            station_options.check_out_files_when_edited = False
            station_options.language = "English"
            station_options.rte_option = RTEOption.Continue
            station_options.allow_automatic_type_conflict_resolution = (
                AllowAutomaticTypeConflictResolution.Never
            )
            station_options.auto_create_variable_location = AutoCreateVariableLocation.Locals
            station_options.default_file_writing_format = FileWritingFormat.Binary
            station_options.interactive_branch_mode = InteractiveBranchMode.AllowAll
            station_options.debug_options = (
                DebugOption.ReportKnownOSandComponentProblems | DebugOption.BufferChecking
            )
            station_options.always_goto_cleanup_on_failure = True
            station_options.show_hidden_properties = True
            station_options.prompt_to_find_files = False
            station_options.login_on_start = False
            station_options.ui_message_delay = 100
            station_options.ui_message_min_delay = 10
            station_options.station_id = "STATION_01"
            station_options.use_station_model = True
            station_options.allow_other_models = False
            station_options.use_localized_decimal_point = False
            station_options.allow_sequence_calls_from_remote_machine = False
            station_options.allow_all_users_access_from_remote_machine = False
            station_options.show_engine_tray_icon_on_remote_stations = True
            station_options.prompt_when_adding_files_to_sc = True
            station_options.use_dialog_for_check_out = False
            station_options.check_out_only_selected_files = True
            station_options.interactive_exe_propagate_status = True
            station_options.break_on_step_failure = False
            station_options.break_on_sequence_failure = False
            station_options.file_modification_indicator_policy = 1
            station_options.preload_progress_delay = 5.0
            station_options.set_time_limit(0, 0, 60.0)
            station_options.set_time_limit_enabled(0, 0, True)
            station_options.set_time_limit_action(0, 0, TimeLimitAction.Abort)

        engine.commit_globals_to_disk(prompt_on_save_conflicts=False)


if __name__ == "__main__":
    main()
