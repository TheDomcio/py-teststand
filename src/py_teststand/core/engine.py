from __future__ import annotations

import atexit
import functools
import gc
import re
import shutil
import signal
import time
import typing
import warnings
import weakref
from enum import Enum, IntEnum, IntFlag
from pathlib import Path
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    import pythoncom
    import win32com
    import win32com.client
    import win32com.client.gencache
else:
    try:
        import pythoncom
        import win32com
        import win32com.client
        import win32com.client.gencache
    except ImportError:
        pythoncom = None  # type: ignore[assignment]
        win32com = None  # type: ignore[assignment]

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.core.exceptions import TestStandError
from py_teststand.execution.execution import ExecutionMask, ExecutionTypeMask
from py_teststand.messaging.ui_message import MsgBoxType, UIMessageCode
from py_teststand.property.property_object import (
    EvaluationOption,
    PropertyFlag,
    PropertyOption,
    PropValType,
)
from py_teststand.sequence.step_group import StepGroup

if TYPE_CHECKING:
    from py_teststand.core.external_report_viewers import ExternalReportViewers
    from py_teststand.core.images import Images
    from py_teststand.core.search import SearchResults
    from py_teststand.core.utility import Utility
    from py_teststand.execution.edit_args import EditArgs
    from py_teststand.execution.interactive_args import InteractiveArgs
    from py_teststand.execution.output_record_stream import CSVFileOutputRecordStream
    from py_teststand.execution.result_log import ResultLog, ResultLogger
    from py_teststand.execution.thread import Thread
    from py_teststand.execution.watch_expression import WatchExpressions
    from py_teststand.messaging.output_message import OutputMessage
    from py_teststand.messaging.output_messages import OutputMessages
    from py_teststand.property.data_type import PropertyObjectType
    from py_teststand.property.property_object_file import (
        PropertyObjectFile,
        PropertyObjectFileType,
        TypeUsageList,
    )
    from py_teststand.sequence.expression import EvaluationTypes, Expression
    from py_teststand.sequence.location import Locations
    from py_teststand.sequence.sequence import Sequence
    from py_teststand.sequence.sequence_context import SequenceContext
    from py_teststand.sequence.step_type import StepType
    from py_teststand.ui.menu_item import RunTimeMenuItems
    from py_teststand.undo.undo_item_creator import UndoItemCreator
    from py_teststand.undo.undo_stack import UndoStack

from py_teststand.adapters.adapter import Adapter
from py_teststand.execution.execution import Execution
from py_teststand.ext.events import UIMessageHandler
from py_teststand.messaging.ui_message import UIMessage
from py_teststand.property.property_object import PropertyObject
from py_teststand.sequence.sequence_file import SequenceFile
from py_teststand.sequence.step import Step
from py_teststand.station.search_directories import SearchDirectories
from py_teststand.station.station_options import StationOptions
from py_teststand.users.user import User
from py_teststand.users.users_file import UsersFile
from py_teststand.workspace.workspace_file import WorkspaceFile


class FileOpenMode(IntFlag):
    NoneValue = 0
    Truncate = 0x1
    Append = 0x2
    Uniquify = 0x4


class FileVersionAutoIncrement(IntEnum):
    NoneValue = 0
    Major = 1
    Minor = 2
    Revision = 3
    Build = 4


class FindFilePromptOption(IntEnum):
    HonorUserPreference = 1
    Enable = 2
    Disable = 3


class FindFileSearchListOption(IntEnum):
    Ask = 1
    Always = 2
    Never = 3
    AskIgnorePrivileges = 4
    AlwaysIgnorePrivileges = 5


class GetSeqFileOption(IntFlag):
    NoneValue = 0
    PreloadModules = 1
    UpdateFromDisk = 2
    AllowTypeConflicts = 4
    CheckModelOptions = 8
    DoNotRunLoadCallback = 16
    FindFile = 32
    SearchCurrentDir = 64
    OperatorInterfaceFlags = 107
    GetFileOnlyIfInCache = 512


class GetTemplatesFileOption(IntFlag):
    NoneValue = 0
    LoadIfNotLoaded = 1


class HierarchicalExecutionFlag(IntFlag):
    NoneValue = 0
    DontRunSetupAndCleanup = 2
    RunRemainingSequence = 4
    IgnorePreconditions = 8


class FindPathStatusOption(IntFlag):
    PathIsFile = 1
    PathIsDir = 2
    PathNotFound = 3
    PathNotValid = 4


class ConflictResolution(IntEnum):
    Always = 0
    OnlyIfTypePaletteFilesWillNotBeModified = 1
    OnlyIfATypePaletteFileHasTheHigherVersion = 2
    Never = 3


class RTEOption(IntEnum):
    ShowDialog = 0
    Continue = 1
    Ignore = 2
    Abort = 3
    Retry = 4


class AcquireLicense(IntEnum):
    NoneValue = 0
    SuppressStartupDialog = 1
    SuppressStartupDialogIfAlreadyShown = 2
    ShowExitButton = 4


class BrowseExprDialogOption(IntFlag):
    NoneValue = 0
    UsesCRLF = 0x1
    NoContextMenus = 0x2
    ForViewingTypes = 0x4
    ModalToAppMainWind = 0x10000


class CommonDialogOption(IntEnum):
    NoneValue = 0
    ModalToAppMainWind = 0x10000
    ReadOnly = 0x20000
    DisableGotoLocation = 0x80000


class CrashCallbackOption(IntEnum):
    NoneValue = 0
    PreloadFile = 1


class DecimalPointLocalizationOption(IntEnum):
    UsePreference = 1
    UseSystemSetting = 2
    UsePeriod = 3
    UseComma = 4


class ReleaseSeqFileOption(IntEnum):
    NoneValue = 0
    UnloadFileIfModified = 0x1
    DoNotRunUnloadCallback = 0x2
    UnloadFile = 0x4


class WatchExpressionFilterOption(IntEnum):
    NoneValue = 0
    IncludeGlobals = 0x1
    FilterByExecution = 0x2
    FilterBySequenceFile = 0x4
    FilterBySequence = 0x8


class EditBreakAndWatchOption(IntEnum):
    NoneValue = 0
    DisplayBreakpointTab = 0x1
    DisplayWatchExpressionTab = 0x2
    ModalToAppMainWind = 0x10000
    ReadOnly = 0x20000


class EditNumericFormatOption(IntEnum):
    NoneValue = 0
    AllowDefaultFormat = 0x1
    ModalToAppMainWind = 0x10000


class EditPathsDialogOption(IntEnum):
    NoneValue = 0x0
    AllowEditOfReadOnlyFiles = 0x1
    ModalToAppMainWind = 0x10000
    ReadOnly = 0x20000


class LockUnlockDialogOption(IntEnum):
    NoneValue = 0
    Lock = 0x1
    Unlock = 0x2
    HideRememberPasswordControls = 0x4
    ModalToAppMainWind = 0x10000


class WorkspaceBrowserDialogOption(IntEnum):
    NoneValue = 0x0
    Editable = 0x1
    ModalToAppMainWind = 0x10000


class LicenseType(IntEnum):
    DevelopmentSystem = 1
    DebugDeploymentEnv = 2
    BaseDeploymentEngine = 3
    OEM = 4
    Evaluation = 5
    NoLicense = 6
    Temporary = 7
    Other = 8
    CustomEditorDeployment = 9


class ConflictHandler(IntEnum):
    Error = 1
    Prompt = 3
    UseGlobalType = 4


class OpenFileDialogOption(IntEnum):
    NoneValue = 0
    DisableUseAbsPathCheck = 0x1
    InitialSetUseAbsPathCheck = 0x2
    InitialUnsetUseAbsPathCheck = 0x4
    ResolveNonExistentFile = 0x8
    FileMustNotExist = 0x10
    InitialSetBrowseIntoLLB = 0x20
    SaveAsDialog = 0x40
    HideUseAbsPathCheck = 0x80
    UseAbsolutePath = 131
    UseRelativePath = 133
    ShowBrowseIntoLLBCheck = 0x100
    SelectDirectoriesOnly = 0x200
    HideMultiSelectListCtrl = 0x400
    UseSequenceFileFilters = 0x800
    IgnoreInitialPathExtension = 0x1000
    SubstituteMacrosByDefault = 0x2000
    ModalToAppMainWind = 0x10000


class SearchDirectory(IntEnum):
    TestStandDir = 1
    TestStandBinDir = 2
    AdapterSupportDir = 3
    ApplicationDir = 4
    InitialWorkingDir = 5
    WindowsSystemDir = 6
    WindowsDir = 7
    PathEnvironmentVarDir = 8
    CurrentSequenceFileDir = 9
    PublicComponentsDir = 11
    UserComponentsDir = 11
    NIComponentsDir = 12
    CurrentWorkspaceDir = 13
    ContainingProjectDir = 14
    ExplicitDir = 15
    TestStandPublicDir = 16


class ProfilerState(IntEnum):
    NotAState = 0
    Blocked = 1
    InUse = 2
    Aborted = 3
    TimedOut = 4
    Completed = 5


class EditKind(IntEnum):
    NoneValue = 0
    ChangeValue = 1
    Rename = 2
    ModifyComment = 3
    ModifyFlags = 4
    ChangeNumericFormat = 5
    InsertProperty = 6
    DeleteProperty = 7
    MoveProperty = 8
    ReplaceProperty = 9
    InsertStep = 10
    DeleteStep = 11
    MoveStep = 12
    InsertSequence = 13
    DeleteSequence = 14
    MoveSequence = 15
    ChangeObject = 16
    ChangeStep = 17
    ChangeSequenceProperties = 18
    ChangeSequenceFileProperties = 19
    ChangeRunMode = 20
    InsertType = 21
    ChangeRepresentation = 22
    ModifyAttributes = 23
    MoveType = 24


class AdapterKeyName:
    StdCVIAdapterKeyName = "C/CVI Std Prototype Adapter"
    FlexCAdapterKeyName = "DLL Flexible Prototype Adapter"
    LVAdapterKeyName = "G Std Prototype Adapter"
    GAdapterKeyName = "G Std Prototype Adapter"
    SequenceAdapterKeyName = "Sequence Adapter"
    AutomationAdapterKeyName = "Automation Adapter"
    NoneAdapterKeyName = "None Adapter"
    HTBasicAdapterKeyName = "HTBasic Adapter"
    FlexLVAdapterKeyName = "G Flexible VI Adapter"
    FlexCVIAdapterKeyName = "C/CVI Flexible Prototype Adapter"
    DotNetAdapterKeyName = "DotNet Adapter"


class TSError(IntEnum):
    AccessDenied = -17205
    ActiveXAutomationServerException = -17811
    AdapterNoConnectToAutoServer = -18201
    AdapterServerConnectionLost = -18202
    ArrayDimensionExpected = -17344
    ArrayDimensionSizeExpected = -17345
    ArrayIndexOutOfBounds = -17324
    ArrayLocked = -17310
    ArrayTypeExpected = -17343
    AutomationObjNotValid = -17810
    BadExpressionError = -17322
    BadFileFormat = -17100
    BadNetPath = -17202
    BadPropertyOrVariableName = -17319
    CVIAutoCmdFailed = -17704
    CVICantConnectToTecrunServer = -17711
    CVIFuncNotFoundInModule = -17710
    CVIModuleHasUnresolvedReferences = -17709
    CVINonDllModuleNotSupported = -17713
    CVINotReg = -17703
    CVIOleError = -17702
    CVIRegGenericReadError = -17708
    CVIRegKeyNotFound = -17707
    CVIRegValueNotFound = -17706
    CVIRegValueTypeMismatch = -17705
    CVIUnableToTerminateUserProgInCVI = -17712
    CVIVersionNotSupported = -17714
    ConvertedErrorCode = -17009
    CurrentSeqFileNotAvailable = -17330
    DDEFail = -18101
    DLLNotLoadable = -17004
    DNAssemblyMissing = -18700
    DiskFull = -17207
    DispMissingParamID = -17807
    DispMissingParamName = -17806
    DispMissingRequiredArg = -17809
    DispObsoleteMember = -17812
    DispUnknownInterface = -17801
    DispUnknownMemberID = -17803
    DispUnknownMemberName = -17802
    DispUnknownParamID = -17805
    DispUnknownParamName = -17804
    DispWrongNumPositionalParams = -17808
    DoesNotHaveRequiredPrivilege = -18360
    DriveNotReady = -17203
    DuplicateItemOrValue = -17305
    EmptyExpressionError = -17347
    EvaluateFunctionEmptyExpressionError = -17350
    EvaluationContextNotAvailable = -17316
    ExprTypeIncompatibleWithParameter = -17313
    ExprValueNotSuperSetOfParameter = -17314
    ExternalServerUnavailable = -17012
    FailToRegisterClipFormat = -18251
    FileAlreadyExists = -17206
    FileFormatIsOutOfDate = -17099
    FileFormatNewerThanCurrentVersion = -17098
    FileNotConvertableToSeqFile = -17901
    FileWasNotFound = -17208
    FunctionNotFoundInLib = -17005
    IOError = -17200
    IllegalOperationOnValue = -17309
    IncompatibleParameters = -17311
    IndexOutOfRange = -17301
    Int32Overflow = -17010
    Int64Overflow = -17013
    InvalidAdapterName = -17336
    InvalidDrive = -17211
    InvalidPathname = -17204
    InvalidPointer = -17346
    InvalidRegularExpression = -17342
    ItemCannotBeDeleted = -17331
    LVAutoServerError = -18001
    LVMissingRequiredArg = -18003
    LVRTDllNotLoaded = -17338
    LVReportedError = -18002
    LVRunTimeEngineError = -18004
    LVTypeConversionError = -18005
    LV_NXG_AutoBuildError = -18526
    LV_NXG_AutoServerError = -18520
    LV_NXG_MissingRequiredArg = -18522
    LV_NXG_RTEDllNotLoaded = -18525
    LV_NXG_ReportedError = -18521
    LV_NXG_RunTimeEngineError = -18523
    LV_NXG_TypeConversionError = -18524
    LValueExpected = -17318
    LabVIEWTypeNotSupportedInCVI = -17341
    MeasStudioInterfaceNotFound = -18390
    MemoryChecking = -17214
    MethodOrPropertyNotAvailable = -18400
    MismatchedArrayBounds = -17326
    MismatchedItems = -17348
    MissingType = -17328
    ModuleLoadFailure = -17600
    ModuleNotSpecified = -17601
    NameAlreadyInUse = -17327
    NoError = 0
    NoFileAssoc = -18151
    NoItemsInList = -17302
    NotSupported = -17503
    OS_Exception = -17502
    ObjectCannotBeAdded = -17335
    ObjectLocked = -17349
    ObjectTypeIncompatibleWithParameter = -17332
    OperationCanceled = -17604
    OperationFailed = -17500
    OperationInProgress = -17401
    OperationOnlyValidWhenSuspended = -17323
    OperationTimedOut = -17402
    OutOfMemory = -17000
    PathNotFound = -17212
    ProgramError = -17001
    RStringNotFound = -18051
    ReadObjectNotFound = -17339
    RegistryAccessError = -17002
    RegistryItemNotFound = -17003
    RemoteHostNotSpecified = -17853
    RemoteSequenceError = -17850
    RemoteSequenceErrorUnableToConnect = -17851
    RemoteSequenceRemoteExecutionDenied = -17852
    SequenceAborted = -17602
    SequenceTerminated = -17603
    SharingViolation = -17209
    SingleDimensionalNumericArrayExpected = -17317
    SourceCodeControlError = -18370
    StackOverflow = -17008
    StepTypeNotFound = -17337
    ThreadCreationFailed = -17400
    TooManyItems = -17303
    TwoDimensionalNumericArrayExpected = -17340
    TypeCannotBeDeleted = -17333
    TypeConflict = -17329
    TypeLibraryReadError = -18351
    TypeMismatchError = -17321
    TypePaletteFileLoadErrors = -17902
    TypeWithDependingInstancesCannotBeDeleted = -17334
    UInt32Overflow = -17011
    UInt64Overflow = -17014
    UnRecognizedValue = -17304
    UnableToAllocateSystemResource = -17006
    UnableToCloseFile = -17213
    UnableToInitializeOLESystemDLLs = -17007
    UnableToLaunchCVI = -17701
    UnableToOpenDirectory = -17215
    UnableToOpenFile = -17201
    UnableToPassByReference = -17312
    UnexpectedChangeCount = -17351
    UnexpectedEndOfFile = -17216
    UnexpectedSystemError = -17501
    UnexpectedType = -17308
    UnknownFunctionOrSequenceName = -17320
    UnknownType = -17307
    UnknownVariableOrProperty = -17306
    ValueIsInvalidOrOutOfRange = -17300
    VisualStudioAutomationError = -18500
    XMLError = -18600


