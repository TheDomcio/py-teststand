from __future__ import annotations

from enum import Enum, IntEnum, IntFlag


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
    UseBinary = 1
    UseXml = 2
    SupportNonTypedefMatchingInstances = 4


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
    PropertyNodeVIWrapper = 2
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
    NeverOverride = 1


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
