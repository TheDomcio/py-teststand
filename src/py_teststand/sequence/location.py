from __future__ import annotations

import typing
from enum import IntEnum, IntFlag

from py_teststand.core.com_wrapper import COMWrapper, ts_interface


class GotoLocationOption(IntFlag):
    NoneValue = 0
    DoNotDisplayMessageIfLocationNotFound = 0x1


class AutoCreateVariableLocation(IntEnum):
    Locals = 1
    Parameters = 2
    FileGlobals = 3
    StationGlobals = 4


class LocationKind(IntEnum):
    File = 1
    Execution = 2
    Type = 3
    IOConfiguration = 4


class APILocation(IntEnum):
    ActiveXModule_ActiveXReferenceExpr = 65
    ActiveXModule_FilePath = 66
    ActiveXModule_RemoteHost = 67
    ActiveXParameter_ValueExpr = 68
    AdditionalResult_Condition = 57
    AdditionalResult_Name = 58
    AdditionalResult_ValueToLog = 59
    CommonCModule_ModulePath = 51
    CommonCModule_ProjectFilePath = 52
    CommonCModule_SourceFilePath = 53
    CommonCModule_WorkspaceFilePath = 54
    CommonCParameter_StringBufferSizeExpr = 56
    CommonCParameter_ValueExpr = 55
    DllParameter_ImaginaryPartValueExpr = 124
    DotNetModule_GetAssembly = 63
    DotNetModule_ProjectFilePath = 60
    DotNetModule_SolutionFilePath = 61
    DotNetModule_SourceFilePath = 62
    DotNetParameter_ParameterName = 127
    DotNetParameter_ValueExpr = 64
    HTBasicModule_SubroutineFilePath = 70
    LabVIEWModule_CallName = 130
    LabVIEWModule_ClassPath = 129
    LabVIEWModule_GetVIAbsolutePath = 48
    LabVIEWModule_NodeLibraryName = 133
    LabVIEWModule_OverrideBinaryClassPath = 154
    LabVIEWModule_OverrideBinaryProjectPath = 152
    LabVIEWModule_OverrideBinaryVIPath = 153
    LabVIEWModule_OverrideSourceClassPath = 143
    LabVIEWModule_OverrideSourceProjectPath = 141
    LabVIEWModule_OverrideSourceVIPath = 142
    LabVIEWModule_ProjectPath = 47
    LabVIEWModule_RemoteConnectionTimeout = 46
    LabVIEWModule_RemoteHost = 44
    LabVIEWModule_RemotePortNumber = 45
    LabVIEWModule_VIPath = 42
    LabVIEWModule_VIType = 43
    LabVIEWNXGModule_GllPath = 135
    LabVIEWNXGModule_ModuleQualifiedName = 139
    LabVIEWNXGModule_ProjectPath = 134
    LabVIEWNXGModule_QualifiedName = 136
    LabVIEWNXGParameter_ParameterLabel = 137
    LabVIEWNXGParameter_Type = 140
    LabVIEWNXGParameter_ValueExpression = 138
    LabVIEWParameter_ParameterCaption = 126
    LabVIEWParameter_ValueExpr = 49
    LabVIEWParameterElement_ElementCaption = 125
    LabVIEWParameterElement_ValueExpr = 50
    NoneValue = 0
    PythonModule_ClassInstanceLocationExpr = 150
    PythonModule_ClassName = 148
    PythonModule_FunctionOrAttributeName = 149
    PythonModule_InterpreterReferenceExpr = 147
    PythonModule_ModulePath = 145
    PythonModule_PythonVersion = 144
    PythonModule_PythonVirtualEnvironmentPath = 146
    PythonParameter_ValueExpr = 151
    Sequence_DisableResults = 128
    SequenceCallModule_CustomCPUAffinityForNewThread = 71
    SequenceCallModule_NewExecutionBreakOnEntryExpr = 72
    SequenceCallModule_NewExecutionModelPath = 73
    SequenceCallModule_NewExecutionTypeMaskExpr = 74
    SequenceCallModule_RemoteHost = 75
    SequenceCallModule_SequenceFilePath = 76
    SequenceCallModule_SequenceName = 77
    SequenceCallModule_StoreActiveXReferenceExpr = 78
    SequenceCallParameter_ValueExpr = 79
    SequenceFile_ModelPath = 123
    Step_BatchSyncOption = 1
    Step_CustomActionExpression = 2
    Step_CustomFalseAction = 3
    Step_CustomFalseActionTargetByExpr = 4
    Step_CustomTrueAction = 5
    Step_CustomTrueActionTargetByExpr = 6
    Step_EvalPrecondForInteractiveExecution = 7
    Step_FailAction = 8
    Step_FailActionTargetByExpr = 9
    Step_IconName = 10
    Step_IgnoreRTE = 11
    Step_LoopIncExpression = 12
    Step_LoopInitExpression = 13
    Step_LoopStatusExpression = 14
    Step_LoopType = 15
    Step_LoopWhileExpression = 16
    Step_ModuleLoadOption = 17
    Step_ModuleUnloadOption = 18
    Step_MutexNameOrRefExpr = 19
    Step_PassAction = 20
    Step_PassActionTargetByExpr = 21
    Step_PostExpression = 22
    Step_Precondition = 23
    Step_PreExpression = 24
    Step_RecordLoopIterationResults = 25
    Step_RecordResult = 26
    Step_ResultRecordingOption = 131
    Step_RunMode = 27
    Step_StatusExpression = 28
    Step_StepFailCausesSequenceFail = 29
    Step_SwitchExecConnectionLifetime = 30
    Step_SwitchExecEnabled = 31
    Step_SwitchExecMulticonnectMode = 32
    Step_SwitchExecOperation = 33
    Step_SwitchExecOperationOrder = 34
    Step_SwitchExecRoutesToConnect = 35
    Step_SwitchExecRoutesToDisconnect = 36
    Step_SwitchExecVirtualDevice = 37
    Step_SwitchExecWaitForDebounce = 38
    Step_UniqueStepId = 39
    Step_UseMutex = 40
    Step_WindowActivation = 41
    StepType_BatchSyncOption = 108
    StepType_CustomActionExpression = 95
    StepType_CustomFalseAction = 97
    StepType_CustomFalseActionTargetByExpr = 99
    StepType_CustomTrueAction = 96
    StepType_CustomTrueActionTargetByExpr = 98
    StepType_DefaultNameExpr = 113
    StepType_DescriptionExpr = 114
    StepType_EvalPrecondForInteractiveExecution = 83
    StepType_FailAction = 92
    StepType_FailActionTargetByExpr = 94
    StepType_IconName = 80
    StepType_IgnoreRTE = 116
    StepType_LoopIncExpression = 87
    StepType_LoopInitExpression = 86
    StepType_LoopStatusExpression = 89
    StepType_LoopType = 90
    StepType_LoopWhileExpression = 88
    StepType_MenuItemNameExpr = 115
    StepType_ModuleLoadOption = 81
    StepType_ModuleUnloadOption = 82
    StepType_MutexNameOrRefExpr = 107
    StepType_PassAction = 91
    StepType_PassActionTargetByExpr = 93
    StepType_PostExpression = 110
    StepType_Precondition = 112
    StepType_PreExpression = 109
    StepType_RecordLoopIterationResults = 117
    StepType_RecordResult = 118
    StepType_ResultRecordingOption = 132
    StepType_RunMode = 85
    StepType_StatusExpression = 111
    StepType_StepFailCausesSequenceFail = 119
    StepType_SwitchExecConnectionLifetime = 104
    StepType_SwitchExecEnabled = 120
    StepType_SwitchExecMulticonnectMode = 103
    StepType_SwitchExecOperation = 101
    StepType_SwitchExecOperationOrder = 106
    StepType_SwitchExecRoutesToConnect = 102
    StepType_SwitchExecRoutesToDisconnect = 105
    StepType_SwitchExecVirtualDevice = 100
    StepType_SwitchExecWaitForDebounce = 121
    StepType_UseMutex = 122
    StepType_WindowActivation = 84


