from __future__ import annotations

import typing
from enum import IntFlag

from py_teststand.adapters.adapter import Adapter, Module
from py_teststand.core.com_wrapper import ts_interface
from py_teststand.property.property_object import PropertyObject
from py_teststand.sequence.expression import EvaluationTypes
from py_teststand.sequence.sequence_file import SequenceFile


class NewThreadOption(IntFlag):
    NoneValue = 0x0
    AutoWaitAtEndOfSequence = 0x1
    InitiallySuspended = 0x2
    UseSTA = 0x4


class SequenceAdapter(Adapter):
    @ts_interface
    def as_adapter(self) -> Adapter:
        return Adapter(self._com_obj.AsAdapter(), self._engine_ref)

    @ts_interface
    def get_sequence_file(self, path: str) -> SequenceFile:
        from py_teststand.sequence.sequence_file import SequenceFile

        return SequenceFile(self._com_obj.GetSequenceFile(str(path)), self._engine_ref)


class SequenceCallModule(Module):
    def __init__(self, com_obj: typing.Any, engine: typing.Any = None) -> None:

        super().__init__(com_obj, engine)

    @property
    @ts_interface
    def cpu_affinity_for_new_thread_option(self) -> typing.Any:
        return int(self._com_obj.CPUAffinityForNewThreadOption)

    @cpu_affinity_for_new_thread_option.setter
    @ts_interface
    def cpu_affinity_for_new_thread_option(self, value: int) -> None:
        self._com_obj.CPUAffinityForNewThreadOption = int(value)

    @property
    @ts_interface
    def custom_cpu_affinity_for_new_thread(self) -> typing.Any:
        return str(self._com_obj.CustomCPUAffinityForNewThread)

    @custom_cpu_affinity_for_new_thread.setter
    @ts_interface
    def custom_cpu_affinity_for_new_thread(self, value: str) -> None:
        self._com_obj.CustomCPUAffinityForNewThread = str(value)

    @property
    @ts_interface
    def ignore_termination(self) -> bool:
        return bool(self._com_obj.IgnoreTermination)

    @ignore_termination.setter
    @ts_interface
    def ignore_termination(self, value: bool) -> None:
        self._com_obj.IgnoreTermination = bool(value)

    @property
    @ts_interface
    def initially_suspended(self) -> bool:
        return bool(self._com_obj.InitiallySuspended)

    @initially_suspended.setter
    @ts_interface
    def initially_suspended(self, value: bool) -> None:
        self._com_obj.InitiallySuspended = bool(value)

    @ts_interface
    def load_parameters(
        self,
        use_current_seq_file: bool = False,
        seq_file_path: str = "",
        seq_name: str = "",
    ) -> None:
        self._com_obj.LoadParameters(bool(use_current_seq_file), str(seq_file_path), str(seq_name))

    @ts_interface
    def load_parameters_from_sequence(self, sequence: typing.Any) -> None:
        com_seq = getattr(sequence, "_com_obj", sequence)
        self._com_obj.LoadParametersFromSequence(com_seq)

    @ts_interface
    def load_prototype_from_sequence(self, sequence: typing.Any) -> None:
        com_seq = getattr(sequence, "_com_obj", sequence)
        self._com_obj.LoadPrototypeFromSequence(com_seq)

    @property
    @ts_interface
    def multithreading_and_remote_exec_option(self) -> typing.Any:
        return int(self._com_obj.MultithreadingAndRemoteExecOption)

    @multithreading_and_remote_exec_option.setter
    @ts_interface
    def multithreading_and_remote_exec_option(self, value: int) -> None:
        self._com_obj.MultithreadingAndRemoteExecOption = int(value)

    @property
    @ts_interface
    def new_execution_break_on_entry_ex(self) -> int:
        return int(self._com_obj.NewExecutionBreakOnEntryEx)

    @new_execution_break_on_entry_ex.setter
    @ts_interface
    def new_execution_break_on_entry_ex(self, value: int) -> None:
        self._com_obj.NewExecutionBreakOnEntryEx = int(value)

    @property
    @ts_interface
    def new_execution_model_option(self) -> typing.Any:
        return int(self._com_obj.NewExecutionModelOption)

    @new_execution_model_option.setter
    @ts_interface
    def new_execution_model_option(self, value: int) -> None:
        self._com_obj.NewExecutionModelOption = int(value)

    @property
    @ts_interface
    def new_execution_model_path(self) -> str:
        return str(self._com_obj.NewExecutionModelPath)

    @new_execution_model_path.setter
    @ts_interface
    def new_execution_model_path(self, value: str) -> None:
        self._com_obj.NewExecutionModelPath = str(value)

    @property
    @ts_interface
    def new_execution_type_mask(self) -> int:
        return int(self._com_obj.NewExecutionTypeMask)

    @new_execution_type_mask.setter
    @ts_interface
    def new_execution_type_mask(self, value: int) -> None:
        self._com_obj.NewExecutionTypeMask = int(value)

    @property
    @ts_interface
    def new_execution_type_mask_expr(self) -> str:
        return str(self._com_obj.NewExecutionTypeMaskExpr)

    @new_execution_type_mask_expr.setter
    @ts_interface
    def new_execution_type_mask_expr(self, value: str) -> None:
        self._com_obj.NewExecutionTypeMaskExpr = str(value)

    @property
    @ts_interface
    def new_execution_wait_for_completion(self) -> int:
        return int(self._com_obj.NewExecutionWaitForCompletion)

    @new_execution_wait_for_completion.setter
    @ts_interface
    def new_execution_wait_for_completion(self, value: int) -> None:
        self._com_obj.NewExecutionWaitForCompletion = int(value)

    @property
    @ts_interface
    def new_thread_options(self) -> int:
        return int(self._com_obj.NewThreadOption)

    @new_thread_options.setter
    @ts_interface
    def new_thread_options(self, value: int) -> None:
        self._com_obj.NewThreadOption = int(value)

    @property
    @ts_interface
    def parameter_prototype(self) -> typing.Any:
        return self._com_obj.ParameterPrototype

    @property
    @ts_interface
    def parameters(self) -> SequenceCallParameters:
        return SequenceCallParameters(self._com_obj.Parameters, self._engine_ref)

    @property
    @ts_interface
    def remote_host(self) -> str:
        return str(self._com_obj.RemoteHost)

    @remote_host.setter
    @ts_interface
    def remote_host(self, value: str) -> None:
        self._com_obj.RemoteHost = str(value)

    @property
    @ts_interface
    def sequence_comment(self) -> str:
        return str(self._com_obj.SequenceComment)

    @property
    @ts_interface
    def sequence_file_path(self) -> str:
        return str(self._com_obj.SequenceFilePath)

    @sequence_file_path.setter
    @ts_interface
    def sequence_file_path(self, value: str) -> None:
        self._com_obj.SequenceFilePath = str(value)

    @property
    @ts_interface
    def sequence_name(self) -> str:
        return str(self._com_obj.SequenceName)

    @sequence_name.setter
    @ts_interface
    def sequence_name(self, value: str) -> None:
        self._com_obj.SequenceName = str(value)

    @property
    @ts_interface
    def specify_by_expression(self) -> bool:
        return bool(self._com_obj.SpecifyByExpression)

    @specify_by_expression.setter
    @ts_interface
    def specify_by_expression(self, value: bool) -> None:
        self._com_obj.SpecifyByExpression = bool(value)

    @property
    @ts_interface
    def specify_host_by_expression(self) -> bool:
        return bool(self._com_obj.SpecifyHostByExpression)

    @specify_host_by_expression.setter
    @ts_interface
    def specify_host_by_expression(self, value: bool) -> None:
        self._com_obj.SpecifyHostByExpression = bool(value)

    @property
    @ts_interface
    def store_activex_reference_expr(self) -> str:
        return str(self._com_obj.StoreActiveXReferenceExpr)

    @store_activex_reference_expr.setter
    @ts_interface
    def store_activex_reference_expr(self, value: str) -> None:
        self._com_obj.StoreActiveXReferenceExpr = str(value)

    @property
    @ts_interface
    def trace_setting(self) -> typing.Any:
        return int(self._com_obj.TraceSetting)

    @trace_setting.setter
    @ts_interface
    def trace_setting(self, value: int) -> None:
        self._com_obj.TraceSetting = int(value)

    @property
    @ts_interface
    def use_current_file(self) -> bool:
        return bool(self._com_obj.UseCurrentFile)

    @use_current_file.setter
    @ts_interface
    def use_current_file(self, value: bool) -> None:
        self._com_obj.UseCurrentFile = bool(value)

    @property
    @ts_interface
    def use_sequence_parameter_prototype(self) -> bool:
        return bool(self._com_obj.UseSequenceParameterPrototype)

    @use_sequence_parameter_prototype.setter
    @ts_interface
    def use_sequence_parameter_prototype(self, value: bool) -> None:
        self._com_obj.UseSequenceParameterPrototype = bool(value)

    @ts_interface
    def as_module(self) -> typing.Any:
        from py_teststand.adapters import Module

        return Module(self._com_obj.AsModule(), self._engine_ref)


