from __future__ import annotations

import typing
from enum import IntEnum, IntFlag
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COM, ts_interface
from py_teststand.property.property_object import PropertyObject
from py_teststand.sequence.step import Step
from py_teststand.sequence.step_group import StepGroup


class FailureAction(IntEnum):
    NoneValue = 0
    GotoCleanup = 1
    UseStationOption = 2


class LoadModuleOption(IntFlag):
    EvaluateExpressions = 0x4
    DoNotPromptToFindFile = 32
    DoNotRunLoadCallbacks = 64
    IgnoreErrors = 1
    IgnoreSkippedSteps = 8
    LoadModulesInSubSequence = 2
    NoneValue = 0
    ThrowExceptionOnError = 16


class SequenceType(IntEnum):
    Normal = 0
    Callback = 1
    ExeEntryPoint = 3
    CfgEntryPoint = 5
    ReservedCallback = 7


class SequenceContextProperties:
    RunState_LoopIndex = "LoopIndex"
    RunState_LoopNumFailed = "LoopNumFailed"
    RunState_LoopNumPassed = "LoopNumPassed"
    RunState_SeqFileProp = "SequenceFile"
    RunState_SeqProp = "Sequence"
    RunState_StepProp = "Step"
    SeqContext_RunStateProp = "RunState"


class SequenceDefaultValueScope(IntEnum):
    Execution = 1
    ExecutionTree = 2


class SequenceProperties:
    Seq_CleanupProp = "Cleanup"
    Seq_MainProp = "Main"
    Seq_SetupProp = "Setup"


if TYPE_CHECKING:
    from py_teststand.core.engine import Engine
    from py_teststand.sequence.sequence_file import SequenceFile


class StepCollection:
    def __init__(self, sequence: Sequence, group: int = StepGroup.Main):

        self._sequence = sequence
        self._group = group

    def __len__(self) -> int:

        return self._sequence.get_num_steps(self._group)

    def __getitem__(self, index: int | str | slice) -> Step | list[Step]:

        if isinstance(index, str):
            return self._sequence.get_step_by_name(index, self._group)
        if isinstance(index, slice):
            return typing.cast("list[Step]", [self[i] for i in range(*index.indices(len(self)))])
        return self._sequence.get_step(index, self._group)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    def __contains__(self, name: str) -> bool:

        try:
            self._sequence.get_step_index(name, self._group)
            return True
        except Exception:
            return False


