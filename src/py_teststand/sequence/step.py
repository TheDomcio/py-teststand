from __future__ import annotations

import functools
import typing
from enum import Enum, IntEnum, IntFlag
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COM, COMWrapper, ts_interface
from py_teststand.sequence.step_group import StepGroup
from py_teststand.sequence.step_type import SwitchExecOperation

if TYPE_CHECKING:
    from py_teststand.adapters.adapter import Module


class BlockFlag(IntFlag):
    NoneValue = 0
    Open = 1
    Close = 2
    Start = 4
    End = 8
    Unmatched = 16
    AppliesToBlockStructure = 32


class ResultRecordingOption(IntEnum):
    Disabled = 0
    Enabled = 1
    EnabledAndOverrideSequenceSetting = 2


class EvalPrecondOption(IntEnum):
    UseStationOption = 0
    EvaluatePrecond = 1
    NoEvaluatePrecond = 2


class RunMode(IntEnum):
    Normal = 0
    Skip = 1
    ForcePass = 2
    ForceFail = 3


class FlexCStepAdditions:
    ExternalCall_CallConvProp = "Conv"
    ExternalCall_FunctionNameProp = "Func"
    ExternalCall_LibPathProp = "LibPath"
    ExternalCall_ParametersProp = "Params"
    FCParam_ArgValueProp = "ArgVal"
    FCParam_ArrayElemPassingProp = "ElemPass"
    FCParam_FlagsProp = "Flags"
    FCParam_NameProp = "Name"
    FCParam_NumArrayElementsProp = "NumEls"
    FCParam_NumericPassingProp = "NumPass"
    FCParam_NumericTypeProp = "NumType"
    FCParam_ObjectTypeProp = "ObjType"
    FCParam_ResultActionProp = "ResultAct"
    FCParam_StringPassingProp = "StrPass"
    FCParam_StringSizeProp = "StrSize"
    FCParam_TypeProp = "Type"
    FlexCStep_ExternalCallProp = "Call"


class GetModuleFromProjectOption(IntFlag):
    NoneValue = 0x0
    NoPrompts = 0x1


class CodeTemplateType(IntEnum):
    Legacy = 1
    LabVIEW = 2
    CVI = 3
    CppOrC = 4
    VisualCppDotNet = 5
    VisualCSharpDotNet = 6
    VisualBasicDotNet = 7
    HTBasic = 8
    LabVIEWNXG = 9


class CustomPostStepUIMsgOption(IntEnum):
    NoneValue = 0
    SuppressIfTraceSent = 1
    AppliesToAllThreads = 2


class LoopType(IntEnum):
    NoLooping = 0
    FixedNumber = 1
    While = 2
    For = 3
    ForEach = 4


class ModuleAdapter(IntEnum):
    DLL = 0
    LabVIEW = 1
    DotNet = 2


class LVStepAdditions:
    LVStep_ModulePathProp = "ViPath"
    LVStep_PassInBufProp = "PassInBuf"
    LVStep_PassInvocInfoProp = "PassInvocInfo"
    LVStep_PassContextPtrProp = "PassContextPtr"
    LVStep_ShowFrntPnlProp = "ShowFrntPnl"


class PostActionValues:
    Break = "Break"
    CallCallback = "Cback"
    GotoStep = "Goto"
    NoneValue = "None"
    Terminate = "Term"


class SeqCallMultithreadOption(IntEnum):
    NewExecution = 2
    NewThread = 1
    NoneValue = 0
    Remote = 256


class SeqCallTraceSetting(IntEnum):
    UseCurrent = 1
    Enable = 2
    Disable = 3
    UseExecutionSetting = 4


class SequenceCallStepAdditions:
    SeqCallStep_ActualArgsProp = "ActualArgs"
    SeqCallStep_PrototypeProp = "Prototype"
    SeqCallStep_IgnoreTerminateProp = "IgnoreTerminate"
    SeqCallStep_SFPathExprProp = "SFPathExpr"
    SeqCallStep_SFPathProp = "SFPath"
    SeqCallStep_SeqNameExprProp = "SeqNameExpr"
    SeqCallStep_SeqNameProp = "SeqName"
    SeqCallStep_SpecifyByExprProp = "SpecifyByExpr"
    SeqCallStep_TraceProp = "Trace"
    SeqCallStep_UseCurFileProp = "UseCurFile"


class SpecifyModuleOption(IntFlag):
    AllowPrototypeChanges = 0x4
    NoneValue = 0x0
    NoParameterLogging = 0x10


class SpecifyStepsByUniqueIdOption(IntEnum):
    Ask = 1
    No = 3
    Yes = 2


class TimeLimitAction(IntEnum):
    Abort = 0
    KillThreads = 1
    Prompt = 2
    Terminate = 3


class TimeLimitOperation(IntEnum):
    Aborting = 2
    Executing = 0
    Terminating = 1


