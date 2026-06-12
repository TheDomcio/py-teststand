from __future__ import annotations

try:
    from importlib.metadata import version as _version

    __version__ = _version("py-teststand")
except Exception:
    __version__ = "0.1.0"


from .adapters import (
    ActiveXAdapter,
    ActiveXModule,
    CVIAdapter,
    CVIModule,
    DLLAdapter,
    DLLModule,
    DotNetAdapter,
    DotNetModule,
    HTBasicAdapter,
    HTBasicModule,
    LabVIEWAdapter,
    LabVIEWModule,
    LabVIEWNXGAdapter,
    LabVIEWNXGModule,
    PythonAdapter,
    PythonModule,
    SequenceAdapter,
    SequenceCallModule,
    UnmappedArgumentValue,
    UnmappedArgumentValueList,
)
from .adapters.adapter import Adapter, Module
from .core.com_wrapper import COMWrapper, ts_interface  # noqa: F401
from .core.engine import (
    AdapterKeyName,
    AllowAutomaticTypeConflictResolution,
    ConflictResolution,
    EditKind,
    Engine,
    FindFilePromptOption,
    FindFileSearchListOption,
    GetSeqFileOption,
    GetTemplatesFileOption,
    OpenWorkspaceFileOption,
    ReleaseSeqFileOption,
    RTEOption,
    TestStandPath,
)
from .core.exceptions import (
    AccessDeniedError,
    AdapterError,
    COMError,
    DeploymentError,
    Error,
    ExecutionError,
    FileAlreadyExistsError,
    FileNotFoundError,
    IndexOutOfRangeError,
    InvalidPropertyError,
    IOError,
    LicenseError,
    MemoryError,
    ModuleLoadError,
    PathNotFoundError,
    PropertyError,
    SequenceAbortedError,
    SequenceFileLoadError,
    SequenceTerminatedError,
    SequenceValidationError,
    StepExecutionError,
    SystemError,
    TypeMismatchError,
)
from .core.file_information import FileInformation
from .core.search import (
    SearchElement,
    SearchFilterOption,
    SearchMatch,
    SearchOption,
    SearchResults,
)
from .execution.additional_results import (
    AdditionalResult,
    AdditionalResultKind,
    AdditionalResults,
    CheckedState,
)
from .execution.breakpoint import SelectedBreakpointItem
from .execution.database_options import DatabaseLogOptions
from .execution.edit_args import EditArgs
from .execution.execution import Execution, ExecutionTypeMask
from .execution.interactive_args import InteractiveArgs, InteractiveContext
from .execution.report import Report, ReportConversion, Reports, ReportSection, ReportSections
from .execution.result_log import ResultLog, ResultLogger, ResultLogRecordType
from .execution.sync_manager import (
    AutoReleaser,
    Batch,
    Mutex,
    Notification,
    Queue,
    Rendezvous,
    Semaphore,
    SyncManager,
)
from .execution.thread import (
    SeqCallNewExecModelOption,
    SeqCallNewThreadOption,
    SeqCallWaitForExecOption,
    Thread,
)
from .execution.watch_expression import WatchExpression, WatchExpressions
from .messaging.output_message import OutputMessage
from .messaging.output_messages import OutputMessages
from .messaging.ui_message import UIMessage, UIMessageCode
from .property.array_dimensions import ArrayDimensions
from .property.data_type import (
    DataType,
    PropertyObjectType,
    PropertyRepresentation,
    PropertyValueTypeFlag,
    PropValType,
)
from .property.property_object import PropertyFlag, PropertyObject, PropertyOption, TypeCategory
from .property.property_object_file import (
    FileWritingFormat,
    PropertyObjectFile,
    PropertyObjectFileType,
    TypeUsageList,
)
from .sequence.code_template import CodeTemplate, CodeTemplates
from .sequence.expression import EvaluationType, Expression
from .sequence.location import AutoCreateVariableLocation, Location, Locations
from .sequence.sequence import Sequence
from .sequence.sequence_context import SequenceContext
from .sequence.sequence_file import SequenceFile
from .sequence.step import RunMode, Step
from .sequence.step_group import StepGroup, StepGroupMode
from .sequence.step_type import StepType
from .station.search_directories import SearchDirectories, SearchDirectory
from .station.station_options import (
    DebugOption,
    InteractiveBranchMode,
    StationOptions,
    TimeLimitAction,
)
from .ui.application_manager import ApplicationManager
from .ui.execution_view_manager import ExecutionViewManager
from .ui.sequence_file_view_manager import SequenceFileViewManager
from .undo.undo_item import UndoItem
from .undo.undo_item_creator import UndoItemCreator
from .undo.undo_stack import UndoStack
from .users.user import User, UserGroup, UserPrivilege
from .users.users_file import UsersFile
from .workspace.workspace_file import SaveWorkspaceFileOption, WorkspaceFile
from .workspace.workspace_object import (
    SourceControlCommand,
    SourceControlCommandOption,
    SourceControlStatus,
    WorkspaceObject,
    WorkspaceObjectType,
)