class InternalOption(IntEnum):
    WarnOnAPICallThroughDispatchInterface = 1
    AutomationAdapterUsesDispatchForDualInterfaces = 2
    UpdateExternalEnvironments = 3
    ApplicationManager = 5
    DisableFloatingWindowsForModalDialogs = 10


class SearchElement(IntFlag):
    Name = 0x1
    Comment = 0x2
    StringValue = 0x4
    NumericValue = 0x8
    BooleanValue = 0x10
    Attributes = 0x20
    TypeName = 0x40
    Enumerators = 0x80
    AllValues = 0x1C
    All = 0xFFFFFFFF


class TestStandPath(IntEnum):
    Bin = 2
    CommonAppData = 5
    Config = 3
    GlobalCommonAppData = 13
    GlobalConfig = 11
    GlobalLocalAppData = 14
    GlobalPublic = 12
    LocalAppData = 6
    NIComponents = 8
    Public = 4
    PublicComponents = 7
    Temp = 9
    Temporary = 10
    TestStand = 1


class ToolMenuItemAttribute(IntFlag):
    SeparatorBefore = 0x1
    Enabled = 0x2
    EditsSelectedFile = 0x4


class ProfilerOption(IntFlag):
    NoOptions = 0
    ExcludeStepTypeModules = 1
    ExcludeStepModules = 2
    ExcludeLoad = 4
    ExcludeUnload = 8
    ExcludeSteps = 16
    ExcludeSynchronization = 32
    ExcludeProcessModels = 64
    ExcludeLocationInformation = 128
    IncludeModulePathsAndEnvironments = 256
    IncludeModuleInputs = 512
    IncludeModuleOutputs = 1024


class OutputMessageSeverityType(IntEnum):
    Information = 0
    Warning = 1
    Error = 2


class OpenWorkspaceFileOption(IntFlag):
    NoneValue = 0x0
    IgnoreMissingFiles = 0x1
    SearchCurrentDirectory = 0x2
    UseSearchDirectories = 0x4


class ParseLookupStringOption(IntFlag):
    NoneValue = 0x0
    TreatArrayIndicesAsSeparateTokens = 0x1


class ReadPropertyObjectFileOption(IntFlag):
    NoneValue = 0x0
    TypesOnly = 0x2


class SaveAllSeqFileOption(IntFlag):
    NoneValue = 0x0
    PromptUser = 0x1


class SerializationOption(IntFlag):
    NoneValue = 0
    SupportNonTypedefMatchingInstances = 4
    SupportOneDimensionalArrays = 1
    SupportTwoDimensionalArrays = 2


class FileOpenStatusFlag(IntFlag):
    InWindow = 0x1


class GetUpdatedStatusOption(IntFlag):
    NoneValue = 0
    GVIDescriptionChanged = 0x1
    GVIChecksumChanged = 0x2
    GVIStateChanged = 0x4
    ExpectedGLLPathChanged = 0x8
    QualifiedNamePresentInGLL = 0x10


class FrontEndCallback(str, Enum):
    LoginLogout = "LoginLogout"


class FileGlobalsScopeOption(IntEnum):
    SeparateForEachExecution = 0
    AllExecutionsShare = 1


class UnloadModuleOption(IntEnum):
    Never = 0
    AfterStepCompletes = 1
    AfterSequenceCompletes = 2
    WhenSequenceFileCloses = 3
    WhenEngineShutsDown = 4


class EscapingOption(IntEnum):
    NoneValue = 0
    SurroundedByQuotes = 1


class AllowAutomaticTypeConflictResolution(IntEnum):
    Always = 0
    OnlyIfTypePaletteFilesWillNotBeModified = 1
    OnlyIfATypePaletteFileHasTheHigherVersion = 2
    Never = 3


class ApplicationLicense(IntEnum):
    Unspecified = 0
    OperatorInterface = 100
    CustomEditor = 200
    SequenceEditor = 300


class ApplicationSite(IntEnum):
    DefaultSite = 0
    ItemList = 1
    PropertyBrowser = 3
    Variables = 2
    Settings = 4


class ArrayBoundsDialogOption(IntFlag):
    NoneValue = 0x0
    InitializeArray = 0x1
    ReturnOkCancel = 0x2


class CheckForModifiedType(IntFlag):
    UseStationOptions = 0x0
    AutoIncrementVersions = 0x1
    Prompt = 0x2
    NoAction = 0x4
    RemoveTypesModifiedMark = 0xC


class CheckUpdatedStatusOption(IntFlag):
    All = 0x0
    GVIDescription = 0x1
    GVIState = 0x4
    GVIChecksum = 0x2
    ExpectedGLLPath = 0x8
    QualifiedNamePresentInGLL = 0x10


class CreateUndoItemOption(IntEnum):
    NoneValue = 0
    CreateOnly = 1


class DeployProjectLibraryOption(IntEnum):
    Deploy = 0
    Undeploy = 1


class DefaultModelCallback(str, Enum):
    DatabaseOptions = "DatabaseOptions"
    GetReportFilePath = "GetReportFilePath"
    LogToDatabase = "LogToDatabase"
    ModelOption = "ModelOption"
    ModelPluginConfiguration = "ModelPluginConfiguration"
    ModelPluginOptions = "ModelPluginOptions"
    ModifyReportEntry = "ModifyReportEntry"
    ModifyReportFooter = "ModifyReportFooter"
    ModifyReportHeader = "ModifyReportHeader"
    PostMainSequence = "PostMainSequence"
    PostUUT = "PostUUT"
    PostUUTLoop = "PostUUTLoop"
    PreMainSequence = "PreMainSequence"
    PreUUT = "PreUUT"
    PreUUTLoop = "PreUUTLoop"
    ProcessCleanup = "ProcessCleanup"
    ProcessSetup = "ProcessSetup"
    ReportOptions = "ReportOptions"
    TestReport = "TestReport"


class WindowsFileDialogFlag(IntFlag):
    READONLY = 0x1
    OVERWRITEPROMPT = 0x2
    HIDEREADONLY = 0x4
    NOCHANGEDIR = 0x8
    SHOWHELP = 0x10
    ENABLEHOOK = 0x20
    ENABLETEMPLATE = 0x40
    ENABLETEMPLATEHANDLE = 0x80
    ALLOWMULTISELECT = 0x200
    EXTENSIONDIFFERENT = 0x400
    PATHMUSTEXIST = 0x800
    FILEMUSTEXIST = 0x1000
    CREATEPROMPT = 0x2000
    SHAREAWARE = 0x4000
    NOREADONLYRETURN = 0x8000
    NOTESTFILECREATE = 0x10000
    NONETWORKBUTTON = 0x20000
    NOLONGNAMES = 0x40000
    EXPLORER = 0x80000
    NODEREFERENCELINKS = 0x100000
    LONGNAMES = 0x200000
    ENABLEINCLUDENOTIFY = 0x400000
    ENABLESIZING = 0x800000
    DONTADDTORECENT = 0x2000000
    FORCESHOWHIDDEN = 0x10000000


class MessageStatus(IntEnum):
    Active = 0
    Fixed = 1
    Ignored = 2


class ContextChangedReason(IntEnum):
    SetContext = 1
    VariableCreatedFromContextMenu = 2
    ExpressionBrowserDialogBox = 3


class ShortcutKey(IntEnum):
    VK_NOT_A_KEY = 0
    VK_F1 = 0x70
    VK_F2 = 0x71
    VK_F3 = 0x72
    VK_F4 = 0x73
    VK_F5 = 0x74
    VK_F6 = 0x75
    VK_F7 = 0x76
    VK_F8 = 0x77
    VK_F9 = 0x78
    VK_F10 = 0x79
    VK_F11 = 0x7A
    VK_F12 = 0x7B


class PerformActionOption(IntFlag):
    No = 1
    Prompt = 2
    Yes = 0


class ProcessCommandLineError(IntEnum):
    NoneValue = 0
    UnrecognizedArgumentError = 1
    CustomError = 2


class DisplayErrorOption(IntFlag):
    NoneValue = 0x0
    ForAll = 0x1


class EditingDenialReason(IntFlag):
    NoneValue = 0
    IsReadOnly = 0x1
    IsNotEditor = 0x2
    IsExecuting = 0x4
    IsLocked = 0x8
    NoFileEditingPrivilege = 0x10


class QueryShutdownOption(IntEnum):
    ShowDialog = 0
    Continue = 1
    Cancel = 2


class RefreshOption(IntFlag):
    AllSequenceFileViewMgrs = 0x1
    AllExecutionViewMgrs = 0x2
    Commands = 0x4
    Captions = 0x8
    AllCommands = 0x10
    AllCaptions = 0x20
    AdapterList = 0x40
    EntryPoints = 0x80
    All = 0xFFFFFFFF


class ReloadFileOption(IntFlag):
    NoneValue = 0x0
    OnlyIfModifiedOnDisk = 0x1
    OnlyIfModifiedInMemory = 0x2


class ReloadFile(IntEnum):
    NoneValue = 0
    Selected = 1
    All = 2


class ValidatePathOption(IntFlag):
    NoneValue = 0x0
    IgnoreAbsolutePath = 0x1
    DoNotCheckIfExists = 0x2
    NotRequiredForExecution = 0x4
    IsCommand = 0x8
    IsDirectory = 0x10
    DoNotAllowEmpty = 0x20


class ImportVIOption(IntFlag):
    NoneValue = 0
    ConfigureExpressVI = 0x1


class ImportVIType(IntEnum):
    ExpressVIWrapper = 0
    ExpressVITemplate = 1
    PropertyNodeVIUpdate = 2
    PropertyNodeVICreate = 3


class InternalStartupOption(IntFlag):
    NoneValue = 0
    TestStandReserved1 = 0x1


class LoadPrototypeOption(IntFlag):
    NoneValue = 0
    MapExistingParameters = 0x1


class LoadTypePaletteFilesOption(IntFlag):
    NoneValue = 0x0
    DisplayErrors = 0x1


class ProtectedObjectOption(IntEnum):
    NoneValue = 0
    NotEditable = 1
    NotViewable = 2


class WindowActivationOption(IntFlag):
    ActivateWhenStepCompletes = 2
    IfActiveReactivateWhenStepCompletes = 3
    NoneValue = 1


class SetTempFileDirectoryOption(IntEnum):
    Default = 0
    DoNotChangeOnLoadOrSave = 1


class SourceControlCommandOption(IntFlag):
    DoNotRecurse = 0x1
    NoneValue = 0x0
    ShowPromptDialog = 0x4


class SourceControlCommand(IntEnum):
    AddToSC = 1
    CheckIn = 4
    CheckOut = 3
    GetLatest = 5


class SourceControlStatus(IntFlag):
    CheckedOut = 0x2
    CheckedOutByUser = 0x1000


class ResetTypeInstanceOption(IntFlag):
    NoneValue = 0
    RecurseSubProperties = 4
    ResetFlags = 2
    ResetValues = 1


class TypeVersionAutoIncrement(IntFlag):
    Build = 4
    Major = 1
    Minor = 2
    NoneValue = 0
    Revision = 3


class VisualStudioDTEVersion(str, Enum):
    V2022 = "VisualStudio.DTE.17.0"
    AlwaysPrompt = "AlwaysPrompt"
    MatchProject = "MatchProject"


SearchOption = typing.Any
SearchFilterOption = typing.Any
UndoItemCreatorAlias = typing.Any
UndoStackAlias = typing.Any
AdapterKeyNameAlias = typing.Any
CSVFileOutputRecordStreamAlias = typing.Any
SelectedBreakpointItem = typing.Any