class PropertyObjectElement(IntEnum):
    Attributes = 7
    Comment = 3
    Flags = 4
    Name = 2
    NoneValue = 0
    NumericFormat = 5
    Representation = 6
    Value = 1


class TypeCategory(IntFlag):
    BuiltinDataTypes = 3
    CustomDataTypes = 2
    NoneValue = 0
    StepTypes = 1


class ApplicationSite(IntEnum):
    DefaultSite = 0
    ItemList = 1
    PropertyBrowser = 3
    Settings = 4
    Variables = 2


class Location(COMWrapper):
    @property
    @ts_interface
    def kind(self) -> typing.Any:
        return int(self._com_obj.Kind)

    @kind.setter
    @ts_interface
    def kind(self, value: int) -> None:
        self._com_obj.Kind = value

    @property
    @ts_interface
    def file_path(self) -> str:
        return str(self._com_obj.FilePath)

    @file_path.setter
    @ts_interface
    def file_path(self, value: str) -> None:
        self._com_obj.FilePath = value

    @property
    @ts_interface
    def io_configuration_name(self) -> str:
        return str(self._com_obj.IOConfigurationName)

    @io_configuration_name.setter
    @ts_interface
    def io_configuration_name(self, value: str) -> None:
        self._com_obj.IOConfigurationName = value

    @property
    @ts_interface
    def file_id(self) -> int:
        return int(self._com_obj.FileId)

    @file_id.setter
    @ts_interface
    def file_id(self, value: int) -> None:
        self._com_obj.FileId = value

    @property
    @ts_interface
    def file_display_name(self) -> str:
        return str(self._com_obj.FileDisplayName)

    @file_display_name.setter
    @ts_interface
    def file_display_name(self, value: str) -> None:
        self._com_obj.FileDisplayName = value

    @property
    @ts_interface
    def property_path(self) -> str:
        return str(self._com_obj.PropertyPath)

    @property_path.setter
    @ts_interface
    def property_path(self, value: str) -> None:
        self._com_obj.PropertyPath = value

    @property
    @ts_interface
    def context_id(self) -> int:
        return int(self._com_obj.ContextId)

    @context_id.setter
    @ts_interface
    def context_id(self, value: int) -> None:
        self._com_obj.ContextId = value

    @property
    @ts_interface
    def type_name(self) -> str:
        return str(self._com_obj.TypeName)

    @type_name.setter
    @ts_interface
    def type_name(self, value: str) -> None:
        self._com_obj.TypeName = value

    @property
    @ts_interface
    def attributes_path(self) -> str:
        return str(self._com_obj.AttributesPath)

    @property
    @ts_interface
    def base_attributes_path(self) -> str:
        return str(self._com_obj.BaseAttributesPath)

    @property
    @ts_interface
    def element(self) -> typing.Any:
        return self._com_obj.Element

    @property
    @ts_interface
    def execution_display_name(self) -> str:
        return str(self._com_obj.ExecutionDisplayName)

    @property
    @ts_interface
    def execution_id(self) -> int:
        return int(self._com_obj.ExecutionId)

    @property
    @ts_interface
    def property_path_with_names(self) -> str:
        return str(self._com_obj.PropertyPathWithNames)

    @property
    @ts_interface
    def sel_length(self) -> int:
        return int(self._com_obj.SelLength)

    @property
    @ts_interface
    def sel_start(self) -> int:
        return int(self._com_obj.SelStart)

    @property
    @ts_interface
    def sequence_name(self) -> str:
        return str(self._com_obj.SequenceName)

    @property
    @ts_interface
    def step_group(self) -> typing.Any:
        return self._com_obj.StepGroup

    @property
    @ts_interface
    def step_id(self) -> str:
        return str(self._com_obj.StepId)

    @property
    @ts_interface
    def step_index(self) -> int:
        return int(self._com_obj.StepIndex)

    @property
    @ts_interface
    def step_name(self) -> str:
        return str(self._com_obj.StepName)

    @property
    @ts_interface
    def thread_display_name(self) -> str:
        return str(self._com_obj.ThreadDisplayName)

    @property
    @ts_interface
    def thread_id(self) -> int:
        return int(self._com_obj.ThreadId)

    @property
    @ts_interface
    def type_category(self) -> typing.Any:
        return self._com_obj.TypeCategory


