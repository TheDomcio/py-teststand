from __future__ import annotations

from py_teststand import (
    ConflictResolution,
    ExecutionTypeMask,
    FindFilePromptOption,
    GetSeqFileOption,
    OpenWorkspaceFileOption,
    PropertyFlag,
    ReleaseSeqFileOption,
    RTEOption,
    SearchElement,
    SearchFilterOption,
    SearchOption,
    SourceControlCommand,
    SourceControlStatus,
    WorkspaceObjectType,
)


def test_conflict_resolution_values():

    assert ConflictResolution.Always == 0

    assert ConflictResolution.OnlyIfTypePaletteFilesWillNotBeModified == 1

    assert ConflictResolution.OnlyIfATypePaletteFileHasTheHigherVersion == 2

    assert ConflictResolution.Never == 3


def test_execution_type_mask_values():

    assert ExecutionTypeMask.Normal == 0

    assert ExecutionTypeMask.InitiallyHidden == 0x1

    assert ExecutionTypeMask.TracingInitiallyOff == 0x2

    assert ExecutionTypeMask.InitiallySuspended == 0x4

    assert ExecutionTypeMask.NotRestartable == 0x8

    assert ExecutionTypeMask.CloseWindowWhenDone == 0x10

    assert ExecutionTypeMask.BreakOnStepFailure == 0x20

    assert ExecutionTypeMask.BreakOnSequenceFailure == 0x40

    assert ExecutionTypeMask.AutoWaitAtEndOfSequence == 0x80

    assert ExecutionTypeMask.UseSTA == 0x100

    assert ExecutionTypeMask.DisplayPreloadProgress == 0x200

    assert ExecutionTypeMask.DiscardArgumentsWhenDone == 0x400


def test_execution_type_mask_bitwise():

    mask = ExecutionTypeMask.InitiallyHidden | ExecutionTypeMask.InitiallySuspended

    assert mask & ExecutionTypeMask.InitiallyHidden

    assert mask & ExecutionTypeMask.InitiallySuspended

    assert not (mask & ExecutionTypeMask.TracingInitiallyOff)


def test_property_flags_values():

    assert PropertyFlag.NoneValue == 0

    assert PropertyFlag.NotEditable == 0x1

    assert PropertyFlag.PassByReference == 0x4

    assert PropertyFlag.Hidden == 0x8

    assert PropertyFlag.HiddenInTypes == 0x10

    assert PropertyFlag.IntermediateExprValue == 0x40

    assert PropertyFlag.DontTypeCheckParameter == 0x80


def test_property_flags_bitwise():

    flags = PropertyFlag.NotEditable | PropertyFlag.Hidden

    assert flags & PropertyFlag.NotEditable

    assert flags & PropertyFlag.Hidden

    assert not (flags & PropertyFlag.PassByReference)


def test_find_file_prompt_option_values():

    assert FindFilePromptOption.Disable == 3

    assert FindFilePromptOption.Enable == 2

    assert FindFilePromptOption.HonorUserPreference == 1


def test_get_seq_file_option_values():

    assert GetSeqFileOption.NoneValue == 0

    assert GetSeqFileOption.PreloadModules == 1

    assert GetSeqFileOption.UpdateFromDisk == 2

    assert GetSeqFileOption.AllowTypeConflicts == 4

    assert GetSeqFileOption.CheckModelOptions == 8


def test_open_workspace_file_option_values():

    assert OpenWorkspaceFileOption.NoneValue == 0x0

    assert OpenWorkspaceFileOption.IgnoreMissingFiles == 0x1

    assert OpenWorkspaceFileOption.SearchCurrentDirectory == 0x2

    assert OpenWorkspaceFileOption.UseSearchDirectories == 0x4


def test_release_seq_file_option_values():

    assert ReleaseSeqFileOption.NoneValue == 0

    assert ReleaseSeqFileOption.UnloadFileIfModified == 0x1

    assert ReleaseSeqFileOption.DoNotRunUnloadCallback == 0x2

    assert ReleaseSeqFileOption.UnloadFile == 0x4


def test_rte_option_values():

    assert RTEOption.ShowDialog == 0

    assert RTEOption.Continue == 1

    assert RTEOption.Ignore == 2

    assert RTEOption.Abort == 3

    assert RTEOption.Retry == 4


def test_search_option_values():

    assert SearchOption.MatchCase == 0x1

    assert SearchOption.WholeWordOnly == 0x2

    assert SearchOption.RegExpr == 0x4


def test_search_filter_option_values():

    assert SearchFilterOption.Locals == 0x1

    assert SearchFilterOption.Parameters == 0x2

    assert SearchFilterOption.FileGlobals == 0x4


def test_source_control_command_values():

    assert SourceControlCommand.AddToSC == 1

    assert SourceControlCommand.CheckOut == 3

    assert SourceControlCommand.CheckIn == 4

    assert SourceControlCommand.GetLatest == 5


def test_source_control_status_values():

    assert SourceControlStatus.CheckedOut == 0x2

    assert SourceControlStatus.CheckedOutByUser == 0x1000


def test_workspace_object_type_values():

    assert WorkspaceObjectType.WorkspaceFile == 1

    assert WorkspaceObjectType.ProjectFile == 2

    assert WorkspaceObjectType.Folder == 3

    assert WorkspaceObjectType.SequenceFile == 4

    assert WorkspaceObjectType.OtherFile == 5


def test_search_element_values():

    assert SearchElement.Name == 0x1

    assert SearchElement.Comment == 0x2

    assert SearchElement.StringValue == 0x4
