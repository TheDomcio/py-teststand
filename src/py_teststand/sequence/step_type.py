from __future__ import annotations

import typing
from enum import IntEnum
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import ts_interface
from py_teststand.execution.sync_manager import BatchSynchronization
from py_teststand.property.property_object import PropertyObject


class SwitchExecOperation(IntEnum):
    Connect = 1
    Disconnect = 2
    DisconnectAll = 3
    ConnectDisconnect = 4


if TYPE_CHECKING:
    from py_teststand.execution.additional_results import AdditionalResults
    from py_teststand.sequence.sequence_file import ModuleLoadOption, ModuleUnloadOption
    from py_teststand.sequence.step import EvalPrecondOption, ResultRecordingOption, Step


class StepType(PropertyObject):
    def __init__(self, com_obj: typing.Any, engine_ref: typing.Any = None) -> None:

        super().__init__(com_obj, engine_ref)

    @property
    @ts_interface
    def as_property_object(self) -> PropertyObject:
        return PropertyObject(self._com_obj, self._engine_ref)

    @property
    @ts_interface
    def designated_adapter_key_name(self) -> str:
        return str(self._com_obj.DesignatedAdapter)

    @property
    @ts_interface
    def can_specify_module(self) -> bool:
        return bool(self._com_obj.CanSpecifyModule)

    @property
    @ts_interface
    def batch_sync_option(self) -> typing.Any:

        return BatchSynchronization(int(self._com_obj.BatchSyncOption))

    @batch_sync_option.setter
    @ts_interface
    def batch_sync_option(self, value: int) -> None:
        self._com_obj.BatchSyncOption = int(value)

    @property
    @ts_interface
    def can_encapsulate(self) -> bool:
        return bool(self._com_obj.CanEncapsulate)

    @property
    @ts_interface
    def applies_to_block_structure(self) -> bool:
        return bool(self._com_obj.AppliesToBlockStructure)

    @applies_to_block_structure.setter
    @ts_interface
    def applies_to_block_structure(self, value: bool) -> None:
        self._com_obj.AppliesToBlockStructure = value

    @property
    @ts_interface
    def block_end_types(self) -> str:
        return str(self._com_obj.BlockEndTypes)

    @block_end_types.setter
    @ts_interface
    def block_end_types(self, value: str) -> None:
        self._com_obj.BlockEndTypes = value

    @property
    @ts_interface
    def block_start_types(self) -> str:
        return str(self._com_obj.BlockStartTypes)

    @block_start_types.setter
    @ts_interface
    def block_start_types(self, value: str) -> None:
        self._com_obj.BlockStartTypes = value

    @property
    @ts_interface
    def icon_name(self) -> str:
        return str(self._com_obj.IconName)

    @property
    @ts_interface
    def description_expr(self) -> str:
        return str(self._com_obj.DescriptionExpr)

    @description_expr.setter
    @ts_interface
    def description_expr(self, value: str) -> None:
        self._com_obj.DescriptionExpr = value

    @property
    @ts_interface
    def default_name_expr(self) -> str:
        return str(self._com_obj.DefaultNameExpr)

    @default_name_expr.setter
    @ts_interface
    def default_name_expr(self, value: str) -> None:
        self._com_obj.DefaultNameExpr = value

    @property
    @ts_interface
    def category(self) -> int:
        return int(self._com_obj.Category)

    @property
    @ts_interface
    def name(self) -> str:
        return str(self._com_obj.Name)

    @name.setter
    @ts_interface
    def name(self, value: str) -> None:
        self._com_obj.Name = value

    @property
    @ts_interface
    def dimmable_property_key_names(self) -> list[str]:
        return list(self._com_obj.DimmablePropertyKeyNames)

    @property
    @ts_interface
    def code_templates(self) -> PropertyObject:
        return PropertyObject(self._com_obj.CodeTemplates, self._engine_ref)

    @property
    @ts_interface
    def additional_results_hints(self) -> AdditionalResults:
        from py_teststand.execution.additional_results import AdditionalResults

        return AdditionalResults(self._com_obj.AdditionalResultsHints, self._engine_ref)

    @property
    @ts_interface
    def module(self) -> typing.Any:
        from py_teststand.adapters.adapter import Module

        return Module(self._com_obj.Module, self._engine_ref)

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
    def mutex_name_or_ref_expr(self) -> str:
        return str(self._com_obj.MutexNameOrRefExpr)

    @mutex_name_or_ref_expr.setter
    @ts_interface
    def mutex_name_or_ref_expr(self, value: str) -> None:
        self._com_obj.MutexNameOrRefExpr = value

    @property
    @ts_interface
    def num_substeps(self) -> int:
        return int(self._com_obj.NumSubsteps)

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
    def eval_precond_for_interactive_execution(self) -> typing.Any:
        from py_teststand.sequence.step import EvalPrecondOption

        return EvalPrecondOption(int(self._com_obj.EvalPrecondForInteractiveExecution))

    @eval_precond_for_interactive_execution.setter
    @ts_interface
    def eval_precond_for_interactive_execution(self, value: EvalPrecondOption | int) -> None:
        self._com_obj.EvalPrecondForInteractiveExecution = int(value)

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
    def loop_status_expression(self) -> str:
        return str(self._com_obj.LoopStatusExpression)

    @loop_status_expression.setter
    @ts_interface
    def loop_status_expression(self, value: str) -> None:
        self._com_obj.LoopStatusExpression = value

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
    def loop_while_expression(self) -> str:
        return str(self._com_obj.LoopWhileExpression)

    @loop_while_expression.setter
    @ts_interface
    def loop_while_expression(self, value: str) -> None:
        self._com_obj.LoopWhileExpression = value

    @property
    @ts_interface
    def menu_group_name(self) -> str:
        return str(self._com_obj.MenuGroupName)

    @menu_group_name.setter
    @ts_interface
    def menu_group_name(self, value: str) -> None:
        self._com_obj.MenuGroupName = value

    @property
    @ts_interface
    def menu_icon(self) -> typing.Any:
        return self._com_obj.MenuIcon

    @property
    @ts_interface
    def menu_icon_index(self) -> int:
        return int(self._com_obj.MenuIconIndex)

    @property
    @ts_interface
    def menu_item_name_expr(self) -> str:
        return str(self._com_obj.MenuItemNameExpr)

    @menu_item_name_expr.setter
    @ts_interface
    def menu_item_name_expr(self, value: str) -> None:
        self._com_obj.MenuItemNameExpr = value

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
    def fail_action_target_by_expr(self) -> str:
        return str(self._com_obj.FailActionTargetByExpr)

    @fail_action_target_by_expr.setter
    @ts_interface
    def fail_action_target_by_expr(self, value: str) -> None:
        self._com_obj.FailActionTargetByExpr = value

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
    def custom_false_action(self) -> str:
        return str(self._com_obj.CustomFalseAction)

    @custom_false_action.setter
    @ts_interface
    def custom_false_action(self, value: str) -> None:
        self._com_obj.CustomFalseAction = value

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
    def custom_true_action_target_by_expr(self) -> str:
        return str(self._com_obj.CustomTrueActionTargetByExpr)

    @custom_true_action_target_by_expr.setter
    @ts_interface
    def custom_true_action_target_by_expr(self, value: str) -> None:
        self._com_obj.CustomTrueActionTargetByExpr = value

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
    def pass_action_target_by_expr(self) -> str:
        return str(self._com_obj.PassActionTargetByExpr)

    @pass_action_target_by_expr.setter
    @ts_interface
    def pass_action_target_by_expr(self, value: str) -> None:
        self._com_obj.PassActionTargetByExpr = value

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
    def precondition(self) -> str:
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
    def record_loop_iteration_results(self) -> bool:
        return bool(self._com_obj.RecordLoopIterationResults)

    @record_loop_iteration_results.setter
    @ts_interface
    def record_loop_iteration_results(self, value: bool) -> None:
        self._com_obj.RecordLoopIterationResults = value

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
        from py_teststand.sequence.step import ResultRecordingOption

        return ResultRecordingOption(int(self._com_obj.ResultRecordingOption))

    @result_recording_option.setter
    @ts_interface
    def result_recording_option(self, value: ResultRecordingOption | int) -> None:
        self._com_obj.ResultRecordingOption = int(value)

    @property
    @ts_interface
    def run_mode(self) -> str:
        return str(self._com_obj.RunMode)

    @run_mode.setter
    @ts_interface
    def run_mode(self, value: str) -> None:
        self._com_obj.RunMode = value

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
    def step_fail_causes_sequence_fail(self) -> bool:
        return bool(self._com_obj.StepFailCausesSequenceFail)

    @step_fail_causes_sequence_fail.setter
    @ts_interface
    def step_fail_causes_sequence_fail(self, value: bool) -> None:
        self._com_obj.StepFailCausesSequenceFail = value

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
    def switch_exec_multiconnect_mode(self) -> typing.Any:
        return int(self._com_obj.SwitchExecMulticonnectMode)

    @switch_exec_multiconnect_mode.setter
    @ts_interface
    def switch_exec_multiconnect_mode(self, value: int) -> None:
        self._com_obj.SwitchExecMulticonnectMode = value

    @property
    @ts_interface
    def switch_exec_operation(self) -> typing.Any:

        return SwitchExecOperation(int(self._com_obj.SwitchExecOperation))

    @switch_exec_operation.setter
    @ts_interface
    def switch_exec_operation(self, value: SwitchExecOperation | int) -> None:
        self._com_obj.SwitchExecOperation = int(value)

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
    def switch_exec_virtual_device(self) -> str:
        return str(self._com_obj.SwitchExecVirtualDevice)

    @switch_exec_virtual_device.setter
    @ts_interface
    def switch_exec_virtual_device(self, value: str) -> None:
        self._com_obj.SwitchExecVirtualDevice = value

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
    def use_mutex(self) -> bool:
        return bool(self._com_obj.UseMutex)

    @use_mutex.setter
    @ts_interface
    def use_mutex(self, value: bool) -> None:
        self._com_obj.UseMutex = value

    @property
    @ts_interface
    def window_activation(self) -> typing.Any:
        return int(self._com_obj.WindowActivation)

    @window_activation.setter
    @ts_interface
    def window_activation(self, value: int) -> None:
        self._com_obj.WindowActivation = value

    @ts_interface
    def change_designated_adapter(self, adapter_name: str) -> typing.Any:
        self._com_obj.ChangeDesignatedAdapter(adapter_name)

    @ts_interface
    def add_substep(self, new_substep: Step) -> typing.Any:
        self._com_obj.AddSubstep(new_substep._com_obj)

    @ts_interface
    def create_combined_step_type(self, combine_with: StepType) -> typing.Any:
        return StepType(
            self._com_obj.CreateCombinedStepType(combine_with._com_obj),
            self._engine_ref,
        )

    @ts_interface
    def dim_property(self, property_key_name: str, new_value: bool) -> typing.Any:
        self._com_obj.DimProperty(property_key_name, new_value)

    @ts_interface
    def get_default_name(self) -> str:
        return str(self._com_obj.GetDefaultName())

    @ts_interface
    def get_dimmable_property_display_name(self, property_key_name: str) -> typing.Any:
        return str(self._com_obj.GetDimmablePropertyDisplayName(property_key_name))

    @ts_interface
    def get_substep(self, substep_index: int) -> typing.Any:
        from py_teststand.sequence.step import Step

        return Step(self._com_obj.GetSubstep(substep_index), self._engine_ref)

    @ts_interface
    def is_property_dimmed(self, property_key_name: str) -> typing.Any:
        return bool(self._com_obj.IsPropertyDimmed(property_key_name))

    @ts_interface
    def remove_substep(self, substep_index: int) -> typing.Any:
        self._com_obj.RemoveSubstep(substep_index)

    @ts_interface
    def specify_module(self, spec_mod_options: int = 0) -> typing.Any:
        return bool(self._com_obj.SpecifyModule(spec_mod_options))

    @ts_interface
    def swap_substeps(self, index1: int, index2: int) -> typing.Any:
        self._com_obj.SwapSubsteps(index1, index2)