class SequenceCallParameter(PropertyObject):
    @ts_interface
    def as_adapter_parameter(self) -> typing.Any:
        return self._com_obj.AsAdapterParameter()

    @ts_interface
    def as_property_object(self) -> PropertyObject:
        return PropertyObject(self._com_obj.AsPropertyObject(), self._engine_ref)

    @property
    @ts_interface
    def direction(self) -> int:
        return int(self._com_obj.Direction)

    @property
    @ts_interface
    def flags(self) -> int:
        return int(self._com_obj.Flags)

    @flags.setter
    @ts_interface
    def flags(self, value: int) -> None:
        self._com_obj.Flags = int(value)

    @property
    @ts_interface
    def is_parameter_mapping_valid(self) -> bool:
        return bool(self._com_obj.IsParameterMappingValid)

    @property
    @ts_interface
    def name(self) -> str:
        return str(self._com_obj.Name)

    @property
    @ts_interface
    def type(self) -> typing.Any:
        return int(self._com_obj.Type)

    @property
    @ts_interface
    def type_display_string(self) -> str:
        return str(self._com_obj.TypeDisplayString)

    @property
    @ts_interface
    def user_data(self) -> PropertyObject:
        return PropertyObject(self._com_obj.UserData, self._engine_ref)

    @user_data.setter
    @ts_interface
    def user_data(self, value: PropertyObject) -> None:
        self._com_obj.UserData = value._com_obj

    @property
    @ts_interface
    def valid_evaluation_types(self) -> EvaluationTypes:
        from py_teststand.sequence.expression import EvaluationTypes

        return EvaluationTypes(self._com_obj.ValidEvaluationTypes, self._engine_ref)

    @property
    @ts_interface
    def value_expr(self) -> str:
        return str(self._com_obj.ValueExpr)

    @value_expr.setter
    @ts_interface
    def value_expr(self, value: str) -> None:
        self._com_obj.ValueExpr = str(value)

    @property
    @ts_interface
    def value_expr_is_optional(self) -> bool:
        return bool(self._com_obj.ValueExprIsOptional)


class SequenceCallParameters(PropertyObject):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index: typing.Any) -> typing.Any:
        return SequenceCallParameter(self._com_obj.Item(index), self._engine_ref)

    def __len__(self) -> int:

        return self.count

    def __getitem__(self, index: int | str) -> SequenceCallParameter:

        return self.item(index)