class TimeLimitType(IntEnum):
    Exiting = 1
    NormalExecution = 0


class UpdateModuleFromStepOption(IntFlag):
    CopyParameterDefaultCheckState = 2
    CopyParameterLogCheckState = 4
    CopyParameterValue = 1
    CopyShowFrontPanelState = 8
    CopyStepRTEState = 16
    NoneValue = 0


class CVIStepAdditions(str, Enum):
    def __str__(self) -> str:
        return str(self.value)

    CVIStep_FunctionNameProp = "FuncName"
    CVIStep_FunctionPrototypeProp = "FuncProto"
    CVIStep_ModulePathProp = "ModulePath"
    CVIStep_ModulePrjPathProp = "ModulePrjPath"
    CVIStep_ModuleSrcPathProp = "ModuleSrcPath"
    CVIStep_ModuleTypeProp = "ModuleType"
    CVIStep_ParamsStringProp = "ExtProtoParams"
    CVIStep_SeqContextPassProp = "SeqContextType"


class SwitchExecLifetime(IntEnum):
    Execution = 1
    Manual = 0
    Sequence = 3
    Step = 4


class SwitchExecMulticonnectMode(IntEnum):
    Default = -1
    Multiconnect = 1
    NoMulticonnect = 0


class SwitchExecOperationOrder(IntEnum):
    DisconnectAfterConnect = 2
    DisconnectBeforeConnect = 1


if TYPE_CHECKING:
    from py_teststand.core.engine import Engine
    from py_teststand.execution.additional_results import AdditionalResults
    from py_teststand.execution.execution import Execution
    from py_teststand.property.property_object import PropertyObject
    from py_teststand.sequence.sequence import Sequence
    from py_teststand.sequence.sequence_file import ModuleLoadOption, ModuleUnloadOption
    from py_teststand.sequence.step_type import StepType

    ModuleType = typing.Any
else:
    ModuleType = typing.Any