class Locations(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index_or_name: typing.Any) -> Location:
        return Location(self._com_obj.Item(index_or_name), self._engine_ref)

    @ts_interface
    def get_by_index(self, index: int) -> Location:
        if index < 0 or index >= self.count:
            raise IndexError(f"Location index {index} out of range (count={self.count})")
        return Location(self._com_obj.Item(index), self._engine_ref)

    @ts_interface
    def add_api_location(
        self,
        base_obj: typing.Any,
        api_location: int,
        obj_file: typing.Any = None,
    ) -> Location:
        com_base = getattr(base_obj, "_com_obj", base_obj)
        com_file = getattr(obj_file, "_com_obj", obj_file) if obj_file else None
        return Location(
            self._com_obj.AddAPILocation(com_base, int(api_location), com_file),
            self._engine_ref,
        )

    @ts_interface
    def add_execution_location(
        self,
        seq_context: typing.Any,
        lookup_string: str,
        elem: int = 0,
        selection_start: int = 0,
        selection_length: int = -1,
    ) -> Location:
        com_ctx = getattr(seq_context, "_com_obj", seq_context)
        return Location(
            self._com_obj.AddExecutionLocation(
                com_ctx,
                lookup_string,
                int(elem),
                int(selection_start),
                int(selection_length),
            ),
            self._engine_ref,
        )

    @ts_interface
    def add_execution_location_by_object(
        self,
        seq_context: typing.Any,
        obj: typing.Any,
        elem: int = 0,
        selection_start: int = 0,
        selection_length: int = -1,
    ) -> Location:
        com_ctx = getattr(seq_context, "_com_obj", seq_context)
        com_obj = getattr(obj, "_com_obj", obj)
        return Location(
            self._com_obj.AddExecutionLocationByObject(
                com_ctx,
                com_obj,
                int(elem),
                int(selection_start),
                int(selection_length),
            ),
            self._engine_ref,
        )

    @ts_interface
    def add_file_location(
        self,
        file: typing.Any,
        lookup_string: str,
        elem: int = 0,
        selection_start: int = 0,
        selection_length: int = -1,
    ) -> Location:
        com_file = getattr(file, "_com_obj", file)
        return Location(
            self._com_obj.AddFileLocation(
                com_file,
                lookup_string,
                int(elem),
                int(selection_start),
                int(selection_length),
            ),
            self._engine_ref,
        )

    @ts_interface
    def add_file_location_by_object(
        self,
        obj: typing.Any,
        elem: int = 0,
        selection_start: int = 0,
        selection_length: int = -1,
    ) -> Location:
        com_obj = getattr(obj, "_com_obj", obj)
        return Location(
            self._com_obj.AddFileLocationByObject(
                com_obj,
                int(elem),
                int(selection_start),
                int(selection_length),
            ),
            self._engine_ref,
        )

    @ts_interface
    def add_io_configuration_location(self, io_configuration_name: str) -> Location:
        return Location(
            self._com_obj.AddIOConfiguraionLocation(str(io_configuration_name)),
            self._engine_ref,
        )

    @ts_interface
    def add_locations(self, locations_to_add: typing.Any, copy_location_option: int) -> typing.Any:
        com_locs = getattr(locations_to_add, "_com_obj", locations_to_add)
        self._com_obj.AddLocations(com_locs, int(copy_location_option))

    @ts_interface
    def add_type_location(
        self,
        file: typing.Any,
        root_type_def: typing.Any,
        lookup_string: str,
        elem: int = 0,
        selection_start: int = 0,
        selection_length: int = -1,
    ) -> Location:
        com_file = getattr(file, "_com_obj", file)
        com_root = getattr(root_type_def, "_com_obj", root_type_def)
        return Location(
            self._com_obj.AddTypeLocation(
                com_file,
                com_root,
                lookup_string,
                int(elem),
                int(selection_start),
                int(selection_length),
            ),
            self._engine_ref,
        )

    @ts_interface
    def add_type_location_by_object(
        self,
        file: typing.Any,
        obj: typing.Any,
        elem: int = 0,
        selection_start: int = 0,
        selection_length: int = -1,
    ) -> Location:
        com_file = getattr(file, "_com_obj", file)
        com_obj = getattr(obj, "_com_obj", obj)
        return Location(
            self._com_obj.AddTypeLocationByObject(
                com_file,
                com_obj,
                int(elem),
                int(selection_start),
                int(selection_length),
            ),
            self._engine_ref,
        )

    @property
    @ts_interface
    def application_site(self) -> typing.Any:
        return int(self._com_obj.ApplicationSite)

    @application_site.setter
    @ts_interface
    def application_site(self, value: int) -> None:
        self._com_obj.ApplicationSite = int(value)

    @property
    @ts_interface
    def can_display_dialog(self) -> bool:
        return bool(self._com_obj.CanDisplayDialog)

    @property
    @ts_interface
    def location_found(self) -> bool:
        return bool(self._com_obj.LocationFound)

    @property
    @ts_interface
    def location_not_found_message(self) -> str:
        return str(self._com_obj.LocationNotFoundMessage)

    @location_not_found_message.setter
    @ts_interface
    def location_not_found_message(self, value: str) -> None:
        self._com_obj.LocationNotFoundMessage = str(value)

    @property
    @ts_interface
    def user_data(self) -> typing.Any:
        return self._com_obj.UserData

    @user_data.setter
    @ts_interface
    def user_data(self, value: typing.Any) -> None:
        self._com_obj.UserData = value

    @ts_interface
    def to_property_object(self) -> typing.Any:
        from py_teststand.property.property_object import PropertyObject

        return PropertyObject(self._com_obj.ToPropertyObject(), self._engine_ref)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def from_property_object(self, val: typing.Any) -> None:
        com_po = getattr(val, "_com_obj", val)
        self._com_obj.FromPropertyObject(com_po)

    @ts_interface
    def goto_location(self, options: int = 0) -> None:
        self._com_obj.GotoLocation(int(options))

    @ts_interface
    def goto_location_in_application(self, application_path: str, options: int = 0) -> None:
        self._com_obj.GotoLocationInApplication(str(application_path), int(options))

    @ts_interface
    def remove(self, index_or_name: typing.Any) -> None:
        self._com_obj.Remove(index_or_name)

    def __len__(self) -> int:

        return self.count

    def __getitem__(self, index_or_name: typing.Any) -> Location:

        return self.item(index_or_name)