__all__ = [
    "AccessDeniedError",
    "ActiveXAdapter",
    "ActiveXModule",
    "Adapter",
    "AdapterError",
    "AdapterKeyName",
    "AdditionalResult",
    "AdditionalResultKind",
    "AdditionalResults",
    "AllowAutomaticTypeConflictResolution",
    "ApplicationManager",
    "ArrayDimensions",
    "AutoCreateVariableLocation",
    "AutoReleaser",
    "Batch",
    "COMError",
    "CVIAdapter",
    "CVIModule",
    "CheckedState",
    "CodeTemplate",
    "CodeTemplates",
    "ConflictResolution",
    "DLLAdapter",
    "DLLModule",
    "DataType",
    "DatabaseLogOptions",
    "DebugOption",
    "DeploymentError",
    "DotNetAdapter",
    "DotNetModule",
    "EditArgs",
    "EditKind",
    "Engine",
    "Error",
    "EvaluationType",
    "Execution",
    "ExecutionError",
    "ExecutionTypeMask",
    "ExecutionViewManager",
    "Expression",
    "FileAlreadyExistsError",
    "FileInformation",
    "FileNotFoundError",
    "FileWritingFormat",
    "FindFilePromptOption",
    "FindFileSearchListOption",
    "GetSeqFileOption",
    "GetTemplatesFileOption",
    "HTBasicAdapter",
    "HTBasicModule",
    "IOError",
    "IndexOutOfRangeError",
    "InteractiveArgs",
    "InteractiveBranchMode",
    "InteractiveContext",
    "InvalidPropertyError",
    "LabVIEWAdapter",
    "LabVIEWModule",
    "LabVIEWNXGAdapter",
    "LabVIEWNXGModule",
    "LicenseError",
    "Location",
    "Locations",
    "MemoryError",
    "Module",
    "ModuleLoadError",
    "Mutex",
    "Notification",
    "OpenWorkspaceFileOption",
    "OutputMessage",
    "OutputMessages",
    "PathNotFoundError",
    "PropValType",
    "PropertyError",
    "PropertyFlag",
    "PropertyObject",
    "PropertyObjectFile",
    "PropertyObjectFileType",
    "PropertyObjectType",
    "PropertyOption",
    "PropertyRepresentation",
    "PropertyValueTypeFlag",
    "PythonAdapter",
    "PythonModule",
    "Queue",
    "RTEOption",
    "ReleaseSeqFileOption",
    "Rendezvous",
    "Report",
    "ReportConversion",
    "ReportSection",
    "ReportSections",
    "Reports",
    "ResultLog",
    "ResultLogRecordType",
    "ResultLogger",
    "RunMode",
    "SaveWorkspaceFileOption",
    "SearchDirectories",
    "SearchDirectory",
    "SearchElement",
    "SearchFilterOption",
    "SearchMatch",
    "SearchOption",
    "SearchResults",
    "SelectedBreakpointItem",
    "Semaphore",
    "SeqCallNewExecModelOption",
    "SeqCallNewThreadOption",
    "SeqCallWaitForExecOption",
    "Sequence",
    "SequenceAbortedError",
    "SequenceAdapter",
    "SequenceCallModule",
    "SequenceContext",
    "SequenceFile",
    "SequenceFileLoadError",
    "SequenceFileViewManager",
    "SequenceTerminatedError",
    "SequenceValidationError",
    "SourceControlCommand",
    "SourceControlCommandOption",
    "SourceControlStatus",
    "StationOptions",
    "Step",
    "StepExecutionError",
    "StepGroup",
    "StepGroupMode",
    "StepType",
    "SyncManager",
    "SystemError",
    "TestStandPath",
    "Thread",
    "TimeLimitAction",
    "TypeCategory",
    "TypeMismatchError",
    "TypeUsageList",
    "UIMessage",
    "UIMessageCode",
    "UndoItem",
    "UndoItemCreator",
    "UndoStack",
    "UnmappedArgumentValue",
    "UnmappedArgumentValueList",
    "User",
    "UserGroup",
    "UserPrivilege",
    "UsersFile",
    "WatchExpression",
    "WatchExpressions",
    "WorkspaceFile",
    "WorkspaceObject",
    "WorkspaceObjectType",
]