class Step(COMWrapper):
    def __init__(self, com_obj: COM, engine: Engine | typing.Any | None = None) -> None:

        super().__init__(com_obj, engine)

    @property
    @ts_interface
    def name(self) -> typing.Any:
        return str(self._com_obj.Name)

    @name.setter
    @ts_interface
    def name(self, value: str) -> None:
        self._com_obj.Name = value

    @property
    @ts_interface
    def step_type(self) -> StepType | None:
        from py_teststand.sequence.step_type import StepType

        st_com = self._com_obj.StepType
        return StepType(st_com) if st_com else None

    @functools.cached_property
    @ts_interface
    def step_type_name(self) -> str:
        return str(self._com_obj.StepType.Name)

    @functools.cached_property
    @ts_interface
    def unique_id(self) -> str:
        return str(self._com_obj.UniqueStepId)

    @property
    @ts_interface
    def step_index(self) -> int:
        return int(self._com_obj.StepIndex)

    @property
    def index(self) -> int:

        return self.step_index

    @property
    @ts_interface
    def can_specify_module(self) -> bool:
        return bool(self._com_obj.CanSpecifyModule)

    @property
    @ts_interface
    def can_create_code(self) -> bool:
        return bool(self._com_obj.CanCreateCode)

    @property
    @ts_interface
    def window_activation(self) -> typing.Any:
        return int(self._com_obj.WindowActivation)

    @window_activation.setter
    @ts_interface
    def window_activation(self, value: int) -> None:
        self._com_obj.WindowActivation = value

    @property
    @ts_interface
    def can_edit_code(self) -> bool:
        return bool(self._com_obj.CanEditCode)

    @property
    @ts_interface
    def custom_action_expression(self) -> str:
        return str(self._com_obj.CustomActionExpression)

    @custom_action_expression.setter
    @ts_interface
    def custom_action_expression(self, value: str) -> None:
        self._com_obj.CustomActionExpression = value

    @property
    @ts_interface
    def custom_false_action(self) -> str:
        return str(self._com_obj.CustomFalseAction)

    @custom_false_action.setter
    @ts_interface
    def custom_false_action(self, value: str) -> None:
        self._com_obj.CustomFalseAction = value

    @property
    @ts_interface
    def custom_false_action_target(self) -> str:
        return str(self._com_obj.CustomFalseActionTarget)

    @custom_false_action_target.setter
    @ts_interface
    def custom_false_action_target(self, value: str) -> None:
        self._com_obj.CustomFalseActionTarget = value

    @property
    @ts_interface
    def custom_false_action_target_by_expr(self) -> str:
        return str(self._com_obj.CustomFalseActionTargetByExpr)

    @custom_false_action_target_by_expr.setter
    @ts_interface
    def custom_false_action_target_by_expr(self, value: str) -> None:
        self._com_obj.CustomFalseActionTargetByExpr = value

    @property
    @ts_interface
    def custom_true_action(self) -> str:
        return str(self._com_obj.CustomTrueAction)

    @custom_true_action.setter
    @ts_interface
    def custom_true_action(self, value: str) -> None:
        self._com_obj.CustomTrueAction = value

    @property
    @ts_interface
    def custom_true_action_target(self) -> str:
        return str(self._com_obj.CustomTrueActionTarget)

    @custom_true_action_target.setter
    @ts_interface
    def custom_true_action_target(self, value: str) -> None:
        self._com_obj.CustomTrueActionTarget = value

    @property
    @ts_interface
    def custom_true_action_target_by_expr(self) -> str:
        return str(self._com_obj.CustomTrueActionTargetByExpr)

    @custom_true_action_target_by_expr.setter
    @ts_interface
    def custom_true_action_target_by_expr(self, value: str) -> None:
        self._com_obj.CustomTrueActionTargetByExpr = value

    @property
    def expression(self) -> str:

        return self.custom_action_expression

    @expression.setter
    def expression(self, value: str) -> None:

        self.custom_action_expression = value

    @classmethod
    def create(cls, engine: Engine | typing.Any, adapter_name: str, step_type_name: str) -> Step:

        raw_engine = getattr(engine, "_engine", engine)
        raw_step = raw_engine.NewStep(adapter_name, step_type_name)
        return cls(raw_step, engine)

    @property
    @ts_interface
    def step_group(self) -> typing.Any:

        return StepGroup(int(self._com_obj.StepGroup))

    @property
    @ts_interface
    def description(self) -> str:
        return str(self._com_obj.Description)

    @ts_interface
    def get_description_ex(self, options: int = 0) -> typing.Any:
        return str(self._com_obj.GetDescriptionEx(options))

    @property
    @ts_interface
    def comment(self) -> str:
        return str(self._com_obj.Comment)

    @comment.setter
    @ts_interface
    def comment(self, value: str) -> None:
        self._com_obj.Comment = value

    @property
    @ts_interface
    def result_status(self) -> str:
        return str(self._com_obj.ResultStatus)

    @result_status.setter
    @ts_interface
    def result_status(self, value: str) -> None:
        self._com_obj.ResultStatus = value

    @ts_interface
    def get_result_status_display_string(self) -> str:
        return str(self._com_obj.GetResultStatusDisplayString())

    @ts_interface
    def get_step_settings_string(self) -> typing.Any:
        return str(self._com_obj.GetStepSettingsString())

    @property
    @ts_interface
    def run_mode(self) -> RunMode:

        val = self._com_obj.RunMode
        if isinstance(val, str):
            try:
                return RunMode[f"{val}"]
            except KeyError:
                pass
        return RunMode(int(val))

    @run_mode.setter
    @ts_interface
    def run_mode(self, value: RunMode | int | str) -> None:
        if isinstance(value, RunMode):
            self._com_obj.RunMode = value.name.replace("", "")
        else:
            self._com_obj.RunMode = value

    @property
    @ts_interface
    def runtime_run_mode(self) -> str:
        return str(self._com_obj.RunTimeRunMode)

    @runtime_run_mode.setter
    @ts_interface
    def runtime_run_mode(self, value: str) -> None:
        self._com_obj.RunTimeRunMode = value

    @ts_interface
    def reset(self) -> None:
        self._com_obj.Reset()

    @property
    @ts_interface
    def interactive_args(self) -> typing.Any:
        from py_teststand.execution.interactive_args import InteractiveArgs

        return InteractiveArgs(self._com_obj.InteractiveArgs, self.engine)

    @property
    @ts_interface
    def break_on_step(self) -> bool:
        return bool(self._com_obj.BreakOnStep)

    @break_on_step.setter
    @ts_interface
    def break_on_step(self, value: bool) -> None:
        self._com_obj.BreakOnStep = value

    @property
    @ts_interface
    def ignore_rte(self) -> bool:
        return bool(self._com_obj.IgnoreRTE)

    @ignore_rte.setter
    @ts_interface
    def ignore_rte(self, value: bool) -> None:
        self._com_obj.IgnoreRTE = value

    @property
    @ts_interface
    def cancel_current_execution(self) -> bool:
        return bool(self._com_obj.CancelCurrentExecution)

    @cancel_current_execution.setter
    @ts_interface
    def cancel_current_execution(self, value: bool) -> None:
        self._com_obj.CancelCurrentExecution = value

    @property
    @ts_interface
    def cancel_current_module_execution(self) -> bool:
        return bool(self._com_obj.CancelCurrentModuleExecution)

    @cancel_current_module_execution.setter
    @ts_interface
    def cancel_current_module_execution(self, value: bool) -> None:
        self._com_obj.CancelCurrentModuleExecution = value

    @property
    @ts_interface
    def cancel_step_callback(self) -> bool:
        return bool(self._com_obj.CancelStepCallback)

    @cancel_step_callback.setter
    @ts_interface
    def cancel_step_callback(self, value: bool) -> None:
        self._com_obj.CancelStepCallback = value

    @property
    @ts_interface
    def block_level(self) -> int:
        return int(self._com_obj.BlockLevel)

    @property
    @ts_interface
    def block_levels_unmatched(self) -> int:
        return int(self._com_obj.BlockLevelsUnmatched)

    @property
    @ts_interface
    def block_start_index(self) -> int:
        return int(self._com_obj.BlockStartIndex)

    @property
    @ts_interface
    def block_previous_index(self) -> int:
        return int(self._com_obj.BlockPreviousIndex)

    @property
    @ts_interface
    def block_end_index(self) -> int:
        return int(self._com_obj.BlockEndIndex)

    @property
    @ts_interface
    def block_next_index(self) -> int:
        return int(self._com_obj.BlockNextIndex)

    @property
    @ts_interface
    def block_parent_index(self) -> int:
        return int(self._com_obj.BlockParentIndex)

    @property
    @ts_interface
    def block_flags(self) -> BlockFlag:

        return BlockFlag(int(self._com_obj.BlockFlag))

    @block_flags.setter
    @ts_interface
    def block_flags(self, value: BlockFlag | int) -> None:
        self._com_obj.BlockFlag = int(value)

    @property
    @ts_interface
    def precondition(self) -> typing.Any:
        return str(self._com_obj.Precondition)

    @precondition.setter
    @ts_interface
    def precondition(self, value: str) -> None:
        self._com_obj.Precondition = value

    @property
    @ts_interface
    def pre_expression(self) -> str:
        return str(self._com_obj.PreExpression)

    @pre_expression.setter
    @ts_interface
    def pre_expression(self, value: str) -> None:
        self._com_obj.PreExpression = value

    @property
    @ts_interface
    def post_expression(self) -> str:
        return str(self._com_obj.PostExpression)

    @post_expression.setter
    @ts_interface
    def post_expression(self, value: str) -> None:
        self._com_obj.PostExpression = value

    @property
    @ts_interface
    def postcondition(self) -> str:
        return str(self._com_obj.Postcondition)

    @postcondition.setter
    @ts_interface
    def postcondition(self, value: str) -> None:
        self._com_obj.Postcondition = value

    @property
    @ts_interface
    def status_expression(self) -> str:
        return str(self._com_obj.StatusExpression)

    @status_expression.setter
    @ts_interface
    def status_expression(self, value: str) -> None:
        self._com_obj.StatusExpression = value

    @property
    @ts_interface
    def eval_precond_for_interactive_execution(self) -> typing.Any:

        return EvalPrecondOption(int(self._com_obj.EvalPrecondForInteractiveExecution))

    @eval_precond_for_interactive_execution.setter
    @ts_interface
    def eval_precond_for_interactive_execution(self, value: EvalPrecondOption | int) -> None:
        self._com_obj.EvalPrecondForInteractiveExecution = int(value)

    @property
    @ts_interface
    def record_result(self) -> bool:
        return bool(self._com_obj.RecordResult)

    @record_result.setter
    @ts_interface
    def record_result(self, value: bool) -> None:
        self._com_obj.RecordResult = value

    @property
    @ts_interface
    def result_recording_option(self) -> typing.Any:

        return ResultRecordingOption(int(self._com_obj.ResultRecordingOption))

    @result_recording_option.setter
    @ts_interface
    def result_recording_option(self, value: ResultRecordingOption | int) -> None:
        self._com_obj.ResultRecordingOption = int(value)

    @property
    @ts_interface
    def batch_sync_option(self) -> typing.Any:
        from py_teststand.execution.sync_manager import BatchSynchronization

        return BatchSynchronization(int(self._com_obj.BatchSyncOption))

    @batch_sync_option.setter
    @ts_interface
    def batch_sync_option(self, value: int) -> None:
        self._com_obj.BatchSyncOption = int(value)

    @property
    @ts_interface
    def use_mutex(self) -> bool:
        return bool(self._com_obj.UseMutex)

    @use_mutex.setter
    @ts_interface
    def use_mutex(self, value: bool) -> None:
        self._com_obj.UseMutex = value

    @property
    @ts_interface
    def mutex_name_or_ref_expr(self) -> str:
        return str(self._com_obj.MutexNameOrRefExpr)

    @mutex_name_or_ref_expr.setter
    @ts_interface
    def mutex_name_or_ref_expr(self, value: str) -> None:
        self._com_obj.MutexNameOrRefExpr = value

    @property
    @ts_interface
    def switch_exec_enabled(self) -> bool:
        return bool(self._com_obj.SwitchExecEnabled)

    @switch_exec_enabled.setter
    @ts_interface
    def switch_exec_enabled(self, value: bool) -> None:
        self._com_obj.SwitchExecEnabled = value

    @property
    @ts_interface
    def switch_exec_connection_lifetime(self) -> typing.Any:
        return int(self._com_obj.SwitchExecConnectionLifetime)

    @switch_exec_connection_lifetime.setter
    @ts_interface
    def switch_exec_connection_lifetime(self, value: int) -> None:
        self._com_obj.SwitchExecConnectionLifetime = value

    @property
    @ts_interface
    def switch_exec_enabled(self) -> bool:
        return bool(self._com_obj.SwitchExecEnabled)

    @switch_exec_enabled.setter
    @ts_interface
    def switch_exec_enabled(self, value: bool) -> None:
        self._com_obj.SwitchExecEnabled = value

    @property
    @ts_interface
    def switch_exec_virtual_device(self) -> str:
        return str(self._com_obj.SwitchExecVirtualDevice)

    @switch_exec_virtual_device.setter
    @ts_interface
    def switch_exec_virtual_device(self, value: str) -> None:
        self._com_obj.SwitchExecVirtualDevice = value

    @property
    @ts_interface
    def switch_exec_multiconnect_mode(self) -> typing.Any:
        return int(self._com_obj.SwitchExecMulticonnectMode)

    @switch_exec_multiconnect_mode.setter
    @ts_interface
    def switch_exec_multiconnect_mode(self, value: int) -> None:
        self._com_obj.SwitchExecMulticonnectMode = value

    @property
    @ts_interface
    def switch_exec_operation_order(self) -> typing.Any:
        return int(self._com_obj.SwitchExecOperationOrder)

    @switch_exec_operation_order.setter
    @ts_interface
    def switch_exec_operation_order(self, value: int) -> None:
        self._com_obj.SwitchExecOperationOrder = value

    @property
    @ts_interface
    def switch_exec_routes_to_connect(self) -> str:
        return str(self._com_obj.SwitchExecRoutesToConnect)

    @switch_exec_routes_to_connect.setter
    @ts_interface
    def switch_exec_routes_to_connect(self, value: str) -> None:
        self._com_obj.SwitchExecRoutesToConnect = value

    @property
    @ts_interface
    def switch_exec_routes_to_disconnect(self) -> str:
        return str(self._com_obj.SwitchExecRoutesToDisconnect)

    @switch_exec_routes_to_disconnect.setter
    @ts_interface
    def switch_exec_routes_to_disconnect(self, value: str) -> None:
        self._com_obj.SwitchExecRoutesToDisconnect = value

    @property
    @ts_interface
    def switch_exec_wait_for_debounce(self) -> bool:
        return bool(self._com_obj.SwitchExecWaitForDebounce)

    @switch_exec_wait_for_debounce.setter
    @ts_interface
    def switch_exec_wait_for_debounce(self, value: bool) -> None:
        self._com_obj.SwitchExecWaitForDebounce = value

    @property
    @ts_interface
    def switch_exec_operation(self) -> typing.Any:
        return SwitchExecOperation(int(self._com_obj.SwitchExecOperation))

    @switch_exec_operation.setter
    @ts_interface
    def switch_exec_operation(self, value: SwitchExecOperation) -> None:
        self._com_obj.SwitchExecOperation = int(value)

    @property
    @ts_interface
    def switch_exec_routes_to_connect(self) -> str:
        return str(self._com_obj.SwitchExecRoutesToConnect)

    @switch_exec_routes_to_connect.setter
    @ts_interface
    def switch_exec_routes_to_connect(self, value: str) -> None:
        self._com_obj.SwitchExecRoutesToConnect = value

    @property
    @ts_interface
    def switch_exec_routes_to_disconnect(self) -> str:
        return str(self._com_obj.SwitchExecRoutesToDisconnect)

    @switch_exec_routes_to_disconnect.setter
    @ts_interface
    def switch_exec_routes_to_disconnect(self, value: str) -> None:
        self._com_obj.SwitchExecRoutesToDisconnect = value

    @property
    @ts_interface
    def module(self) -> typing.Any:
        from py_teststand.adapters.adapter import Module

        return Module(self._com_obj.Module, self.engine)

    @ts_interface
    def specify_module(self, options: int = 0) -> typing.Any:
        self._com_obj.SpecifyModule(options)

    @ts_interface
    def load_module(self) -> typing.Any:
        self._com_obj.LoadModule()

    @ts_interface
    def unload_module(self) -> None:
        self._com_obj.UnloadModule()

    @property
    @ts_interface
    def module_load_option(self) -> typing.Any:
        from py_teststand.sequence.sequence_file import ModuleLoadOption

        return ModuleLoadOption(int(self._com_obj.ModuleLoadOption))

    @module_load_option.setter
    @ts_interface
    def module_load_option(self, value: ModuleLoadOption | int) -> None:
        self._com_obj.ModuleLoadOption = int(value)

    @property
    @ts_interface
    def module_unload_option(self) -> typing.Any:
        from py_teststand.sequence.sequence_file import ModuleUnloadOption

        return ModuleUnloadOption(int(self._com_obj.ModuleUnloadOption))

    @module_unload_option.setter
    @ts_interface
    def module_unload_option(self, value: ModuleUnloadOption | int) -> None:
        self._com_obj.ModuleUnloadOption = int(value)

    @property
    @ts_interface
    def adapter_key_name(self) -> str:
        return str(self._com_obj.AdapterKeyName)

    @property
    def adapter_module(self) -> Module | typing.Any:
        adapter_key = self._com_obj.AdapterKeyName
        from py_teststand.adapters.adapter import Module

        if adapter_key and self.engine:
            try:
                ts_adapter = self.engine.get_adapter_by_key_name(adapter_key)
                if ts_adapter:
                    return ts_adapter.module
            except Exception:
                pass
        return Module(self._com_obj.Module, self.engine)

    @property
    @ts_interface
    def loop_type(self) -> str:
        return str(self._com_obj.LoopType)

    @loop_type.setter
    @ts_interface
    def loop_type(self, value: str) -> None:
        self._com_obj.LoopType = value

    @property
    @ts_interface
    def loop_inc_expression(self) -> str:
        return str(self._com_obj.LoopIncExpression)

    @loop_inc_expression.setter
    @ts_interface
    def loop_inc_expression(self, value: str) -> None:
        self._com_obj.LoopIncExpression = value

    @property
    @ts_interface
    def loop_init_expression(self) -> str:
        return str(self._com_obj.LoopInitExpression)

    @loop_init_expression.setter
    @ts_interface
    def loop_init_expression(self, value: str) -> None:
        self._com_obj.LoopInitExpression = value

    @property
    @ts_interface
    def loop_while_expression(self) -> str:
        return str(self._com_obj.LoopWhileExpression)

    @loop_while_expression.setter
    @ts_interface
    def loop_while_expression(self, value: str) -> None:
        self._com_obj.LoopWhileExpression = value

    @property
    @ts_interface
    def loop_status_expression(self) -> str:
        return str(self._com_obj.LoopStatusExpression)

    @loop_status_expression.setter
    @ts_interface
    def loop_status_expression(self, value: str) -> None:
        self._com_obj.LoopStatusExpression = value

    @property
    @ts_interface
    def record_loop_iteration_results(self) -> bool:
        return bool(self._com_obj.RecordLoopIterationResults)

    @record_loop_iteration_results.setter
    @ts_interface
    def record_loop_iteration_results(self, value: bool) -> None:
        self._com_obj.RecordLoopIterationResults = value

    @property
    @ts_interface
    def caused_sequence_failure(self) -> bool:
        return bool(self._com_obj.CausedSequenceFailure)

    @caused_sequence_failure.setter
    @ts_interface
    def caused_sequence_failure(self, value: bool) -> None:
        self._com_obj.CausedSequenceFailure = value

    @property
    @ts_interface
    def step_fail_causes_sequence_fail(self) -> bool:
        return bool(self._com_obj.StepFailCausesSequenceFail)

    @step_fail_causes_sequence_fail.setter
    @ts_interface
    def step_fail_causes_sequence_fail(self, value: bool) -> None:
        self._com_obj.StepFailCausesSequenceFail = value

    @property
    @ts_interface
    def is_sequence_call(self) -> bool:
        return bool(self._com_obj.IsSequenceCall)

    @property
    @ts_interface
    def additional_results(self) -> AdditionalResults:
        from py_teststand.execution.additional_results import AdditionalResults

        return AdditionalResults(self._com_obj.AdditionalResults, self.engine)

    @property
    @ts_interface
    def additional_results_hints(self) -> AdditionalResults:
        from py_teststand.execution.additional_results import AdditionalResults

        return AdditionalResults(self._com_obj.AdditionalResultsHints, self.engine)

    @property
    @ts_interface
    def requirements(self) -> typing.Any:
        return list(self._com_obj.Requirements)

    @property
    @ts_interface
    def sequence(self) -> Sequence | None:
        from py_teststand.sequence.sequence import Sequence

        com_obj = self._com_obj.Sequence
        return Sequence(com_obj, self._engine_ref) if com_obj else None

    @requirements.setter
    @ts_interface
    def requirements(self, value: list[str]) -> None:
        self._com_obj.Requirements = value

    @ts_interface
    def can_change_adapter(self, adapter_key_name: str) -> typing.Any:
        return bool(self._com_obj.CanChangeAdapter(adapter_key_name))

    @ts_interface
    def change_adapter(self, adapter_key_name: str) -> typing.Any:
        self._com_obj.ChangeAdapter(adapter_key_name)

    @ts_interface
    def can_change_step_type(self, step_type_name: str) -> typing.Any:
        return bool(self._com_obj.CanChangeStepType(step_type_name))

    @ts_interface
    def change_step_type(self, step_type_name: str) -> typing.Any:
        self._com_obj.ChangeStepType(step_type_name)

    @ts_interface
    def edit_code(self) -> None:
        self._com_obj.EditCode()

    @ts_interface
    def create_new_unique_step_id(self) -> None:
        self._com_obj.CreateNewUniqueStepId()

    @ts_interface
    def display_additional_results_dialog(
        self, title: str = "", read_only: bool = False
    ) -> typing.Any:
        return bool(self._com_obj.DisplayAdditionalResultsDialog(title, read_only))

    @property
    @ts_interface
    def edit_as_read_only(self) -> bool:
        return bool(self._com_obj.EditAsReadOnly)

    @edit_as_read_only.setter
    @ts_interface
    def edit_as_read_only(self, value: bool) -> None:
        self._com_obj.EditAsReadOnly = value

    @ts_interface
    def get_execution_flow_string(self) -> typing.Any:
        return str(self._com_obj.GetExecutionFlowString())

    @ts_interface
    def log_additional_result(self, result_name: str, result_value: typing.Any) -> typing.Any:
        self._com_obj.LogAdditionalResult(result_name, result_value)

    @ts_interface
    def load_prototype(self) -> None:
        self._com_obj.LoadPrototype()

    @ts_interface
    def as_property_object(self) -> PropertyObject:
        from py_teststand.property.property_object import PropertyObject

        return PropertyObject(self._com_obj.AsPropertyObject(), self._engine_ref)

    @ts_interface
    def can_execute_substep(self, substep_index: int) -> typing.Any:
        return bool(self._com_obj.CanExecuteSubstep(substep_index))

    @property
    @ts_interface
    def can_execute_edit_substep(self) -> bool:
        return bool(self._com_obj.CanExecuteEditSubstep)

    @property
    @ts_interface
    def current_loop_result(self) -> typing.Any:
        from py_teststand.property.property_object import PropertyObject

        com_obj = self._com_obj.CurrentLoopResult
        return PropertyObject(com_obj, self._engine_ref) if com_obj else None

    @property
    @ts_interface
    def last_step_result(self) -> typing.Any:
        from py_teststand.property.property_object import PropertyObject

        com_obj = self._com_obj.LastStepResult
        return PropertyObject(com_obj, self._engine_ref) if com_obj else None

    @ts_interface
    def create_code(self) -> None:
        self._com_obj.CreateCode()

    @ts_interface
    def execute_edit_substep(self, substep_index: int) -> None:
        self._com_obj.ExecuteEditSubstep(substep_index)

    @ts_interface
    def execute_substep(self, substep_index: int) -> typing.Any:
        self._com_obj.ExecuteSubstep(substep_index)

    @ts_interface
    def get_break_on_step_ex(self, execution: Execution | typing.Any) -> typing.Any:
        exec_com = getattr(execution, "_com_obj", execution)
        return bool(self._com_obj.GetBreakOnStepEx(exec_com))

    @ts_interface
    def set_break_on_step_ex(self, execution: Execution | typing.Any, value: bool) -> typing.Any:
        exec_com = getattr(execution, "_com_obj", execution)
        self._com_obj.SetBreakOnStepEx(exec_com, value)

    @ts_interface
    def get_break_settings(
        self, execution: Execution | typing.Any = None
    ) -> tuple[bool, bool, int, str]:
        exec_com = getattr(execution, "_com_obj", execution) if execution else None
        return self._com_obj.GetBreakSettings(None, None, None, None, exec_com)

    @ts_interface
    def set_break_settings(
        self,
        is_set: bool,
        enabled: bool,
        pass_count: int,
        condition: str,
        execution: Execution | typing.Any = None,
    ) -> None:
        exec_com = getattr(execution, "_com_obj", execution) if execution else None
        self._com_obj.SetBreakSettings(is_set, enabled, pass_count, condition, exec_com)

    @ts_interface
    def get_run_mode_ex(self, execution: Execution | typing.Any) -> str:
        exec_com = getattr(execution, "_com_obj", execution)
        return str(self._com_obj.GetRunModeEx(exec_com))

    @ts_interface
    def set_run_mode_ex(self, run_mode: str, execution: Execution | typing.Any = None) -> None:
        exec_com = getattr(execution, "_com_obj", execution) if execution else None
        self._com_obj.SetRunModeEx(str(run_mode), exec_com)

    @ts_interface
    def get_edit_substep_menu_structure(self) -> PropertyObject | None:
        from py_teststand.property.property_object import PropertyObject

        com_obj = self._com_obj.GetEditSubstepMenuStructure()
        return PropertyObject(com_obj, self.engine) if com_obj else None

    @property
    @ts_interface
    def num_substeps(self) -> int:
        return int(self._com_obj.NumSubsteps)

    @property
    @ts_interface
    def icon_name(self) -> str:
        return str(self._com_obj.IconName)

    @icon_name.setter
    @ts_interface
    def icon_name(self, value: str) -> None:
        self._com_obj.IconName = value

    @property
    @ts_interface
    def large_icon(self) -> typing.Any:
        return self._com_obj.LargeIcon

    @property
    @ts_interface
    def small_icon(self) -> typing.Any:
        return self._com_obj.SmallIcon

    @property
    @ts_interface
    def small_icon_index(self) -> int:
        return int(self._com_obj.SmallIconIndex)

    @ts_interface
    def add_substep(self, name: str, index: int, type: int) -> None:
        self._com_obj.AddSubstep(name, index, type)

    @ts_interface
    def remove_substep(self, index: int) -> None:
        self._com_obj.RemoveSubstep(index)

    @ts_interface
    def get_substep(self, index: int) -> Step:
        return Step(self._com_obj.GetSubstep(index), self.engine)

    @ts_interface
    def swap_substeps(self, index1: int, index2: int) -> None:
        self._com_obj.SwapSubsteps(index1, index2)

    @property
    @ts_interface
    def pass_action(self) -> str:
        return str(self._com_obj.PassAction)

    @pass_action.setter
    @ts_interface
    def pass_action(self, value: str) -> None:
        self._com_obj.PassAction = value

    @property
    @ts_interface
    def pass_action_target(self) -> str:
        return str(self._com_obj.PassActionTarget)

    @pass_action_target.setter
    @ts_interface
    def pass_action_target(self, value: str) -> None:
        self._com_obj.PassActionTarget = value

    @property
    @ts_interface
    def pass_action_target_by_expr(self) -> typing.Any:
        return str(self._com_obj.PassActionTargetByExpr)

    @pass_action_target_by_expr.setter
    @ts_interface
    def pass_action_target_by_expr(self, value: str) -> None:
        self._com_obj.PassActionTargetByExpr = value

    @property
    @ts_interface
    def fail_action(self) -> str:
        return str(self._com_obj.FailAction)

    @fail_action.setter
    @ts_interface
    def fail_action(self, value: str) -> None:
        self._com_obj.FailAction = value

    @property
    @ts_interface
    def fail_action_target(self) -> str:
        return str(self._com_obj.FailActionTarget)

    @fail_action_target.setter
    @ts_interface
    def fail_action_target(self, value: str) -> None:
        self._com_obj.FailActionTarget = value

    @property
    @ts_interface
    def fail_action_target_by_expr(self) -> typing.Any:
        return str(self._com_obj.FailActionTargetByExpr)

    @fail_action_target_by_expr.setter
    @ts_interface
    def fail_action_target_by_expr(self, value: str) -> None:
        self._com_obj.FailActionTargetByExpr = value

    @property
    @ts_interface
    def custom_true_action(self) -> str:
        return str(self._com_obj.CustomTrueAction)

    @custom_true_action.setter
    @ts_interface
    def custom_true_action(self, value: str) -> None:
        self._com_obj.CustomTrueAction = value

    @property
    @ts_interface
    def custom_true_action_target(self) -> str:
        return str(self._com_obj.CustomTrueActionTarget)

    @custom_true_action_target.setter
    @ts_interface
    def custom_true_action_target(self, value: str) -> None:
        self._com_obj.CustomTrueActionTarget = value

    @property
    @ts_interface
    def custom_false_action(self) -> str:
        return str(self._com_obj.CustomFalseAction)

    @custom_false_action.setter
    @ts_interface
    def custom_false_action(self, value: str) -> None:
        self._com_obj.CustomFalseAction = value

    @property
    @ts_interface
    def custom_false_action_target(self) -> str:
        return str(self._com_obj.CustomFalseActionTarget)

    @custom_false_action_target.setter
    @ts_interface
    def custom_false_action_target(self, value: str) -> None:
        self._com_obj.CustomFalseActionTarget = value

    @property
    @ts_interface
    def large_icon_index(self) -> typing.Any:

        return self._com_obj.LargeIconIndex

    @large_icon_index.setter
    @ts_interface
    def large_icon_index(self, value: typing.Any) -> None:
        self._com_obj.LargeIconIndex = value

    @property
    @ts_interface
    def run_time_run_mode(self) -> typing.Any:

        return self._com_obj.RunTimeRunMode

    @run_time_run_mode.setter
    @ts_interface
    def run_time_run_mode(self, value: typing.Any) -> None:
        self._com_obj.RunTimeRunMode = value

    @property
    @ts_interface
    def unique_step_id(self) -> typing.Any:

        return self._com_obj.UniqueStepId

    @unique_step_id.setter
    @ts_interface
    def unique_step_id(self, value: typing.Any) -> None:
        self._com_obj.UniqueStepId = value
