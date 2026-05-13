from __future__ import annotations

import typing
from enum import IntEnum

from py_teststand.core.com_wrapper import ts_interface
from py_teststand.execution.execution import Execution
from py_teststand.execution.thread import Thread
from py_teststand.property.property_object import PropertyObject


class UIMessageCode(IntEnum):
    BreakOnUserRequest = 1
    BreakOnBreakpoint = 2
    BreakOnRunTimeError = 3
    Trace = 4
    TerminatingExecution = 5
    AbortingExecution = 6
    KillingExecutionThreads = 7
    EndExecution = 8
    ShutDownComplete = 9
    StartExecution = 10
    ProgressPercent = 11
    ProgressText = 12
    StartInteractiveExecution = 13
    EndInteractiveExecution = 14
    TerminatingInteractiveExecution = 15
    TerminationCancelled = 16
    ResumeFromBreak = 17
    StartFileExecution = 18
    EndFileExecution = 19
    ShutDownCancelled = 20
    LocalizationSettingChanged = 21
    OpenWindows = 22
    TileWindows = 23
    CascadeWindows = 24
    ReportChanged = 25
    CloseWindows = 26
    RefreshWindows = 27
    ClientFileChanged = 28
    DisplayReport = 29
    Initializing = 30
    Waiting = 31
    Identified = 32
    BeginTesting = 33
    TestingComplete = 34
    PostProcessingComplete = 35
    EnabledStateSet = 36
    ReportLocationChanged = 37
    GotoLocation = 38
    PushUndoItem = 39
    OutputMessages = 40
    TypePaletteFileListChanged = 41
    NonTerminatableThreadsArePreventingTermination = 42
    PostProcessing = 43
    ReportCollectionChanged = 44
    RuntimeError = 45
    UserMessageBase = 10000


class MsgBoxType(IntEnum):
    Warning = 0
    Information = 1
    Error = 2
    Custom = 3


class UIMessage(PropertyObject):
    @ts_interface
    def as_property_object(self) -> PropertyObject:
        return PropertyObject(self._com_obj.AsPropertyObject(), self._engine_ref)

    @property
    @ts_interface
    def event(self) -> int:
        return int(self._com_obj.Event)

    @property
    @ts_interface
    def is_synchronous(self) -> bool:
        return bool(self._com_obj.IsSynchronous)

    @property
    @ts_interface
    def execution(self) -> Execution | None:
        com = self._com_obj.Execution
        if com is None:
            return None
        return Execution(com, self._engine_ref)

    @property
    @ts_interface
    def thread(self) -> Thread | None:
        com = self._com_obj.Thread
        if com is None:
            return None
        return Thread(com, self._engine_ref)

    @property
    @ts_interface
    def numeric_data(self) -> float:
        return float(self._com_obj.NumericData)

    @property
    @ts_interface
    def string_data(self) -> str:
        return str(self._com_obj.StringData)

    @property
    @ts_interface
    def activex_data(self) -> typing.Any:
        return self._com_obj.ActiveXData

    @ts_interface
    def acknowledge(self) -> None:
        self._com_obj.Acknowledge()