class Engine(COMWrapper):
    _instances: weakref.WeakSet[Engine] = weakref.WeakSet()
    _is_shutting_down: bool = False
    _loaded_files: typing.ClassVar[dict[str, SequenceFile]] = {}
    _engine: typing.Any

    def __init__(self, com_obj: typing.Any = None) -> None:

        self._co_initialized = False
        if com_obj is None:
            try:
                pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)
                self._co_initialized = True
            except pythoncom.com_error as e:
                hr = getattr(e, "hresult", 0)
                if hr != -2147417850:
                    raise

            try:
                com_obj = win32com.client.gencache.EnsureDispatch("TestStand.Engine.1")
            except pythoncom.com_error as e:
                hr = getattr(e, "hresult", None)
                if hr == -2147221005:
                    raise TestStandError(
                        "TestStand Engine not found. Ensure NI TestStand is installed and matches "
                        "your Python bitness (32-bit Python requires 32-bit TestStand, "
                        "64-bit Python requires 64-bit TestStand).",
                        hresult=hr,
                    ) from e
                try:
                    gen_path = win32com.__gen_path__
                    if Path(gen_path).exists():
                        shutil.rmtree(gen_path)
                    com_obj = win32com.client.gencache.EnsureDispatch("TestStand.Engine.1")
                except pythoncom.com_error as e2:
                    hr2 = getattr(e2, "hresult", None)
                    if hr2 == -2147221005:
                        raise TestStandError(
                            "TestStand Engine not found. Ensure NI TestStand is installed "
                            "and matches your Python bitness (32-bit Python requires "
                            "32-bit TestStand, 64-bit Python requires 64-bit TestStand).",
                            hresult=hr2,
                        ) from e2
                    raise TestStandError(
                        f"Failed to initialize TestStand Engine: {e2}",
                        hresult=hr2,
                    ) from e2
            except Exception as e:
                try:
                    com_obj = win32com.client.DispatchEx("TestStand.Engine.1")
                except pythoncom.com_error as dispatch_error:
                    raise TestStandError(
                        "TestStand Engine not found. Ensure NI TestStand is installed and matches "
                        "your Python bitness (32-bit Python requires 32-bit TestStand, "
                        "64-bit Python requires 64-bit TestStand).",
                        hresult=getattr(dispatch_error, "hresult", None),
                    ) from dispatch_error
                warnings.warn(
                    f"Failed early binding: {e}. Falling back to dynamic dispatch.",
                    stacklevel=2,
                )

        _com: typing.Any = com_obj
        super().__init__(_com, self)
        self._engine = _com

        _self_ref = weakref.ref(self)

        def _atexit_shutdown() -> None:
            obj = _self_ref()
            if obj is not None:
                obj.shutdown()

        def _signal_shutdown(_s: typing.Any, _f: typing.Any) -> None:
            obj = _self_ref()
            if obj is not None:
                obj.shutdown()

        self._atexit_callable = _atexit_shutdown
        atexit.register(_atexit_shutdown)
        signal.signal(signal.SIGTERM, _signal_shutdown)
        signal.signal(signal.SIGINT, _signal_shutdown)

        is_mock = type(com_obj).__name__ in ("MagicMock", "Mock") or "MockCOM" in str(type(com_obj))
        if not is_mock:
            try:
                self.station_options.disable_popups = True
            except Exception:
                try:
                    opts = self.station_options
                    opts.rte_option = RTEOption.Abort
                    opts.prompt_to_find_files = False
                    opts.type_version_auto_increment_prompt_opt = False
                    opts.use_dialog_for_check_out = False
                except Exception:
                    pass
            try:
                self._engine.LoadTypePaletteFilesEx(int(ConflictHandler.Error), 0)
            except pythoncom.com_error:
                try:
                    self._engine.LoadTypePaletteFiles()
                except pythoncom.com_error:
                    pass

        self._station_options: StationOptions | None = None
        self._ui_handler: UIMessageHandler | None = None
        self._instances.add(self)

    def __enter__(self) -> Engine:

        return self

    def __exit__(self, exc_type: typing.Any, exc_val: typing.Any, exc_tb: typing.Any) -> None:

        self.shutdown()
        self.release()

    def release(self) -> None:

        try:
            if hasattr(self, "_engine"):
                self._engine = None
            if hasattr(self, "_com_obj"):
                object.__setattr__(self, "_com_obj", None)
        except Exception:
            pass

        if getattr(self, "_co_initialized", False):
            try:
                if pythoncom is not None:
                    pythoncom.CoUninitialize()
                self._co_initialized = False
            except Exception:
                pass

    def __del__(self) -> None:

        try:
            self.release()
        except Exception:
            pass

    @property
    def ui_handler(self) -> UIMessageHandler:

        if self._ui_handler is None:
            self._ui_handler = UIMessageHandler(self)
        return self._ui_handler

    @property
    def is_mock(self) -> bool:
        return type(self._engine).__name__ in ("MagicMock", "Mock") or "MockCOM" in str(
            type(self._engine)
        )

    @ts_interface
    def abort_all(self) -> None:
        self._engine.AbortAll()

    @ts_interface
    def acquire_license(
        self,
        license: LicenseType | int,
        options: AcquireLicense | int = 0,
    ) -> int:
        return int(self._engine.AcquireLicense(int(license), int(options)))

    @ts_interface
    def add_image(self, image: typing.Any, image_name: str) -> typing.Any:
        return int(self._engine.AddImage(image, image_name))

    @property
    @ts_interface
    def always_goto_cleanup_on_failure(self) -> bool:
        return bool(self._engine.AlwaysGotoCleanupOnFailure)

    @always_goto_cleanup_on_failure.setter
    @ts_interface
    def always_goto_cleanup_on_failure(self, value: bool) -> None:
        self._engine.AlwaysGotoCleanupOnFailure = value

    @property
    @ts_interface
    def application_is_editor(self) -> bool:
        return bool(self._engine.ApplicationIsEditor)

    @application_is_editor.setter
    @ts_interface
    def application_is_editor(self, value: bool) -> None:
        self._engine.ApplicationIsEditor = value

    @property
    @ts_interface
    def application_license(self) -> typing.Any:
        return LicenseType(self._engine.ApplicationLicense)

    @functools.cached_property
    @ts_interface
    def application_version_string(self) -> str | None:
        try:
            return str(self._engine.ApplicationVersionString)
        except Exception:
            return None

    @property
    @ts_interface
    def app_main_hwnd(self) -> int:
        return int(self._engine.AppMainHwnd)

    @property
    @ts_interface
    def auto_login_system_user(self) -> bool:
        return bool(self._engine.AutoLoginSystemUser)

    @auto_login_system_user.setter
    @ts_interface
    def auto_login_system_user(self, value: bool) -> None:
        self._engine.AutoLoginSystemUser = value

    @ts_interface
    def begin_profiling(self) -> None:
        self._engine.BeginProfiling()

    @ts_interface
    def break_all(self) -> None:
        self._engine.BreakAll()

    @property
    @ts_interface
    def bin_directory(self) -> str:
        return str(self._engine.BinDirectory)

    @property
    @ts_interface
    def break_on_rte(self) -> bool:
        return bool(self._engine.BreakOnRTE)

    @break_on_rte.setter
    @ts_interface
    def break_on_rte(self, value: bool) -> None:
        self._engine.BreakOnRTE = value

    @property
    @ts_interface
    def breakpoints_enabled(self) -> bool:
        return bool(self._engine.BreakpointsEnabled)

    @breakpoints_enabled.setter
    @ts_interface
    def breakpoints_enabled(self, value: bool) -> None:
        self._engine.BreakpointsEnabled = value

    @property
    @ts_interface
    def build_version(self) -> int:
        return int(self._engine.BuildVersion)

    @property
    @ts_interface
    def builtin_data_types(self) -> PropertyObject:
        from py_teststand.property.property_object import PropertyObject

        return PropertyObject(self._engine.BuiltinDataTypes, self)

    @ts_interface
    def call_front_end_callback(
        self, sequence_name: str, argument_list: PropertyObject
    ) -> Execution:
        return Execution(
            self._engine.CallFrontEndCallback(sequence_name, argument_list._com_obj), self
        )

    @ts_interface
    def call_front_end_callback_ex(
        self,
        sequence_name: str,
        argument_list: PropertyObject,
        handler_type: ConflictHandler | int = ConflictHandler.Error,
        reserved: int = 0,
    ) -> Execution:
        return Execution(
            self._engine.CallFrontEndCallbackEx(
                sequence_name, argument_list._com_obj, int(handler_type), reserved
            ),
            self,
        )

    @ts_interface
    def can_create_step(self, adapter_key_name: str, step_type_name: str) -> typing.Any:
        return bool(self._engine.CanCreateStep(adapter_key_name, step_type_name))

    @ts_interface
    def check_expression(
        self,
        evaluation_context: PropertyObject | None,
        expression_str: str,
        evaluation_options: EvaluationOption | int = 0,
    ) -> tuple[bool, str, int, int]:
        context_com = evaluation_context._com_obj if evaluation_context else None
        error_description = ""
        start_err_pos = 0
        end_err_pos = 0
        is_valid = self._engine.CheckExpression(
            context_com,
            expression_str,
            int(evaluation_options),
            error_description,
            start_err_pos,
            end_err_pos,
        )
        return bool(is_valid), str(error_description), int(start_err_pos), int(end_err_pos)

    @ts_interface
    def check_expr_syntax(self, expression_str: str) -> typing.Any:
        error_description = ""
        start_err_pos = 0
        end_err_pos = 0
        is_valid = self._engine.CheckExprSyntax(
            expression_str, error_description, start_err_pos, end_err_pos
        )
        return bool(is_valid), str(error_description), int(start_err_pos), int(end_err_pos)

    @property
    @ts_interface
    def check_out_files_when_edited(self) -> bool:
        return bool(self._engine.CheckOutFilesWhenEdited)

    @check_out_files_when_edited.setter
    @ts_interface
    def check_out_files_when_edited(self, value: bool) -> None:
        self._engine.CheckOutFilesWhenEdited = value

    @property
    @ts_interface
    def check_out_only_selected_files(self) -> bool:
        return bool(self._engine.CheckOutOnlySelectedFiles)

    @check_out_only_selected_files.setter
    @ts_interface
    def check_out_only_selected_files(self, value: bool) -> None:
        self._engine.CheckOutOnlySelectedFiles = value

    @ts_interface
    def clear_file_password_cache(self) -> None:
        self._engine.ClearFilePasswordCache()

    @ts_interface
    def commit_globals_to_disk(self, prompt_on_save_conflicts: bool = True) -> typing.Any:
        self._engine.CommitGlobalsToDisk(bool(prompt_on_save_conflicts))

    @property
    @ts_interface
    def computer_name(self) -> str:
        return str(self._engine.ComputerName)

    @property
    @ts_interface
    def config_directory(self) -> str:
        return str(self._engine.ConfigDirectory)

    @property
    @ts_interface
    def config_file(self) -> PropertyObjectFile:
        from py_teststand.property.property_object_file import PropertyObjectFile

        return PropertyObjectFile(self._engine.ConfigFile, self)

    @ts_interface
    def construct_tool_menus(self, edit_args: typing.Any | None = None) -> typing.Any:
        return int(self._engine.ConstructToolMenus(edit_args))

    @ts_interface
    def copy_property_object(self, src_obj: PropertyObject) -> typing.Any:
        from py_teststand.property.property_object import PropertyObject

        return PropertyObject(self._engine.CopyPropertyObject(src_obj._com_obj), self)

    @ts_interface
    def create_new_unique_step_ids(self, steps: list[Step]) -> typing.Any:
        step_coms = [s._com_obj for s in steps]
        self._engine.CreateNewUniqueStepIds(step_coms)

    @ts_interface
    def create_temp_file(self, base_name: str, extension: str, directory: str = "") -> typing.Any:
        return str(self._engine.CreateTempFile(base_name, extension, directory))

    @property
    @ts_interface
    def current_user(self) -> typing.Any:
        user_com = self._engine.CurrentUser
        return User(user_com, self) if user_com else None

    @current_user.setter
    @ts_interface
    def current_user(self, value: User | None) -> None:
        user_com = value._com_obj if value else None
        self._engine.CurrentUser = user_com

    @ts_interface
    def current_user_has_privilege(self, privilege_name: str) -> typing.Any:
        return bool(self._engine.CurrentUserHasPrivilege(privilege_name))

    @property
    @ts_interface
    def current_workspace_file(self) -> WorkspaceFile | None:
        ws_com = self._engine.CurrentWorkspaceFile
        return WorkspaceFile(ws_com, self) if ws_com else None

    @current_workspace_file.setter
    @ts_interface
    def current_workspace_file(self, value: WorkspaceFile | None) -> None:
        ws_com = value._com_obj if value else None
        self._engine.CurrentWorkspaceFile = ws_com

    @property
    @ts_interface
    def custom_data_types(self) -> PropertyObject:
        from py_teststand.property.property_object import PropertyObject

        return PropertyObject(self._engine.CustomDataTypes, self)

    @property
    @ts_interface
    def cvi_adapter_execute_steps_in_cvi(self) -> bool:
        return bool(self._engine.CVIAdapter_ExecuteStepsInCVI)

    @cvi_adapter_execute_steps_in_cvi.setter
    @ts_interface
    def cvi_adapter_execute_steps_in_cvi(self, value: bool) -> None:
        self._engine.CVIAdapter_ExecuteStepsInCVI = value

    @property
    @ts_interface
    def cvi_adapter_external_cvi_prj(self) -> str:
        return str(self._engine.CVIAdapter_ExternalCVIPrj)

    @cvi_adapter_external_cvi_prj.setter
    @ts_interface
    def cvi_adapter_external_cvi_prj(self, value: str) -> None:
        self._engine.CVIAdapter_ExternalCVIPrj = value

    @property
    @ts_interface
    def default_adapter(self) -> str:
        return str(self._engine.DefaultAdapter)

    @default_adapter.setter
    @ts_interface
    def default_adapter(self, value: str) -> None:
        self._engine.DefaultAdapter = value

    @property
    @ts_interface
    def default_adapter_index(self) -> int:
        return int(self._engine.DefaultAdapterIndex)

    @default_adapter_index.setter
    @ts_interface
    def default_adapter_index(self, value: int) -> None:
        self._engine.DefaultAdapterIndex = value

    @ts_interface
    def delocalize_expression(
        self,
        localized_expression_string: str,
        decimal_point_option: DecimalPointLocalizationOption | int,
    ) -> str:
        return str(
            self._engine.DelocalizeExpression(
                localized_expression_string, int(decimal_point_option)
            )
        )

    @property
    @ts_interface
    def disable_results(self) -> bool:
        return bool(self._engine.DisableResults)

    @disable_results.setter
    @ts_interface
    def disable_results(self, value: bool) -> None:
        self._engine.DisableResults = value

    @ts_interface
    def display_adapter_config_dialog(
        self,
        dlg_title: str = "",
        adapter_selector_read_only: bool = False,
        adapter_cfg_read_only: bool = False,
        hide_adapter_selector: bool = False,
        modal_to_app_main_wind: bool = False,
    ) -> bool:
        return bool(
            self._engine.DisplayAdapterConfigDialog(
                dlg_title,
                bool(adapter_selector_read_only),
                bool(adapter_cfg_read_only),
                bool(hide_adapter_selector),
                bool(modal_to_app_main_wind),
            )
        )

    @ts_interface
    def display_breakpoint_dialog(
        self,
        dlg_title: str,
        sequence_context: SequenceContext,
        execution: Execution | None,
        selected_step: Step | None,
        step_group: StepGroup | int,
        dlg_options: CommonDialogOption | int = 0,
    ) -> bool:
        exec_com = execution._com_obj if execution else None
        step_com = selected_step._com_obj if selected_step else None
        return bool(
            self._engine.DisplayBreakpointDialog(
                dlg_title,
                sequence_context._com_obj,
                exec_com,
                step_com,
                int(step_group),
                int(dlg_options),
            )
        )

    @ts_interface
    def display_browse_expr_dialog(
        self,
        dlg_title: str,
        sequence_context: SequenceContext,
        expression_in: str,
        selection_start_in: int,
        selection_end_in: int,
        initial_variable_name: str,
        uses_crlf: bool,
        modal_to_app_main_wind: bool,
    ) -> tuple[bool, str, int, int]:
        expression_out = ""
        selection_start_out = 0
        selection_end_out = 0
        result = self._engine.DisplayBrowseExprDialog(
            dlg_title,
            sequence_context._com_obj,
            expression_in,
            int(selection_start_in),
            int(selection_end_in),
            initial_variable_name,
            bool(uses_crlf),
            bool(modal_to_app_main_wind),
            expression_out,
            selection_start_out,
            selection_end_out,
        )
        return bool(result), str(expression_out), int(selection_start_out), int(selection_end_out)

    @ts_interface
    def display_browse_expr_dialog_ex(
        self,
        dlg_title: str,
        object_to_browse: PropertyObject,
        expression_in: str,
        selection_start_in: int,
        selection_end_in: int,
        initial_variable_name: str,
        dlg_options: BrowseExprDialogOption | int,
    ) -> tuple[bool, str, int, int]:
        expression_out = ""
        selection_start_out = 0
        selection_end_out = 0
        result = self._engine.DisplayBrowseExprDialogEx(
            dlg_title,
            object_to_browse._com_obj,
            expression_in,
            int(selection_start_in),
            int(selection_end_in),
            initial_variable_name,
            int(dlg_options),
            expression_out,
            selection_start_out,
            selection_end_out,
        )
        return bool(result), str(expression_out), int(selection_start_out), int(selection_end_out)

    @ts_interface
    def display_browse_property_object_dialog(
        self,
        dlg_title: str,
        object_to_browse: PropertyObject,
        initial_location: str,
        dlg_options: CommonDialogOption | int = 0,
    ) -> None:
        self._engine.DisplayBrowsePropertyObjectDialog(
            dlg_title, object_to_browse._com_obj, initial_location, int(dlg_options)
        )

    @ts_interface
    def display_configure_type_palettes_dialog(
        self, dlg_title: str, dlg_options: CommonDialogOption | int = 0
    ) -> bool:
        return bool(self._engine.DisplayConfigureTypePalettesDialog(dlg_title, int(dlg_options)))

    @ts_interface
    def display_edit_break_and_watch_dialog(
        self, dlg_title: str, dlg_options: EditBreakAndWatchOption | int = 0
    ) -> tuple[bool, SelectedBreakpointItem | None]:
        selected_item_com = None
        result = self._engine.DisplayEditBreakAndWatchDialog(
            dlg_title, int(dlg_options), selected_item_com
        )
        item = SelectedBreakpointItem(selected_item_com, self) if selected_item_com else None
        return bool(result), item

    @ts_interface
    def display_edit_numeric_format_dialog(
        self,
        dlg_title: str,
        numeric_format: str,
        dlg_options: EditNumericFormatOption | int = 0,
        sample_number: float = 1.5,
    ) -> tuple[bool, str]:
        num_format_io = numeric_format
        result = self._engine.DisplayEditNumericFormatDialog(
            dlg_title, num_format_io, int(dlg_options), float(sample_number)
        )
        return bool(result), str(num_format_io)

    @ts_interface
    def display_edit_numeric_format_dialog_ex(
        self,
        dlg_title: str,
        numeric_format: str,
        dlg_options: EditNumericFormatOption | int = 0,
        sample_number: float = 1.5,
    ) -> tuple[bool, str, bool]:
        num_format_io = numeric_format
        valid_format = False
        result = self._engine.DisplayEditNumericFormatDialogEx(
            dlg_title, num_format_io, valid_format, int(dlg_options), float(sample_number)
        )
        return bool(result), str(num_format_io), bool(valid_format)

    @ts_interface
    def display_edit_paths_in_files_dialog(
        self,
        dlg_title: str,
        dlg_options: EditPathsDialogOption | int = 0,
        initial_file: PropertyObjectFile | None = None,
    ) -> bool:
        file_com = initial_file._com_obj if initial_file else None
        return bool(
            self._engine.DisplayEditPathsInFilesDialog(dlg_title, int(dlg_options), file_com)
        )

    @ts_interface
    def display_edit_user_dialog(
        self, dlg_title: str, user: User, modal_to_app_main_wind: bool = False
    ) -> bool:
        return bool(
            self._engine.DisplayEditUserDialog(
                dlg_title, user._com_obj, bool(modal_to_app_main_wind)
            )
        )

    @ts_interface
    def display_environment_configuration_dialog(
        self, dlg_options: int = 0, path: str = ""
    ) -> tuple[bool, str]:
        path_io = path
        result = self._engine.DisplayEnvironmentConfigurationDialog(int(dlg_options), path_io)
        return bool(result), str(path_io)

    @ts_interface
    def display_error_dialog(
        self,
        dlg_title: str,
        error_message: str,
        error_code: int,
        dlg_options: CommonDialogOption | int = 0,
    ) -> None:
        self._engine.DisplayErrorDialog(dlg_title, error_message, int(error_code), int(dlg_options))

    @ts_interface
    def display_expression_edit_options_dialog(
        self, dlg_title: str = "", dlg_options: CommonDialogOption | int = 0
    ) -> bool:
        return bool(self._engine.DisplayExpressionEditOptionsDialog(dlg_title, int(dlg_options)))

    @ts_interface
    def display_external_viewer_dialog(
        self,
        dlg_title: str,
        read_only: bool,
        modal_to_app_main_wind: bool = False,
    ) -> bool:
        return bool(
            self._engine.DisplayExternalViewerDialog(
                dlg_title, bool(read_only), bool(modal_to_app_main_wind)
            )
        )

    @ts_interface
    def display_file_dialog(
        self,
        dlg_title: str,
        ok_button_text: str,
        initial_path: str,
        open_file_dialog_flags: OpenFileDialogOption | int = 0,
        default_extension: str = "",
        win32_flags: int = 0x01 | 0x04,
        file_filter: str = "",
        current_file: PropertyObjectFile | None = None,
        file_filter_index: int = 0,
        dir_history_list: list[str] | None = None,
    ) -> tuple[bool, list[str], list[str], int, list[str]]:
        selected_paths = []
        absolute_paths = []
        file_com = current_file._com_obj if current_file else None
        filter_idx_io = file_filter_index
        history_io = dir_history_list if dir_history_list is not None else []

        result = self._engine.DisplayFileDialog(
            dlg_title,
            ok_button_text,
            initial_path,
            selected_paths,
            absolute_paths,
            int(open_file_dialog_flags),
            default_extension,
            int(win32_flags),
            file_filter,
            file_com,
            filter_idx_io,
            history_io,
        )
        return (
            bool(result),
            list(selected_paths),
            list(absolute_paths),
            int(filter_idx_io),
            list(history_io),
        )

    @ts_interface
    def display_help_file(
        self,
        html_file: str,
        help_file: str = "",
        table_of_contents_file: str = "",
        index_file: str = "",
        home_file: str = "",
        window_caption: str = "",
    ) -> int:
        return int(
            self._engine.DisplayHelpFile(
                html_file,
                help_file,
                table_of_contents_file,
                index_file,
                home_file,
                window_caption,
            )
        )

    @ts_interface
    def display_help_topic(
        self,
        tag_id: int,
        help_file: str = "",
        table_of_contents_file: str = "",
        index_file: str = "",
        home_file: str = "",
        window_caption: str = "",
    ) -> int:
        return int(
            self._engine.DisplayHelpTopic(
                int(tag_id),
                help_file,
                table_of_contents_file,
                index_file,
                home_file,
                window_caption,
            )
        )

    @ts_interface
    def display_help_topic_ex(self, help_context_id: str) -> typing.Any:
        self._engine.DisplayHelpTopicEx(help_context_id)

    @ts_interface
    def display_io_configuration_options_dialog(self) -> bool:
        return bool(self._engine.DisplayIOConfigurationOptionsDialog())

    @ts_interface
    def display_lock_unlock_dialog(
        self,
        dlg_title: str = "",
        dlg_msg: str = "",
        prop_object: PropertyObject | None = None,
        options: LockUnlockDialogOption | int = 0,
        password_string: str | None = None,
    ) -> tuple[bool, str]:
        obj_com = prop_object._com_obj if prop_object else None
        password_io = password_string if password_string is not None else ""
        result = self._engine.DisplayLockUnlockDialog(
            dlg_title, dlg_msg, obj_com, int(options), password_io
        )
        return bool(result), str(password_io)

    @ts_interface
    def display_login_dialog(
        self,
        dlg_title: str,
        initial_login_name: str,
        initial_password: str,
        modal_to_app_main_wind: bool,
    ) -> tuple[bool, User | None]:
        user_com = None
        result = self._engine.DisplayLoginDialog(
            dlg_title,
            initial_login_name,
            initial_password,
            bool(modal_to_app_main_wind),
            user_com,
        )
        user = User(user_com, self) if user_com else None
        return bool(result), user

    @ts_interface
    def display_loop_on_steps_dialog(
        self,
        dlg_title: str,
        selected_step: Step,
        modal_to_app_main_wind: bool,
    ) -> tuple[bool, int, str]:
        loop_count_out = 0
        stop_expr_out = ""
        result = self._engine.DisplayLoopOnStepsDialog(
            dlg_title,
            selected_step._com_obj,
            bool(modal_to_app_main_wind),
            loop_count_out,
            stop_expr_out,
        )
        return bool(result), int(loop_count_out), str(stop_expr_out)

    @ts_interface
    def display_message_box(
        self,
        dlg_title: str,
        message_text: str,
        msg_box_type: MsgBoxType | int = 0x40,
        dlg_options: CommonDialogOption | int = 0,
        win32_flags: int = 0,
    ) -> int:
        return int(
            self._engine.DisplayMessageBox(
                dlg_title, message_text, int(msg_box_type), int(dlg_options), int(win32_flags)
            )
        )

    @ts_interface
    def display_new_user_dialog(
        self, dlg_title: str, modal_to_app_main_wind: bool
    ) -> tuple[bool, User | None]:
        user_com = None
        result = self._engine.DisplayNewUserDialog(
            dlg_title, bool(modal_to_app_main_wind), user_com
        )
        user = User(user_com, self) if user_com else None
        return bool(result), user

    @ts_interface
    def display_open_file_dialog(
        self,
        dlg_title: str,
        ok_button_text: str,
        initial_path: str,
        modal_to_app_main_wind: bool,
        open_file_dialog_flags: OpenFileDialogOption | int = 0,
        default_extension: str = "",
        win32_flags: int = 0x01 | 0x04,
        file_filter: str = "",
        current_sequence_file: SequenceFile | None = None,
    ) -> tuple[bool, str, str]:
        selected_path_io = ""
        absolute_path_io = ""
        file_com = current_sequence_file._com_obj if current_sequence_file else None
        result = self._engine.DisplayOpenFileDialog(
            dlg_title,
            ok_button_text,
            initial_path,
            bool(modal_to_app_main_wind),
            selected_path_io,
            absolute_path_io,
            int(open_file_dialog_flags),
            default_extension,
            int(win32_flags),
            file_filter,
            file_com,
        )
        return bool(result), str(selected_path_io), str(absolute_path_io)

    @ts_interface
    def display_options_dialog(
        self, dlg_title: str, read_only: bool, modal_to_app_main_wind: bool
    ) -> bool:
        return bool(
            self._engine.DisplayOptionsDialog(
                dlg_title, bool(read_only), bool(modal_to_app_main_wind)
            )
        )

    @ts_interface
    def display_password_protect_type_definitions_dialog(
        self,
        type_definitions: list[PropertyObject],
        dlg_options: CommonDialogOption | int = 0,
    ) -> tuple[bool, list[PropertyObject]]:
        type_coms = [t._com_obj for t in type_definitions]
        modified_types_com = []
        result = self._engine.DisplayPasswordProtectTypeDefinitionsDialog(
            type_coms, modified_types_com, int(dlg_options)
        )
        modified_types = [PropertyObject(t, self) for t in modified_types_com]
        return bool(result), modified_types

    @ts_interface
    def display_precondition_builder_dialog(
        self,
        dlg_title: str,
        precondition_expr: str,
        sequence: Sequence,
        dlg_options: CommonDialogOption | int = 0,
        sequence_context: SequenceContext | None = None,
    ) -> tuple[bool, str]:
        expr_io = precondition_expr
        ctx_com = sequence_context._com_obj if sequence_context else None
        result = self._engine.DisplayPreconditionBuilderDialog(
            dlg_title, expr_io, sequence._com_obj, int(dlg_options), ctx_com
        )
        return bool(result), str(expr_io)

    @ts_interface
    def display_precondition_dialog(
        self,
        dlg_title: str,
        sequence: Sequence,
        read_only: bool,
        modal_to_app_main_wind: bool,
        initial_step: Step | None = None,
    ) -> bool:
        step_com = initial_step._com_obj if initial_step else None
        return bool(
            self._engine.DisplayPreconditionDialog(
                dlg_title,
                sequence._com_obj,
                bool(read_only),
                bool(modal_to_app_main_wind),
                step_com,
            )
        )

    @ts_interface
    def display_runtime_error_dialog(
        self,
        dlg_title: str,
        error_message: str,
        in_cleanup_step_group: bool,
        modal_to_app_main_wind: bool,
    ) -> tuple[bool, bool, RTEOption]:
        display_on_next_out, suspend_execution_out, rte_action_out = (
            self._engine.DisplayRunTimeErrorDialog(
                dlg_title,
                error_message,
                bool(in_cleanup_step_group),
                bool(modal_to_app_main_wind),
            )
        )
        return (
            bool(display_on_next_out),
            bool(suspend_execution_out),
            RTEOption(rte_action_out),
        )

    @ts_interface
    def display_runtime_error_dialog_ex(
        self,
        dlg_title: str,
        sequence_context: SequenceContext,
        dlg_options: CommonDialogOption | int = 0,
    ) -> tuple[bool, bool, bool, RTEOption]:
        (
            suspend_out,
            dont_show_exec_out,
            dont_show_batch_out,
            rte_action_out,
        ) = self._engine.DisplayRunTimeErrorDialogEx(
            dlg_title,
            sequence_context._com_obj,
            int(dlg_options),
        )
        return (
            bool(suspend_out),
            bool(dont_show_exec_out),
            bool(dont_show_batch_out),
            RTEOption(rte_action_out),
        )

    @ts_interface
    def display_search_dir_dialog(
        self, dlg_title: str, read_only: bool, modal_to_app_main_wind: bool
    ) -> bool:
        return bool(
            self._engine.DisplaySearchDirDialog(
                dlg_title, bool(read_only), bool(modal_to_app_main_wind)
            )
        )

    @ts_interface
    def display_seq_file_prop_dialog(
        self,
        dlg_title: str,
        sequence_file: SequenceFile,
        read_only: bool,
        modal_to_app_main_wind: bool,
        show_view_contents_btn: bool,
    ) -> tuple[bool, bool]:
        view_contents_out = False
        result = self._engine.DisplaySeqFilePropDialog(
            dlg_title,
            sequence_file._com_obj,
            bool(read_only),
            bool(modal_to_app_main_wind),
            bool(show_view_contents_btn),
            view_contents_out,
        )
        return bool(result), bool(view_contents_out)

    @ts_interface
    def display_sequence_file_callbacks_dialog(
        self,
        dlg_title: str,
        sequence_file: SequenceFile,
        dlg_options: CommonDialogOption | int = 0,
    ) -> tuple[bool, str, int, int]:
        seq_to_edit_out = ""
        added_out = 0
        deleted_out = 0
        result = self._engine.DisplaySequenceFileCallbacksDialog(
            dlg_title,
            sequence_file._com_obj,
            int(dlg_options),
            seq_to_edit_out,
            added_out,
            deleted_out,
        )
        return bool(result), str(seq_to_edit_out), int(added_out), int(deleted_out)

    @ts_interface
    def display_sequence_prop_dialog(
        self,
        dlg_title: str,
        sequence: Sequence,
        read_only: bool,
        modal_to_app_main_wind: bool,
        show_view_contents_btn: bool,
    ) -> tuple[bool, bool]:
        view_contents_out = False
        result = self._engine.DisplaySequencePropDialog(
            dlg_title,
            sequence._com_obj,
            bool(read_only),
            bool(modal_to_app_main_wind),
            bool(show_view_contents_btn),
            view_contents_out,
        )
        return bool(result), bool(view_contents_out)

    @ts_interface
    def display_step_prop_dialog(
        self,
        dlg_title: str,
        step: Step,
        read_only: bool,
        modal_to_app_main_wind: bool,
        show_view_contents_btn: bool,
    ) -> tuple[bool, bool, bool]:
        view_contents_out = False
        modified_out = False
        result = self._engine.DisplayStepPropDialog(
            dlg_title,
            step._com_obj,
            bool(read_only),
            bool(modal_to_app_main_wind),
            bool(show_view_contents_btn),
            view_contents_out,
            modified_out,
        )
        return bool(result), bool(view_contents_out), bool(modified_out)

    @ts_interface
    def display_step_type_menu_editor(
        self,
        dlg_title: str,
        for_substeps: bool,
        dlg_options: CommonDialogOption | int = 0,
    ) -> bool:
        return bool(
            self._engine.DisplayStepTypeMenuEditor(dlg_title, bool(for_substeps), int(dlg_options))
        )

    @ts_interface
    def display_step_type_menu_editor_ex(
        self,
        dlg_title: str,
        selected_file: PropertyObjectFile,
        for_substeps: bool,
        dlg_options: CommonDialogOption | int = 0,
    ) -> bool:
        return bool(
            self._engine.DisplayStepTypeMenuEditorEx(
                dlg_title, selected_file._com_obj, bool(for_substeps), int(dlg_options)
            )
        )

    @ts_interface
    def display_tool_menu_dialog(
        self, dlg_title: str, read_only: bool, modal_to_app_main_wind: bool
    ) -> bool:
        return bool(
            self._engine.DisplayToolMenuDialog(
                dlg_title, bool(read_only), bool(modal_to_app_main_wind)
            )
        )

    @ts_interface
    def display_unlock_type_definitions_dialog(
        self,
        type_definitions: list[PropertyObject],
        dlg_options: LockUnlockDialogOption | int = 0,
    ) -> tuple[bool, bool]:
        type_coms = [t._com_obj for t in type_definitions]
        all_unlocked_out = False
        result = self._engine.DisplayUnlockTypeDefinitionsDialog(
            type_coms, all_unlocked_out, int(dlg_options)
        )
        return bool(result), bool(all_unlocked_out)

    @ts_interface
    def display_workspace_browser_dialog(
        self,
        dlg_title: str,
        dlg_options: WorkspaceBrowserDialogOption | int = 0,
    ) -> bool:
        return bool(self._engine.DisplayWorkspaceBrowserDialog(dlg_title, int(dlg_options)))

    @ts_interface
    def do_dot_net_garbage_collection(self, reserved: int = 0) -> typing.Any:
        self._engine.DoDotNetGarbageCollection(int(reserved))

    @property
    @ts_interface
    def dot_net_clr_version(self) -> str:
        return str(self._engine.DotNetCLRVersion)

    @property
    def dot_net_runtime_kind(self) -> typing.Any:
        from py_teststand.adapters.dotnet import (
            DotNetRuntimeKind,
            parse_dotnet_runtime_kind,
        )

        try:
            return parse_dotnet_runtime_kind(self.dot_net_clr_version)
        except Exception:
            return DotNetRuntimeKind.Unknown

    @property
    def gac_supported(self) -> bool:
        from py_teststand.adapters.dotnet import DotNetRuntimeKind

        return self.dot_net_runtime_kind == DotNetRuntimeKind.Framework

    @property
    @ts_interface
    def dot_net_garbage_collection_interval(self) -> typing.Any:
        return int(self._engine.DotNetGarbageCollectionInterval)

    @dot_net_garbage_collection_interval.setter
    @ts_interface
    def dot_net_garbage_collection_interval(self, value: int) -> None:
        self._engine.DotNetGarbageCollectionInterval = int(value)

    @property
    @ts_interface
    def enable_remote(self) -> bool:
        return bool(self._engine.EnableRemote)

    @enable_remote.setter
    @ts_interface
    def enable_remote(self, value: bool) -> None:
        self._engine.EnableRemote = bool(value)

    @property
    @ts_interface
    def enable_user_privilege_checking(self) -> bool:
        return bool(self._engine.EnableUserPrivilegeChecking)

    @enable_user_privilege_checking.setter
    @ts_interface
    def enable_user_privilege_checking(self, value: bool) -> None:
        self._engine.EnableUserPrivilegeChecking = bool(value)

    @ts_interface
    def end_profiling(self) -> None:
        self._engine.EndProfiling()

    @functools.cached_property
    @ts_interface
    def engine_version_string(self) -> str:
        return str(self._engine.EngineVersionString)

    @ts_interface
    def eval_tool_menu_item_exprs(self, edit_args: typing.Any | None = None) -> typing.Any:
        self._engine.EvalToolMenuItemExprs(edit_args)

    @property
    @ts_interface
    def execution_mask(self) -> ExecutionMask | int:
        return int(self._engine.ExecutionMask)

    @execution_mask.setter
    @ts_interface
    def execution_mask(self, value: ExecutionMask | int) -> None:
        self._engine.ExecutionMask = int(value)

    @ts_interface
    def expand_path_macros(self, path_string: str) -> typing.Any:
        path_io = path_string
        result = self._engine.ExpandPathMacros(path_io)
        return bool(result), str(path_io)

    @property
    @ts_interface
    def external_report_viewers(self) -> ExternalReportViewers:
        from py_teststand.core.external_report_viewers import ExternalReportViewers

        return ExternalReportViewers(self._engine.ExternalReportViewers, self)

    @property
    @ts_interface
    def file_dialog_dir_history_list(self) -> list[str]:
        return list(self._engine.FileDialogDirHistoryList)

    @file_dialog_dir_history_list.setter
    @ts_interface
    def file_dialog_dir_history_list(self, value: list[str]) -> None:
        self._engine.FileDialogDirHistoryList = value

    @ts_interface
    def find_file(
        self,
        file_to_find: str,
        prompt_option: FindFilePromptOption | int = FindFilePromptOption.HonorUserPreference,
        search_list_option: FindFileSearchListOption | int = FindFileSearchListOption.Ask,
        is_command: bool = False,
        current_sequence_file: SequenceFile | None = None,
    ) -> tuple[bool, str, bool]:
        abs_path_out = ""
        cancelled_out = False
        seq_com = current_sequence_file._com_obj if current_sequence_file else None
        result = self._engine.FindFile(
            file_to_find,
            abs_path_out,
            cancelled_out,
            int(prompt_option),
            int(search_list_option),
            bool(is_command),
            seq_com,
        )
        return bool(result), str(abs_path_out), bool(cancelled_out)

    @ts_interface
    def find_file_ex(
        self,
        file_to_find: str,
        prompt_option: FindFilePromptOption | int = FindFilePromptOption.HonorUserPreference,
        search_list_option: FindFileSearchListOption | int = FindFileSearchListOption.Ask,
        is_command: bool = False,
        search_context: SequenceFile | None = None,
        reserved: typing.Any | None = None,
    ) -> tuple[bool, str, SearchDirectory, int, bool]:
        abs_path_out = ""
        type_out = 0
        index_out = 0
        cancelled_out = False
        ctx_com = search_context._com_obj if search_context else None
        result = self._engine.FindFileEx(
            file_to_find,
            abs_path_out,
            type_out,
            index_out,
            cancelled_out,
            int(prompt_option),
            int(search_list_option),
            bool(is_command),
            ctx_com,
            reserved,
        )
        return (
            bool(result),
            str(abs_path_out),
            SearchDirectory(type_out),
            int(index_out),
            bool(cancelled_out),
        )

    @ts_interface
    def find_path(
        self,
        path_to_find: str,
        current_sequence_file: SequenceFile | None = None,
    ) -> tuple[bool, str, FindPathStatusOption]:
        abs_path_out = ""
        status_out = 0
        seq_com = current_sequence_file._com_obj if current_sequence_file else None
        result = self._engine.FindPath(path_to_find, abs_path_out, status_out, seq_com)
        return bool(result), str(abs_path_out), FindPathStatusOption(status_out)

    @ts_interface
    def get_adapter(self, adapter_index: int) -> typing.Any:
        return Adapter(self._engine.GetAdapter(int(adapter_index)), self)

    @ts_interface
    def get_adapter_by_key_name(self, adapter_key_name: str | AdapterKeyName) -> typing.Any:
        return Adapter(self._engine.GetAdapterByKeyName(str(adapter_key_name)), self)

    @ts_interface
    def get_edit_time_tool_menu_items(self, reserved: int = 0) -> typing.Any:
        from py_teststand.ui.menu_item import EditTimeMenuItems

        return EditTimeMenuItems(self._engine.GetEditTimeToolMenuItems(int(reserved)), self)

    @ts_interface
    def get_engine_config_file(
        self, config_file_type: PropertyObjectFileType | int
    ) -> PropertyObjectFile:
        return PropertyObjectFile(
            self._get_com_prop("GetEngineConfigFile", int(config_file_type)), self
        )

    @ts_interface
    def get_environment_path(self) -> typing.Any:
        return str(self._engine.GetEnvironmentPath())

    @ts_interface
    def get_remote_executor_interface(self, adapter_index: int) -> typing.Any:
        return self._engine.GetRemoteExecutorInterface(int(adapter_index))

    @ts_interface
    def get_error_string(self, error_code: TSError | int) -> typing.Any:
        error_string_out = ""
        result = self._engine.GetErrorString(int(error_code), error_string_out)
        return bool(result), str(error_string_out)

    @ts_interface
    def get_execution(self, execution_id: int) -> typing.Any:
        com_obj = self._engine.GetExecution(int(execution_id))
        return Execution(com_obj, self) if com_obj else None

    @ts_interface
    def get_file_information(self, path: str) -> typing.Any:
        from py_teststand.core.file_information import FileInformation

        return FileInformation(self._engine.GetFileInformation(path), self)

    @ts_interface
    def get_image_index(self, image_name: str) -> typing.Any:
        return int(self._engine.GetImageIndex(image_name))

    @ts_interface
    def get_image_name(self, image_index: int) -> typing.Any:
        return str(self._engine.GetImageName(int(image_index)))

    @ts_interface
    def get_insert_step_menu_structure(
        self,
        selected_file: PropertyObjectFile | None,
        hidden_flags: PropertyFlag | int = 0,
    ) -> PropertyObject:
        file_com = selected_file._com_obj if selected_file else None
        return PropertyObject(
            self._engine.GetInsertStepMenuStructure(file_com, int(hidden_flags)), self
        )

    @ts_interface
    def get_insert_variable_menu_structure(
        self,
        selected_file: PropertyObjectFile | None,
        hidden_flags: PropertyFlag | int = 0,
    ) -> PropertyObject:
        file_com = selected_file._com_obj if selected_file else None
        return PropertyObject(
            self._engine.GetInsertVariableMenuStructure(file_com, int(hidden_flags)), self
        )

    @ts_interface
    def get_internal_option(self, option: InternalOption | int) -> typing.Any:
        return self._engine.GetInternalOption(int(option))

    @ts_interface
    def get_license_description(self, reserved: int = 0) -> typing.Any:
        return str(self._engine.GetLicenseDescription(int(reserved)))

    @ts_interface
    def get_localized_decimal_point(
        self, decimal_point_option: DecimalPointLocalizationOption | int
    ) -> str:
        return str(self._engine.GetLocalizedDecimalPoint(int(decimal_point_option)))

    @ts_interface
    def get_location_for_next_dialog(
        self, clear_loc: bool = True
    ) -> tuple[str, SearchElement, int, int]:
        lookup_out = ""
        element_out = 0
        start_out = 0
        length_out = 0
        self._engine.GetLocationForNextDialog(
            lookup_out, element_out, start_out, length_out, bool(clear_loc)
        )
        return str(lookup_out), SearchElement(element_out), int(start_out), int(length_out)

    @ts_interface
    def get_module_profiling(self, adapter_key_name: str | AdapterKeyName) -> typing.Any:
        return bool(self._engine.GetModuleProfiling(str(adapter_key_name)))

    @ts_interface
    def get_num_tool_menu_items(self, menu_index: int) -> typing.Any:
        return int(self._engine.GetNumToolMenuItems(int(menu_index)))

    @ts_interface
    def get_num_tool_menus(self) -> int:
        return int(self._engine.GetNumToolMenus())

    @ts_interface
    def get_output_messages(self) -> OutputMessages:
        from py_teststand.messaging.output_messages import OutputMessages

        return OutputMessages(self._engine.GetOutputMessages(), self)

    @ts_interface
    def get_product_registration_info(self) -> typing.Any:
        user_out = ""
        company_out = ""
        serial_out = ""
        result = self._engine.GetProductRegistrationInfo(user_out, company_out, serial_out)
        return bool(result), str(user_out), str(company_out), str(serial_out)

    @ts_interface
    def get_relative_path_from_absolute_path(
        self,
        absolute_path: str,
        search_context: SequenceFile | None = None,
    ) -> tuple[bool, str, str]:
        relative_path_out = ""
        search_dir_out = ""
        ctx_com = search_context._com_obj if search_context else None
        result = self._engine.GetRelativePathFromAbsolutePath(
            absolute_path, ctx_com, relative_path_out, search_dir_out
        )
        return bool(result), str(relative_path_out), str(search_dir_out)

    @ts_interface
    def get_resource_string(
        self,
        section: str,
        symbol: str,
        default_string: str | None = None,
    ) -> tuple[str, bool]:
        found_out = False
        result = self._engine.GetResourceString(section, symbol, default_string, found_out)
        return str(result), bool(found_out)

    @ts_interface
    def get_resource_symbols(self, section: str) -> typing.Any:
        return list(self._engine.GetResourceSymbols(section))

    @ts_interface
    def get_run_time_tool_menu_items(
        self,
        edit_args: typing.Any | None = None,
        reserved: int = 0,
    ) -> RunTimeMenuItems:
        from py_teststand.ui.menu_item import RunTimeMenuItems

        return RunTimeMenuItems(
            self._engine.GetRunTimeToolMenuItems(edit_args, int(reserved)), self
        )

    @ts_interface
    def get_sequence_file(
        self,
        seq_file_path: str,
        get_seq_file_flags: GetSeqFileOption | int = GetSeqFileOption.OperatorInterfaceFlags,
    ) -> SequenceFile:
        return SequenceFile(
            self._engine.GetSequenceFile(seq_file_path, int(get_seq_file_flags)), self
        )

    @ts_interface
    def get_sequence_file_ex(
        self,
        seq_file_path: str,
        get_seq_file_flags: GetSeqFileOption | int = GetSeqFileOption.OperatorInterfaceFlags,
        handler_type: ConflictHandler | int = ConflictHandler.Error,
    ) -> SequenceFile:
        return SequenceFile(
            self._engine.GetSequenceFileEx(
                seq_file_path, int(get_seq_file_flags), int(handler_type)
            ),
            self,
        )

    @ts_interface
    def get_station_model_sequence_file(self) -> typing.Any:
        model_desc_out = ""
        result_com = self._engine.GetStationModelSequenceFile(model_desc_out)
        return SequenceFile(result_com, self), str(model_desc_out)

    @ts_interface
    def get_sync_manager(self, sync_object_name: str) -> typing.Any:
        return self._engine.GetSyncManager(sync_object_name)

    @ts_interface
    def get_templates_file(self, options: GetTemplatesFileOption | int = 0) -> typing.Any:
        return PropertyObjectFile(self._engine.GetTemplatesFile(int(options)), self)

    @ts_interface
    def get_test_stand_path(self, test_stand_path: TestStandPath | int) -> typing.Any:
        return str(self._engine.GetTestStandPath(int(test_stand_path)))

    @ts_interface
    def get_tool_menu_item_info(
        self, menu_index: int, item_index: int
    ) -> tuple[str, int, bool, int]:
        item_text_out = ""
        sub_menu_index_out = 0
        enabled_out = False
        unique_id_out = 0
        self._engine.GetToolMenuItemInfo(
            int(menu_index),
            int(item_index),
            item_text_out,
            sub_menu_index_out,
            enabled_out,
            unique_id_out,
        )
        return str(item_text_out), int(sub_menu_index_out), bool(enabled_out), int(unique_id_out)

    @ts_interface
    def get_tool_menu_item_info_ex(
        self, menu_index: int, item_index: int
    ) -> tuple[str, int, ToolMenuItemAttribute, int]:
        item_text_out = ""
        sub_menu_index_out = 0
        item_attributes_out = 0
        unique_id_out = 0
        self._engine.GetToolMenuItemInfoEx(
            int(menu_index),
            int(item_index),
            item_text_out,
            sub_menu_index_out,
            item_attributes_out,
            unique_id_out,
        )
        return (
            str(item_text_out),
            int(sub_menu_index_out),
            ToolMenuItemAttribute(item_attributes_out),
            int(unique_id_out),
        )

    @ts_interface
    def get_tool_menu_item_info_with_id(self, unique_item_id: int) -> typing.Any:
        item_text_out = ""
        sub_menu_index_out = 0
        enabled_out = False
        self._engine.GetToolMenuItemInfoWithID(
            int(unique_item_id), item_text_out, sub_menu_index_out, enabled_out
        )
        return str(item_text_out), int(sub_menu_index_out), bool(enabled_out)

    @ts_interface
    def get_tool_menu_item_info_with_id_ex(
        self, unique_item_id: int
    ) -> tuple[str, int, ToolMenuItemAttribute]:
        item_text_out = ""
        sub_menu_index_out = 0
        item_attributes_out = 0
        self._engine.GetToolMenuItemInfoWithIDEx(
            int(unique_item_id), item_text_out, sub_menu_index_out, item_attributes_out
        )
        return (
            str(item_text_out),
            int(sub_menu_index_out),
            ToolMenuItemAttribute(item_attributes_out),
        )

    @ts_interface
    def get_tool_menu_structure(self) -> PropertyObject:
        return PropertyObject(self._engine.GetToolMenuStructure(), self)

    @ts_interface
    def get_type_definition(self, type_name: str) -> typing.Any:
        com_obj = self._engine.GetTypeDefinition(type_name)
        return PropertyObject(com_obj, self) if com_obj else None

    @ts_interface
    def get_type_names(self) -> list[str]:
        return list(self._engine.GetTypeNames())

    @ts_interface
    def get_type_palette_file_list(self) -> list[PropertyObjectFile]:
        return [PropertyObjectFile(f, self) for f in self._engine.GetTypePaletteFileList()]

    @ts_interface
    def get_types(self, reserved: int = 0) -> typing.Any:
        from py_teststand.property.property_object_file import TypeUsageList

        return TypeUsageList(self._engine.GetTypes(int(reserved)), self)

    @ts_interface
    def get_type_usage_locations(self, type_name: str) -> typing.Any:
        return [PropertyObjectFile(f, self) for f in self._engine.GetTypeUsageLocations(type_name)]

    @ts_interface
    def get_ui_message(self) -> typing.Any:
        return UIMessage(self._engine.GetUIMessage(), self)

    @ts_interface
    def get_user(self, login_name: str) -> typing.Any:
        com_obj = self._engine.GetUser(login_name)
        return User(com_obj, self) if com_obj else None

    @ts_interface
    def get_user_group(self, user_group_name: str) -> typing.Any:
        com_obj = self._engine.GetUserGroup(user_group_name)
        return User(com_obj, self) if com_obj else None

    @ts_interface
    def get_user_profile(self, user_profile_name: str) -> typing.Any:
        com_obj = self._engine.GetUserProfile(user_profile_name)
        return User(com_obj, self) if com_obj else None

    @ts_interface
    def get_watch_expressions(
        self,
        client_sequence_file: SequenceFile | None = None,
        scoping_seq_context: SequenceContext | None = None,
        filter_options: WatchExpressionFilterOption | int = WatchExpressionFilterOption.NoneValue,
    ) -> WatchExpressions:
        file_com = client_sequence_file._com_obj if client_sequence_file else None

        context_com = scoping_seq_context._com_obj if scoping_seq_context else None
        from py_teststand.execution.watch_expression import WatchExpressions

        return WatchExpressions(
            self._engine.GetWatchExpressions(file_com, context_com, int(filter_options)),
            self,
        )

    @ts_interface
    def get_watch_expressions_change_count(self) -> int:
        return int(self._engine.GetWatchExpressionsChangeCount())

    @property
    @ts_interface
    def globals(self) -> PropertyObject:
        return PropertyObject(self._engine.Globals, self)

    @property
    @ts_interface
    def globals_file(self) -> PropertyObjectFile:
        return PropertyObjectFile(self._engine.GlobalsFile, self)

    @ts_interface
    def has_addon_license(self, addon_feature_name: str) -> typing.Any:
        return bool(self._engine.HasAddonLicense(addon_feature_name))

    @property
    @ts_interface
    def images(self) -> Images:
        from py_teststand.core.images import Images

        return Images(self._engine.Images, self)

    @ts_interface
    def invoke_tool_menu_item(self, menu_index: int, item_index: int) -> typing.Any:
        self._engine.InvokeToolMenuItem(int(menu_index), int(item_index))

    @ts_interface
    def invoke_tool_menu_item_with_id(self, unique_item_id: int) -> typing.Any:
        self._engine.InvokeToolMenuItemWithID(int(unique_item_id))

    @property
    @ts_interface
    def is_64bit(self) -> bool:
        return bool(self._com_obj.Is64Bit)

    @property
    @ts_interface
    def test_stand_directory(self) -> str:
        return str(self._com_obj.TestStandDirectory)

    @property
    @ts_interface
    def always_goto_cleanup_on_failure(self) -> bool:
        return bool(self._com_obj.AlwaysGotoCleanupOnFailure)

    @always_goto_cleanup_on_failure.setter
    @ts_interface
    def always_goto_cleanup_on_failure(self, value: bool) -> None:
        self._com_obj.AlwaysGotoCleanupOnFailure = value

    @ts_interface
    def is_current_sequence_file_version(self, file_path: str) -> typing.Any:
        return int(self._engine.IsCurrentSequenceFileVersion(file_path))

    @property
    @ts_interface
    def is_remote(self) -> bool:
        return bool(self._engine.IsRemote)

    @property
    @ts_interface
    def is_ui_message_queue_empty(self) -> bool:
        return bool(self._engine.IsUIMessageQueueEmpty)

    @property
    @ts_interface
    def large_image_list(self) -> int:
        return int(self._engine.LargeImageList)

    @property
    @ts_interface
    def large_image_list_ex(self) -> typing.Any:
        return self._engine.LargeImageListEx

    @property
    @ts_interface
    def last_workspace_path(self) -> str:
        return str(self._engine.LastWorkspacePath)

    @ts_interface
    def launch_external_viewer(self, file_path: str) -> typing.Any:
        self._engine.LaunchExternalViewer(file_path)

    @property
    @ts_interface
    def license_type(self) -> typing.Any:
        return LicenseType(self._engine.LicenseType)

    @ts_interface
    def load_type_palette_files(self) -> None:
        self._engine.LoadTypePaletteFiles()

    @ts_interface
    def load_type_palette_files_ex(
        self,
        handler_type: ConflictHandler | int = ConflictHandler.Prompt,
        options: int = 0,
    ) -> None:
        self._engine.LoadTypePaletteFilesEx(int(handler_type), int(options))

    @ts_interface
    def localize_expression(
        self,
        expression_string: str,
        decimal_point_option: DecimalPointLocalizationOption | int,
    ) -> str:
        return str(self._engine.LocalizeExpression(expression_string, int(decimal_point_option)))

    @ts_interface
    def log_profiler_action(
        self,
        profiler_mechanism: str,
        adapter_key_name: str,
        sequence_context: SequenceContext | None,
        thread_id: str,
        thread_display_name: str,
        name: str,
        synchronization_state: ProfilerState | int,
        operation: str,
        timeout: float,
        post_message: bool,
        reserved: typing.Any | None = None,
    ) -> OutputMessage:
        ctx_com = sequence_context._com_obj if sequence_context else None
        from py_teststand.messaging.output_message import OutputMessage

        return OutputMessage(
            self._engine.LogProfilerAction(
                profiler_mechanism,
                adapter_key_name,
                ctx_com,
                thread_id,
                thread_display_name,
                name,
                int(synchronization_state),
                operation,
                float(timeout),
                bool(post_message),
                reserved,
            ),
            self,
        )

    @property
    @ts_interface
    def major_version(self) -> int:
        return int(self._engine.MajorVersion)

    @property
    @ts_interface
    def master_engine(self) -> Engine:
        return Engine(self._engine.MasterEngine)

    @ts_interface
    def set_master_engine(self, master: Engine) -> None:
        master_com = master._engine if master is not None else None
        self._engine.SetMasterEngine(master_com)

    @property
    @ts_interface
    def minor_version(self) -> int:
        return int(self._engine.MinorVersion)

    @ts_interface
    def new_csv_file_input_record_stream(self, absolute_path: str) -> typing.Any:
        return self._engine.NewCsvFileInputRecordStream(absolute_path)

    @ts_interface
    def new_csv_file_output_record_stream(
        self,
        absolute_path: str,
        open_mode: FileOpenMode | int,
    ) -> CSVFileOutputRecordStream:
        from py_teststand.execution.output_record_stream import CSVFileOutputRecordStream

        return CSVFileOutputRecordStream(
            self._engine.NewCsvFileOutputRecordStream(absolute_path, int(open_mode)),
            self,
        )

    @ts_interface
    def new_data_type(
        self,
        value_type: PropValType | int,
        as_array: bool,
        type_name_param: str,
        options: PropertyOption | int,
    ) -> PropertyObject:
        return PropertyObject(
            self._engine.NewDataType(
                int(value_type), bool(as_array), type_name_param, int(options)
            ),
            self,
        )

    @ts_interface
    def new_edit_args(self) -> EditArgs:
        from py_teststand.execution.edit_args import EditArgs

        return EditArgs(self._engine.NewEditArgs(), self)

    @ts_interface
    def new_edit_context(
        self,
        obj: PropertyObject,
        edit_args_param: EditArgs | typing.Any | None = None,
        location_string: str | None = None,
    ) -> SequenceContext:
        args_com = (
            edit_args_param._com_obj if hasattr(edit_args_param, "_com_obj") else edit_args_param
        )

        return SequenceContext(
            self._engine.NewEditContext(obj._com_obj, args_com, location_string), self
        )

    @ts_interface
    def new_evaluation_types(
        self,
        initial_property_value_type_flags: int = -1,
    ) -> EvaluationTypes:
        from py_teststand.sequence.expression import EvaluationTypes

        return EvaluationTypes(
            self._engine.NewEvaluationTypes(int(initial_property_value_type_flags)), self
        )

    @ts_interface
    def new_execution(
        self,
        sequence_file: SequenceFile,
        sequence_name: str,
        process_model: PropertyObject | None = None,
        break_at_first: bool = False,
        exec_type_mask: int = 0,
        sequence_args: PropertyObject | None = None,
        edit_args: EditArgs | None = None,
        interactive_args: InteractiveArgs | None = None,
    ) -> Execution:
        import pythoncom

        model_com = process_model._com_obj if process_model else None
        args_com = sequence_args._com_obj if sequence_args else pythoncom.Missing
        edit_com = edit_args._com_obj if edit_args else pythoncom.Missing
        inter_com = interactive_args._com_obj if interactive_args else pythoncom.Missing
        return Execution(
            self._engine.NewExecution(
                sequence_file._com_obj,
                sequence_name,
                model_com,
                bool(break_at_first),
                int(exec_type_mask),
                args_com,
                edit_com,
                inter_com,
            ),
            self,
        )

    @ts_interface
    def new_expression(self) -> Expression:
        return Expression(self._engine.NewExpression(), self)

    @ts_interface
    def new_hierarchical_execution(
        self,
        sequence_call_steps: list[Step],
        hierarchical_execution_flags: HierarchicalExecutionFlag | int,
        sequence_file_param: SequenceFile,
        sequence_name_param: str,
        process_model_param: SequenceFile | None,
        break_at_first_step: bool,
        execution_type_mask_param: ExecutionTypeMask | int,
        sequence_args_param: PropertyObject | None = None,
        edit_args_param: EditArgs | None = None,
        interactive_args_param: InteractiveArgs | None = None,
    ) -> Execution:
        steps_com = [s._com_obj for s in sequence_call_steps]
        model_com = process_model_param._com_obj if process_model_param else None
        args_com = sequence_args_param._com_obj if sequence_args_param else None
        edit_com = edit_args_param._com_obj if edit_args_param else None
        inter_com = interactive_args_param._com_obj if interactive_args_param else None
        return Execution(
            self._engine.NewHierarchicalExecution(
                steps_com,
                int(hierarchical_execution_flags),
                sequence_file_param._com_obj,
                sequence_name_param,
                model_com,
                bool(break_at_first_step),
                int(execution_type_mask_param),
                args_com,
                edit_com,
                inter_com,
            ),
            self,
        )

    @ts_interface
    def new_interactive_args(self) -> InteractiveArgs:
        from py_teststand.execution.interactive_args import InteractiveArgs

        return InteractiveArgs(self._engine.NewInteractiveArgs(), self)

    @ts_interface
    def new_locations(self) -> Locations:
        from py_teststand.sequence.location import Locations

        return Locations(self._engine.NewLocations(), self)

    @ts_interface
    def new_output_message(
        self,
        message_text: str,
        category_text: str = "",
        severity: OutputMessageSeverityType | int = OutputMessageSeverityType.Information,
        sequence_context: SequenceContext | None = None,
    ) -> OutputMessage:
        ctx_com = sequence_context._com_obj if sequence_context else None
        from py_teststand.messaging.output_message import OutputMessage

        return OutputMessage(
            self._engine.NewOutputMessage(message_text, category_text, int(severity), ctx_com),
            self,
        )

    @ts_interface
    def new_output_messages(self) -> OutputMessages:
        from py_teststand.messaging.output_messages import OutputMessages

        return OutputMessages(self._engine.NewOutputMessages(), self)

    @ts_interface
    def new_property_object(
        self,
        value_type: PropValType | int,
        as_array: bool,
        type_name_param: str,
        options: PropertyOption | int,
    ) -> PropertyObject:
        return PropertyObject(
            self._engine.NewPropertyObject(
                int(value_type), bool(as_array), type_name_param, int(options)
            ),
            self,
        )

    @ts_interface
    def new_property_object_file(
        self,
        file_type: PropertyObjectFileType | int,
    ) -> PropertyObjectFile:
        return PropertyObjectFile(self._engine.NewPropertyObjectFile(int(file_type)), self)

    @ts_interface
    def new_property_object_type(
        self,
        value_type: PropValType | int,
        type_name: str = "",
        element_type: PropertyObjectType | None = None,
        is_object: bool = True,
    ) -> PropertyObjectType:
        elem_com = element_type._com_obj if element_type else None
        from py_teststand.property.data_type import PropertyObjectType

        return PropertyObjectType(
            self._engine.NewPropertyObjectType(
                int(value_type), type_name, elem_com, bool(is_object)
            ),
            self,
        )

    @ts_interface
    def new_result_log(self) -> ResultLog:
        from py_teststand.execution.result_log import ResultLog

        return ResultLog(self._engine.NewResultLog(), self)

    @ts_interface
    def new_result_logger(self) -> ResultLogger:
        from py_teststand.execution.result_log import ResultLogger

        return ResultLogger(self._engine.NewResultLogger(), self)

    @ts_interface
    def new_sequence(self) -> Sequence:
        from py_teststand.sequence.sequence import Sequence

        return Sequence(self._engine.NewSequence(), self)

    @ts_interface
    def new_sequence_file(self) -> SequenceFile:
        from py_teststand.sequence.sequence_file import SequenceFile

        return SequenceFile(self._engine.NewSequenceFile(), self)

    @ts_interface
    def diff_sequence_files(
        self,
        sequence_file_1: SequenceFile,
        sequence_file_2: SequenceFile,
        options: int = 0,
    ) -> typing.Any:
        return self._engine.DiffSequenceFiles(
            sequence_file_1._com_obj, sequence_file_2._com_obj, int(options)
        )

    @ts_interface
    def new_step(self, adapter_key_name: str, step_type_name: str) -> typing.Any:
        return Step(self._engine.NewStep(adapter_key_name, step_type_name), self)

    @ts_interface
    def new_step_type(self) -> StepType:
        return StepType(self._engine.NewStepType(), self)

    @ts_interface
    def new_type_usage_list(self, reserved_param: int = 0) -> typing.Any:
        from py_teststand.property.property_object_file import TypeUsageList

        return TypeUsageList(self._engine.NewTypeUsageList(int(reserved_param)), self)

    @ts_interface
    def new_undo_item_creator(
        self,
        kind_param: EditKind | int,
        edited_file_param: PropertyObjectFile,
        edit_description: str = "",
    ) -> UndoItemCreator:
        return UndoItemCreator(
            self._engine.NewUndoItemCreator(
                int(kind_param), edited_file_param._com_obj, edit_description
            ),
            self,
        )

    @ts_interface
    def new_undo_stack(self) -> UndoStack:
        return UndoStack(self._engine.NewUndoStack(), self)

    @ts_interface
    def new_user(self, user_profile: User | None = None) -> typing.Any:
        profile_com = user_profile._com_obj if user_profile else None
        return User(self._engine.NewUser(profile_com), self)

    @ts_interface
    def new_workspace_file(self) -> WorkspaceFile:
        return WorkspaceFile(self._engine.NewWorkspaceFile(), self)

    @ts_interface
    def notify_end_of_modal_dialog(self, modal_id: int) -> typing.Any:
        self._engine.NotifyEndOfModalDialog(int(modal_id))

    @ts_interface
    def notify_start_of_modal_dialog(self) -> int:
        return int(self._engine.NotifyStartOfModalDialog())

    @ts_interface
    def notify_start_of_modal_dialog_ex(
        self,
        sequence_context: SequenceContext | None,
    ) -> tuple[int, bool]:
        ctx_com = sequence_context._com_obj if sequence_context else None
        return self._engine.NotifyStartOfModalDialogEx(ctx_com)

    @property
    @ts_interface
    def num_adapters(self) -> int:
        return int(self._engine.NumAdapters)

    @property
    @ts_interface
    def num_images(self) -> int:
        return int(self._engine.NumImages)

    @ts_interface
    def open_workspace_file(
        self,
        workspace_file_path: str,
        options: OpenWorkspaceFileOption | int = OpenWorkspaceFileOption.NoneValue,
        handler_type: ConflictHandler | int = ConflictHandler.Error,
    ) -> WorkspaceFile:
        return WorkspaceFile(
            self._engine.OpenWorkspaceFile(workspace_file_path, int(options), int(handler_type)),
            self,
        )

    @property
    @ts_interface
    def output_messages_enabled(self) -> bool:
        return bool(self._engine.OutputMessagesEnabled)

    @output_messages_enabled.setter
    @ts_interface
    def output_messages_enabled(self, value: bool) -> None:
        self._engine.OutputMessagesEnabled = bool(value)

    @ts_interface
    def parse_lookup_string(
        self,
        lookup_string: str,
        options: ParseLookupStringOption | int = 0,
    ) -> list[str]:
        return list(self._engine.ParseLookupString(lookup_string, int(options)))

    @property
    @ts_interface
    def patch_version(self) -> int:
        return int(self._engine.PatchVersion)

    @property
    @ts_interface
    def persist_breakpoints(self) -> bool:
        return bool(self._engine.PersistBreakpoints)

    @persist_breakpoints.setter
    @ts_interface
    def persist_breakpoints(self, value: bool) -> None:
        self._engine.PersistBreakpoints = bool(value)

    @property
    @ts_interface
    def persist_config_file(self) -> bool:
        return bool(self._engine.PersistConfigFile)

    @persist_config_file.setter
    @ts_interface
    def persist_config_file(self, value: bool) -> None:
        self._engine.PersistConfigFile = bool(value)

    @property
    @ts_interface
    def persist_watch_expressions(self) -> bool:
        return bool(self._engine.PersistWatchExpressions)

    @persist_watch_expressions.setter
    @ts_interface
    def persist_watch_expressions(self, value: bool) -> None:
        self._engine.PersistWatchExpressions = bool(value)

    @ts_interface
    def post_ui_message(
        self,
        execution: Execution,
        thread_param: Thread,
        event_code: UIMessageCode | int,
        numeric_data: float,
        string_data: str,
        active_x_data: typing.Any | None,
        synchronous: bool,
    ) -> None:
        self._engine.PostUIMessage(
            execution._com_obj,
            thread_param._com_obj,
            int(event_code),
            float(numeric_data),
            string_data,
            active_x_data,
            bool(synchronous),
        )

    @property
    @ts_interface
    def profiler_input_output_capture_maximum_text_length(self) -> int:
        return int(self._engine.ProfilerInputOutputCaptureMaximumTextLength)

    @profiler_input_output_capture_maximum_text_length.setter
    @ts_interface
    def profiler_input_output_capture_maximum_text_length(self, value: int) -> None:
        self._engine.ProfilerInputOutputCaptureMaximumTextLength = int(value)

    @property
    @ts_interface
    def profiler_options(self) -> ProfilerOption | int:
        return ProfilerOption(self._engine.ProfilerOption)

    @profiler_options.setter
    @ts_interface
    def profiler_options(self, value: ProfilerOption | int) -> None:
        self._engine.ProfilerOption = int(value)

    @property
    @ts_interface
    def profiler_output_message_category_name(self) -> str:
        return str(self._engine.ProfilerOutputMessageCategoryName)

    @property
    @ts_interface
    def profiling_enabled(self) -> bool:
        return bool(self._engine.ProfilingEnabled)

    @property
    @ts_interface
    def prompt_when_adding_files_to_sc(self) -> bool:
        return bool(self._engine.PromptWhenAddingFilesToSC)

    @prompt_when_adding_files_to_sc.setter
    @ts_interface
    def prompt_when_adding_files_to_sc(self, value: bool) -> None:
        self._engine.PromptWhenAddingFilesToSC = bool(value)

    @ts_interface
    def read_property_object_file(
        self,
        path: str,
        handler_type: ConflictHandler | int = ConflictHandler.Error,
        options: ReadPropertyObjectFileOption | int = 0,
    ) -> tuple[PropertyObjectFile, bool]:
        obj_com, cancelled = self._engine.ReadPropertyObjectFile(
            path, int(handler_type), int(options)
        )
        return PropertyObjectFile(obj_com, self), bool(cancelled)

    @ts_interface
    def register_modal_window(
        self,
        sequence_context: SequenceContext | None,
        modal_hwnd: int,
    ) -> tuple[int, bool]:
        ctx_com = sequence_context._com_obj if sequence_context else None
        return self._engine.RegisterModalWindow(ctx_com, int(modal_hwnd))

    @ts_interface
    def register_sequence_to_execute_on_crash(
        self,
        seq_file_path: str,
        seq_name: str,
        options: CrashCallbackOption | int = 0,
        reserved: typing.Any = None,
    ) -> int:
        return int(
            self._engine.RegisterSequenceToExecuteOnCrash(
                seq_file_path, seq_name, int(options), reserved
            )
        )

    @ts_interface
    def register_ui_message(self, message_name: str) -> typing.Any:
        return int(self._engine.RegisterUIMessage(message_name))

    @ts_interface
    def register_ui_message_callback(self, callback_func_addr: int) -> typing.Any:
        self._engine.RegisterUIMessageCallback(int(callback_func_addr))

    @ts_interface
    def register_ui_message_callback_ex(self, callback_func_addr: int) -> typing.Any:
        self._engine.RegisterUIMessageCallbackEx(int(callback_func_addr))

    @ts_interface
    def release_license(self, license_handle: int, reserved: int = 0) -> typing.Any:
        self._engine.ReleaseLicense(int(license_handle), int(reserved))

    @ts_interface
    def release_sequence_file(self, sequence_file: SequenceFile) -> typing.Any:
        self._engine.ReleaseSequenceFile(sequence_file._com_obj)

    @ts_interface
    def release_sequence_file_ex(
        self,
        sequence_file: SequenceFile,
        options: ReleaseSeqFileOption | int = 0,
    ) -> bool:
        return bool(self._engine.ReleaseSequenceFileEx(sequence_file._com_obj, int(options)))

    @property
    @ts_interface
    def reload_docs_when_opening_workspace(self) -> bool:
        return bool(self._engine.ReloadDocsWhenOpeningWorkspace)

    @reload_docs_when_opening_workspace.setter
    @ts_interface
    def reload_docs_when_opening_workspace(self, value: bool) -> None:
        self._engine.ReloadDocsWhenOpeningWorkspace = bool(value)

    @ts_interface
    def reload_globals(self) -> None:
        self._engine.ReloadGlobals()

    @ts_interface
    def reload_string_resource_files(self) -> None:
        self._engine.ReloadStringResourceFiles()

    @property
    @ts_interface
    def reload_workspace_at_startup(self) -> bool:
        return bool(self._engine.ReloadWorkspaceAtStartup)

    @reload_workspace_at_startup.setter
    @ts_interface
    def reload_workspace_at_startup(self, value: bool) -> None:
        self._engine.ReloadWorkspaceAtStartup = bool(value)

    @property
    @ts_interface
    def require_user_login(self) -> bool:
        return bool(self._engine.RequireUserLogin)

    @require_user_login.setter
    @ts_interface
    def require_user_login(self, value: bool) -> None:
        self._engine.RequireUserLogin = bool(value)

    @ts_interface
    def reset_type_instances(
        self,
        type_param: PropertyObject,
        options: ResetTypeInstanceOption | int = ResetTypeInstanceOption.ResetFlags
        | ResetTypeInstanceOption.ResetValues,
    ) -> bool:
        return bool(self._engine.ResetTypeInstances(type_param._com_obj, int(options)))

    @property
    @ts_interface
    def revision_version(self) -> int:
        return int(self._engine.RevisionVersion)

    @property
    @ts_interface
    def rte_option(self) -> RTEOption:
        return RTEOption(self._engine.RTEOption)

    @rte_option.setter
    @ts_interface
    def rte_option(self, value: RTEOption | int) -> None:
        self._engine.RTEOption = int(value)

    @ts_interface
    def save_all_modified_seq_files(
        self,
        options: SaveAllSeqFileOption | int = 0,
    ) -> bool:
        return bool(self._engine.SaveAllModifiedSeqFiles(int(options)))

    @property
    @ts_interface
    def search_directories(self) -> SearchDirectories:
        return SearchDirectories(self._engine.SearchDirectories, self)

    @ts_interface
    def search_files(
        self,
        search_string: str,
        search_options: SearchOption | int,
        filter_options: SearchFilterOption | int,
        elements_to_search: SearchElement | int,
        limit_to_adapters: list[str] | None = None,
        limit_to_named_props: list[str] | None = None,
        limit_to_props_of_named_types: list[str] | None = None,
        open_files_to_search: list[PropertyObjectFile] | None = None,
        directories_and_file_paths: list[str] | None = None,
    ) -> SearchResults:
        adapters_com = limit_to_adapters if limit_to_adapters is not None else []
        props_com = limit_to_named_props if limit_to_named_props is not None else []
        types_com = (
            limit_to_props_of_named_types if limit_to_props_of_named_types is not None else []
        )
        files_com = (
            [f._com_obj for f in open_files_to_search] if open_files_to_search is not None else []
        )
        paths_com = directories_and_file_paths if directories_and_file_paths is not None else []

        return SearchResults(
            self._engine.SearchFiles(
                search_string,
                int(search_options),
                int(filter_options),
                int(elements_to_search),
                adapters_com,
                props_com,
                types_com,
                files_com,
                paths_com,
            ),
            self,
        )

    @property
    @ts_interface
    def seconds_at_start_in_1970_universal_coordinated_time(self) -> float:
        return float(self._engine.SecondsAtStartIn1970UniversalCoordinatedTime)

    @property
    @ts_interface
    def seconds_since_1970_universal_coordinated_time(self) -> float:
        return float(self._engine.SecondsSince1970UniversalCoordinatedTime)

    @property
    @ts_interface
    def seconds_since_start(self) -> float:
        return float(self._engine.SecondsSinceStart)

    @property
    @ts_interface
    def seq_file_version_auto_increment_opt(self) -> typing.Any:
        return FileVersionAutoIncrement(self._engine.SeqFileVersionAutoIncrementOpt)

    @seq_file_version_auto_increment_opt.setter
    @ts_interface
    def seq_file_version_auto_increment_opt(self, value: FileVersionAutoIncrement | int) -> None:
        self._engine.SeqFileVersionAutoIncrementOpt = int(value)

    @ts_interface
    def serialize_objects(
        self,
        objects: list[PropertyObject],
        options: SerializationOption | int = 0,
    ) -> str:
        obs_com = [obj._com_obj for obj in objects]
        return str(self._engine.SerializeObjects(obs_com, int(options)))

    @ts_interface
    def set_config_directory(self, path: str, copy_files_on_shutdown: bool) -> typing.Any:
        self._engine.SetConfigDirectory(path, bool(copy_files_on_shutdown))

    @ts_interface
    def set_internal_option(
        self, option: InternalOption | int, new_value: typing.Any
    ) -> typing.Any:
        self._engine.SetInternalOption(int(option), new_value)

    @ts_interface
    def set_location_for_next_dialog(
        self,
        location_lookup_string: str,
        element_at_location: SearchElement | int,
        selection_start: int,
        selection_length: int,
    ) -> None:
        self._engine.SetLocationForNextDialog(
            location_lookup_string,
            int(element_at_location),
            int(selection_start),
            int(selection_length),
        )

    @ts_interface
    def set_module_profiling(self, adapter_key_name: str, enabled: bool) -> typing.Any:
        self._engine.SetModuleProfiling(adapter_key_name, bool(enabled))

    @ts_interface
    def set_product_registration_info(
        self,
        user_name: str,
        company_name: str,
        serial_number: str,
    ) -> bool:
        return bool(self._engine.SetProductRegistrationInfo(user_name, company_name, serial_number))

    @ts_interface
    def set_type_palette_file_list(
        self, type_palette_files: list[PropertyObjectFile]
    ) -> typing.Any:
        files_com = [f._com_obj for f in type_palette_files]
        self._engine.SetTypePaletteFileList(files_com)

    @ts_interface
    def should_auto_launch_external_report_viewer(self, file_path: str) -> typing.Any:
        return bool(self._engine.ShouldAutoLaunchExternalReportViewer(file_path))

    @property
    @ts_interface
    def show_hidden_properties(self) -> bool:
        return bool(self._engine.ShowHiddenProperties)

    @show_hidden_properties.setter
    @ts_interface
    def show_hidden_properties(self, value: bool) -> None:
        self._engine.ShowHiddenProperties = bool(value)

    @ts_interface
    def shut_down(self, final: bool) -> typing.Any:
        self._engine.ShutDown(bool(final))

    @property
    @ts_interface
    def small_image_list(self) -> int:
        return int(self._engine.SmallImageList)

    @property
    @ts_interface
    def small_image_list_ex(self) -> int:
        return int(self._engine.SmallImageListEx)

    @property
    @ts_interface
    def station_id(self) -> str:
        return str(self._engine.StationID)

    @station_id.setter
    @ts_interface
    def station_id(self, value: str) -> None:
        self._engine.StationID = value

    @property
    @ts_interface
    def station_model_sequence_file_path(self) -> str:
        return str(self._engine.StationModelSequenceFilePath)

    @station_model_sequence_file_path.setter
    @ts_interface
    def station_model_sequence_file_path(self, value: str) -> None:
        self._engine.StationModelSequenceFilePath = value

    @property
    @ts_interface
    def station_options(self) -> StationOptions:
        from py_teststand.station.station_options import StationOptions

        return StationOptions(self._engine.StationOptions, self)

    @property
    @ts_interface
    def step_types(self) -> PropertyObject:
        from py_teststand.property.property_object import PropertyObject

        return PropertyObject(self._engine.StepTypes, self)

    @property
    @ts_interface
    def temporary_globals(self) -> PropertyObject:
        from py_teststand.property.property_object import PropertyObject

        return PropertyObject(self._engine.TemporaryGlobals, self)

    @ts_interface
    def terminate_all(self) -> None:
        self._engine.TerminateAll()

    @property
    @ts_interface
    def teststand_directory(self) -> str:
        return str(self._engine.TestStandDirectory)

    @property
    @ts_interface
    def tracing_enabled(self) -> bool:
        return bool(self._engine.TracingEnabled)

    @tracing_enabled.setter
    @ts_interface
    def tracing_enabled(self, value: bool) -> None:
        self._engine.TracingEnabled = bool(value)

    @property
    @ts_interface
    def ui_message_delay(self) -> int:
        return int(self._engine.UIMessageDelay)

    @ui_message_delay.setter
    @ts_interface
    def ui_message_delay(self, value: int) -> None:
        self._engine.UIMessageDelay = int(value)

    @property
    @ts_interface
    def ui_message_min_delay(self) -> int:
        return int(self._engine.UIMessageMinDelay)

    @ui_message_min_delay.setter
    @ts_interface
    def ui_message_min_delay(self, value: int) -> None:
        self._engine.UIMessageMinDelay = int(value)

    @property
    @ts_interface
    def ui_message_polling_enabled(self) -> typing.Any:
        return bool(self._engine.UIMessagePollingEnabled)

    @ui_message_polling_enabled.setter
    @ts_interface
    def ui_message_polling_enabled(self, value: bool) -> None:
        self._engine.UIMessagePollingEnabled = bool(value)

    @property
    @ts_interface
    def undo_limit(self) -> int:
        return int(self._engine.UndoLimit)

    @undo_limit.setter
    @ts_interface
    def undo_limit(self, value: int) -> None:
        self._engine.UndoLimit = int(value)

    @property
    @ts_interface
    def unique_engine_id(self) -> str:
        return str(self._engine.UniqueEngineId)

    @ts_interface
    def unload_all_modules(self) -> None:
        self._engine.UnloadAllModules()

    @ts_interface
    def unload_type_palette_files(self) -> None:
        self._engine.UnloadTypePaletteFiles()

    @ts_interface
    def unregister_modal_window(self, modal_id: int) -> typing.Any:
        self._engine.UnregisterModalWindow(int(modal_id))

    @ts_interface
    def unregister_sequence_to_execute_on_crash(self, registration_id: int) -> typing.Any:
        self._engine.UnregisterSequenceToExecuteOnCrash(int(registration_id))

    @ts_interface
    def unserialize_objects(
        self,
        stream: str,
        reserved_param: int = 0,
        handler_type: ConflictHandler | int = ConflictHandler.Error,
    ) -> list[PropertyObject]:
        from py_teststand.property.property_object import PropertyObject

        ret_com = self._engine.UnserializeObjects(stream, int(reserved_param), int(handler_type))
        return [PropertyObject(obj_com, self) for obj_com in ret_com]

    @ts_interface
    def unserialize_objects_and_types(
        self,
        stream: str,
        reserved_param: int = 0,
        handler_type: ConflictHandler | int = ConflictHandler.Error,
    ) -> tuple[list[PropertyObject], TypeUsageList]:
        from py_teststand.property.property_object import PropertyObject
        from py_teststand.property.property_object_file import TypeUsageList

        types_used_com = None
        ret_com = self._engine.UnserializeObjectsAndTypes(
            stream, types_used_com, int(reserved_param), int(handler_type)
        )

        return [PropertyObject(obj_com, self) for obj_com in ret_com], TypeUsageList(
            typing.cast(typing.Any, types_used_com), self
        )

    @property
    @ts_interface
    def use_dialog_for_check_out(self) -> bool:
        return bool(self._engine.UseDialogForCheckOut)

    @use_dialog_for_check_out.setter
    @ts_interface
    def use_dialog_for_check_out(self, value: bool) -> None:
        self._engine.UseDialogForCheckOut = bool(value)

    @property
    @ts_interface
    def use_localized_decimal_point(self) -> bool:
        return bool(self._engine.UseLocalizedDecimalPoint)

    @use_localized_decimal_point.setter
    @ts_interface
    def use_localized_decimal_point(self, value: bool) -> None:
        self._engine.UseLocalizedDecimalPoint = bool(value)

    @ts_interface
    def user_name_exists(self, login_name: str) -> typing.Any:
        return bool(self._engine.UserNameExists(login_name))

    @property
    @ts_interface
    def users_file(self) -> UsersFile:
        from py_teststand.users.users_file import UsersFile

        return UsersFile(self._engine.UsersFile, self)

    @property
    @ts_interface
    def utility(self) -> Utility:
        from py_teststand.core.utility import Utility

        return Utility(self._engine.Utility, self)

    @property
    @ts_interface
    def version_string(self) -> str:
        return str(self._engine.VersionString)

    @property
    @ts_interface
    def parsed_version(self) -> str | None:
        version_string = self.version_string
        match = re.search(r"\((\d+\.\d+)[^)]*\)", version_string)
        return match.group(1) if match else None

    @property
    @ts_interface
    def watch_expressions_enabled(self) -> bool:
        return bool(self._engine.WatchExpressionsEnabled)

    @watch_expressions_enabled.setter
    @ts_interface
    def watch_expressions_enabled(self, value: bool) -> None:
        self._engine.WatchExpressionsEnabled = bool(value)

    @ts_interface
    def write_tool_menu_to_disk(self, reserved: int = 0) -> typing.Any:
        self._engine.WriteToolMenuToDisk(int(reserved))

    @ts_interface
    def _bootstrap_engine(self) -> None:
        pass

    def shutdown(self) -> None:

        if self._engine is None:
            return
        try:
            cb = getattr(self, "_atexit_callable", None)
            if cb is not None:
                atexit.unregister(cb)
        except Exception:
            pass
        if Engine._is_shutting_down:
            return
        Engine._is_shutting_down = True
        try:
            if self._ui_handler:
                try:
                    self._ui_handler.stop()
                except Exception:
                    pass
                finally:
                    self._ui_handler = None
            if self._station_options:
                try:
                    self._station_options.release()
                except Exception:
                    pass
                finally:
                    self._station_options = None
            for path in list(Engine._loaded_files.keys()):
                f = Engine._loaded_files.pop(path, None)
                if f:
                    try:
                        if self._engine and f._com_obj:
                            self._engine.ReleaseSequenceFile(f._com_obj)
                        f.release()
                    except Exception:
                        pass

            try:
                self.abort_all()
            except Exception:
                pass

            try:
                opts = self.station_options
                if opts.get_val_boolean("SaveOnClose"):
                    try:
                        self.commit_globals_to_disk()
                    except Exception:
                        pass
                    try:
                        users = self.users_file
                        if users:
                            users.save()
                    except Exception:
                        pass
            except Exception:
                pass

            Engine._loaded_files.clear()
            import sys

            if "pytest" not in sys.modules:
                try:
                    self._engine.ShutDown(True)
                except Exception:
                    pass
            self._engine = cast(typing.Any, None)
            if "pytest" not in sys.modules:
                gc.collect()
                pythoncom.PumpWaitingMessages()
                time.sleep(0.05)
                gc.collect()
        except Exception as exc:
            warnings.warn(f"Shutdown error: {exc}", stacklevel=2)
            self._engine = cast(typing.Any, None)
        finally:
            Engine._is_shutting_down = False