class Sequence(PropertyObject):
    def __init__(self, com_obj: COM, engine: Engine | typing.Any | None = None) -> None:

        super().__init__(com_obj, engine)

    @property
    def steps(self) -> StepCollection:

        return StepCollection(self, StepGroup.Main)

    @property
    def setup(self) -> StepCollection:

        return StepCollection(self, StepGroup.Setup)

    @property
    def main(self) -> StepCollection:

        return StepCollection(self, StepGroup.Main)

    @property
    def cleanup(self) -> StepCollection:

        return StepCollection(self, StepGroup.Cleanup)

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
    def disable_results(self) -> bool:
        return bool(self._com_obj.DisableResults)

    @disable_results.setter
    @ts_interface
    def disable_results(self, value: bool) -> None:
        self._com_obj.DisableResults = value

    @property
    @ts_interface
    def allow_interactive_execution_of_entry_point(self) -> bool:
        return bool(self._com_obj.AllowInteractiveExecutionOfEntryPoint)

    @allow_interactive_execution_of_entry_point.setter
    @ts_interface
    def allow_interactive_execution_of_entry_point(self, value: bool) -> None:
        self._com_obj.AllowInteractiveExecutionOfEntryPoint = bool(value)

    @property
    @ts_interface
    def copy_steps_on_override(self) -> bool:
        return bool(self._com_obj.CopyStepsOnOverride)

    @copy_steps_on_override.setter
    @ts_interface
    def copy_steps_on_override(self, value: bool) -> None:
        self._com_obj.CopyStepsOnOverride = bool(value)

    @property
    @ts_interface
    def entry_point_check_to_save_titled_seq_files(self) -> bool:
        return bool(self._com_obj.EntryPointCheckToSaveTitledSeqFiles)

    @entry_point_check_to_save_titled_seq_files.setter
    @ts_interface
    def entry_point_check_to_save_titled_seq_files(self, value: bool) -> None:
        self._com_obj.EntryPointCheckToSaveTitledSeqFiles = bool(value)

    @property
    @ts_interface
    def entry_point_enabled_expression(self) -> str:
        return str(self._com_obj.EntryPointEnabledExpression)

    @entry_point_enabled_expression.setter
    @ts_interface
    def entry_point_enabled_expression(self, value: str) -> None:
        self._com_obj.EntryPointEnabledExpression = value

    @property
    @ts_interface
    def entry_point_ignore_client(self) -> bool:
        return bool(self._com_obj.EntryPointIgnoreClient)

    @entry_point_ignore_client.setter
    @ts_interface
    def entry_point_ignore_client(self, value: bool) -> None:
        self._com_obj.EntryPointIgnoreClient = bool(value)

    @property
    @ts_interface
    def entry_point_initially_hidden(self) -> bool:
        return bool(self._com_obj.EntryPointInitiallyHidden)

    @entry_point_initially_hidden.setter
    @ts_interface
    def entry_point_initially_hidden(self, value: bool) -> None:
        self._com_obj.EntryPointInitiallyHidden = bool(value)

    @property
    @ts_interface
    def entry_point_menu_hint(self) -> str:
        return str(self._com_obj.EntryPointMenuHint)

    @entry_point_menu_hint.setter
    @ts_interface
    def entry_point_menu_hint(self, value: str) -> None:
        self._com_obj.EntryPointMenuHint = value

    @property
    @ts_interface
    def entry_point_name_expression(self) -> str:
        return str(self._com_obj.EntryPointNameExpression)

    @entry_point_name_expression.setter
    @ts_interface
    def entry_point_name_expression(self, value: str) -> None:
        self._com_obj.EntryPointNameExpression = value

    @property
    @ts_interface
    def show_entry_point_for_all_windows(self) -> bool:
        return bool(self._com_obj.ShowEntryPointForAllWindows)

    @show_entry_point_for_all_windows.setter
    @ts_interface
    def show_entry_point_for_all_windows(self, value: bool) -> None:
        self._com_obj.ShowEntryPointForAllWindows = bool(value)

    @property
    @ts_interface
    def show_entry_point_for_editor_only(self) -> bool:
        return bool(self._com_obj.ShowEntryPointForEditorOnly)

    @show_entry_point_for_editor_only.setter
    @ts_interface
    def show_entry_point_for_editor_only(self, value: bool) -> None:
        self._com_obj.ShowEntryPointForEditorOnly = bool(value)

    @property
    @ts_interface
    def show_entry_point_for_exe_window(self) -> bool:
        return bool(self._com_obj.ShowEntryPointForExeWindow)

    @show_entry_point_for_exe_window.setter
    @ts_interface
    def show_entry_point_for_exe_window(self, value: bool) -> None:
        self._com_obj.ShowEntryPointForExeWindow = bool(value)

    @property
    @ts_interface
    def show_entry_point_for_file_window(self) -> bool:
        return bool(self._com_obj.ShowEntryPointForFileWindow)

    @show_entry_point_for_file_window.setter
    @ts_interface
    def show_entry_point_for_file_window(self, value: bool) -> None:
        self._com_obj.ShowEntryPointForFileWindow = bool(value)

    @property
    @ts_interface
    def requirements(self) -> typing.Any:
        return PropertyObject(self._com_obj.Requirements, self._engine_ref)

    @property
    @ts_interface
    def sequence_index(self) -> int:
        return int(self._com_obj.SequenceIndex)

    @property
    @ts_interface
    def type(self) -> SequenceType:

        return SequenceType(int(self._com_obj.Type))

    @type.setter
    @ts_interface
    def type(self, value: SequenceType | int) -> None:
        self._com_obj.Type = int(value)

    @property
    @ts_interface
    def failure_action(self) -> typing.Any:

        return FailureAction(self._com_obj.FailureAction)

    @failure_action.setter
    @ts_interface
    def failure_action(self, value: FailureAction | int) -> None:
        self._com_obj.FailureAction = int(value)

    @property
    @ts_interface
    def goto_cleanup_on_failure(self) -> bool:
        return bool(self._com_obj.GotoCleanupOnFailure)

    @goto_cleanup_on_failure.setter
    @ts_interface
    def goto_cleanup_on_failure(self, value: bool) -> None:
        self._com_obj.GotoCleanupOnFailure = bool(value)

    @property
    @ts_interface
    def has_mismatched_blocks(self) -> bool:
        return bool(self._com_obj.HasMismatchedBlocks)

    @property
    @ts_interface
    def id(self) -> int:
        return int(self._com_obj.Id)

    @property
    @ts_interface
    def optimize_non_reentrant_calls(self) -> bool:
        return bool(self._com_obj.OptimizeNonReentrantCalls)

    @optimize_non_reentrant_calls.setter
    @ts_interface
    def optimize_non_reentrant_calls(self, value: bool) -> None:
        self._com_obj.OptimizeNonReentrantCalls = bool(value)

    @ts_interface
    def get_num_steps(self, group: int = StepGroup.Main) -> typing.Any:
        return int(self._com_obj.GetNumSteps(int(group)))

    @ts_interface
    def get_step(self, index: int, group: int = StepGroup.Main) -> Step:
        return Step(self._com_obj.GetStep(index, int(group)), engine=self.engine)

    @ts_interface
    def get_step_by_name(self, name: str, group: int = StepGroup.Main) -> Step:
        return Step(self._com_obj.GetStepByName(name, int(group)), engine=self.engine)

    @ts_interface
    def get_step_index(self, name: str, group: int = StepGroup.Main) -> int:
        return int(self._com_obj.GetStepIndex(name, int(group)))

    @property
    @ts_interface
    def num_step_groups(self) -> int:
        return 3

    @ts_interface
    def new_step(
        self,
        adapter_name: str = "None Adapter",
        step_type_name: str = "Action",
        name: str = "Step",
        index: int = 0,
        group: int = StepGroup.Main,
    ) -> Step:
        engine = self.engine
        if engine is None:
            raise ValueError("Cannot find engine reference")

        adapter = engine.get_adapter_by_key_name(adapter_name)
        step_com = engine._engine.NewStep(adapter.key_name, step_type_name)
        step_com.Name = name

        self._com_obj.InsertStep(step_com, index, int(group))
        return Step(step_com, engine=self.engine)

    @ts_interface
    def insert_step(self, step: Step, index: int, group: int = StepGroup.Main) -> None:
        self._com_obj.InsertStep(step._com_obj, index, int(group))

    @ts_interface
    def remove_step(self, index: int, group: int = StepGroup.Main) -> Step:
        com_step = self._com_obj.RemoveStep(index, int(group))
        return Step(com_step, engine=self.engine)

    @ts_interface
    def load_modules(
        self,
        load_options: LoadModuleOption | int = 0,
        context: typing.Any | None = None,
    ) -> bool:

        ctx_com = getattr(context, "_com_obj", context)
        return bool(self._com_obj.LoadModules(int(load_options), ctx_com))

    @ts_interface
    def unload_modules(self) -> bool:
        return bool(self._com_obj.UnloadModules())

    @ts_interface
    def step_name_exists(self, name: str, group: StepGroup | int = StepGroup.Main) -> bool:
        return bool(self._com_obj.StepNameExists(name, int(group)))

    @ts_interface
    def eval_entry_point_enabled_expression(self, sequence_file: SequenceFile) -> typing.Any:
        return bool(self._com_obj.EvalEntryPointEnabledExpression(sequence_file._com_obj))

    @ts_interface
    def eval_entry_point_enabled_expression_ex(self, edit_args: typing.Any) -> typing.Any:
        arg_com = getattr(edit_args, "_com_obj", edit_args)
        return bool(self._com_obj.EvalEntryPointEnabledExpressionEx(arg_com))

    @ts_interface
    def eval_entry_point_name_expression(self, sequence_file: SequenceFile) -> typing.Any:
        return str(self._com_obj.EvalEntryPointNameExpression(sequence_file._com_obj))

    @ts_interface
    def eval_entry_point_name_expression_ex(
        self,
        edit_args: typing.Any | None = None,
    ) -> typing.Any:
        arg_com = getattr(edit_args, "_com_obj", edit_args)
        return str(self._com_obj.EvalEntryPointNameExpressionEx(arg_com))

    @ts_interface
    def as_property_object(self) -> PropertyObject:
        return PropertyObject(self._com_obj.AsPropertyObject(), self.engine)

    @ts_interface
    def create_new_unique_step_ids(self) -> None:
        self._com_obj.CreateNewUniqueStepIds()

    @ts_interface
    def delete_step(self, index: int, step_group: StepGroup | int = StepGroup.Main) -> None:
        self._com_obj.DeleteStep(index, int(step_group))

    @ts_interface
    def get_entry_point_menu_from_hint(self, menu_name_list: str) -> typing.Any:
        return int(self._com_obj.GetEntryPointMenuFromHint(menu_name_list))

    @ts_interface
    def get_break_on_end(
        self,
        group: StepGroup | int,
        execution: typing.Any | None = None,
    ) -> typing.Any:
        exec_com = getattr(execution, "_com_obj", execution)
        return bool(self._com_obj.GetBreakOnEnd(int(group), exec_com))

    @ts_interface
    def get_break_on_end_settings(
        self,
        group: StepGroup | int,
        execution: typing.Any | None = None,
    ) -> tuple[bool, bool, int, str]:
        exec_com = getattr(execution, "_com_obj", execution)
        return self._com_obj.GetBreakOnEndSettings(int(group), None, None, None, None, exec_com)

    @ts_interface
    def get_effective_type(self) -> typing.Any:

        return SequenceType(self._com_obj.GetEffectiveType())

    @ts_interface
    def set_break_on_end(
        self,
        group: StepGroup | int,
        break_on_end: bool,
        execution: typing.Any | None = None,
    ) -> None:
        exec_com = getattr(execution, "_com_obj", execution)
        self._com_obj.SetBreakOnEnd(int(group), break_on_end, exec_com)

    @ts_interface
    def set_break_on_end_settings(
        self,
        group: StepGroup | int,
        is_set: bool,
        enabled: bool,
        pass_count: int,
        condition: str,
        execution: typing.Any | None = None,
    ) -> None:
        exec_com = getattr(execution, "_com_obj", execution)
        self._com_obj.SetBreakOnEndSettings(
            int(group),
            is_set,
            enabled,
            pass_count,
            condition,
            exec_com,
        )

    @property
    @ts_interface
    def sequence_file(self) -> SequenceFile:
        from py_teststand.sequence.sequence_file import SequenceFile

        return SequenceFile(self._com_obj.SequenceFile, self._engine_ref)

    @ts_interface
    def get_step_by_unique_id(self, unique_id: str) -> Step:
        return Step(self._com_obj.GetStepByUniqueId(unique_id), engine=self.engine)

    @ts_interface
    def get_step_group(self, group: int = StepGroup.Main) -> list[Step]:
        count = self.get_num_steps(group)
        return [self.get_step(i, group) for i in range(count)]


class CPUAffinityForNewThreadOption(IntEnum):
    UseStationOption = 0
    UseAffinityOfCaller = 1
    UseAllCPUs = 2
    UseCustomAffinity = 3


class SequenceCallParameterType(IntEnum):
    Container = 0
    String = 1
    Boolean = 2
    Number = 3
    NamedType = 4
    Reference = 5
    Array = 6
    Enum = 7
    Object = 8


class SequenceContextSelectedStepGroup(IntEnum):
    Setup = 0
    Main = 1
    Cleanup = 2


class SequenceContextStepGroup(IntEnum):
    Setup = 0
    Main = 1
    Cleanup = 2


class SequenceFileType(IntEnum):
    Normal = 0
    Model = 1
    FrontEndCallbacks = 2
    StationCallbacks = 3
    Template = 4


class SeqFileBatchSynchronizationOption(IntEnum):
    UseModelSetting = 1
    NoSync = 2
    Serial = 3
    Parallel = 4
    OneThreadOnly = 5


class FileGlobalsScopeOption(IntEnum):
    SeparateForEachExecution = 0
    AllExecutionsShare = 1


class ModelOption(IntEnum):
    UseStationModel = 0
    NoModel = 1
    RequireSpecificModel = 2
