from __future__ import annotations

import typing
from enum import IntEnum, IntFlag
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.property.property_object import PropertyObject

if TYPE_CHECKING:
    from py_teststand.execution.execution import Execution
    from py_teststand.execution.interactive_args import InteractiveArgs


class CPUAffinityForNewThreadOption(IntEnum):
    UseStationOption = 0
    UseAffinityOfCaller = 1
    UseAllCPUs = 2
    UseCustomAffinity = 3


class SeqCallNewExecModelOption(IntEnum):
    NoneValue = 0
    SpecifyModel = 2
    UseModelOfCurrentFile = 1


class SeqCallNewThreadOption(IntFlag):
    WaitForThreadCompletion = 0x1
    InitiallySuspended = 0x2
    UseSingleThreadedApartment = 0x4


class SeqCallWaitForExecOption(IntEnum):
    BeforeNextStep = 1
    NoneValue = 0
    EndOfSequence = 2


class Thread(COMWrapper):
    @ts_interface
    def as_property_object(self) -> PropertyObject:
        return PropertyObject(self._com_obj.AsPropertyObject(), self._engine_ref)

    @property
    @ts_interface
    def batch(self) -> typing.Any:
        return self._com_obj.Batch

    @property
    @ts_interface
    def call_stack_size(self) -> int:
        return int(self._com_obj.CallStackSize)

    @property
    @ts_interface
    def display_name(self) -> str:
        return str(self._com_obj.DisplayName)

    @property
    @ts_interface
    def execution(self) -> Execution:
        from py_teststand.execution.execution import Execution

        return Execution(self._com_obj.Execution, self._engine_ref)

    @property
    @ts_interface
    def externally_suspended(self) -> bool:
        return bool(self._com_obj.ExternallySuspended)

    @externally_suspended.setter
    @ts_interface
    def externally_suspended(self, value: bool) -> None:
        self._com_obj.ExternallySuspended = bool(value)

    @property
    @ts_interface
    def id(self) -> int:
        return int(self._com_obj.Id)

    @property
    @ts_interface
    def run_time_variables(self) -> PropertyObject:
        return PropertyObject(self._com_obj.RunTimeVariables, self._engine_ref)

    @property
    @ts_interface
    def termination_option(self) -> int:
        return int(self._com_obj.TerminationOption)

    @termination_option.setter
    @ts_interface
    def termination_option(self, value: int) -> None:
        self._com_obj.TerminationOption = int(value)

    @property
    @ts_interface
    def unique_thread_id(self) -> str:
        return str(self._com_obj.UniqueThreadId)

    @property
    @ts_interface
    def will_step_into_module(self) -> bool:
        return bool(self._com_obj.WillStepIntoModule)

    @ts_interface
    def add_to_batch(self, batch_obj: typing.Any, order_number: int) -> None:
        self._com_obj.AddToBatch(batch_obj, int(order_number))

    @ts_interface
    def clear_current_rte(self) -> None:
        self._com_obj.ClearCurrentRTE()

    @ts_interface
    def clear_temporary_breakpoint(self) -> None:
        self._com_obj.ClearTemporaryBreakpoint()

    @ts_interface
    def do_interactive_execution(self, interactive_args: InteractiveArgs) -> None:
        self._com_obj.DoInteractiveExecution(interactive_args._com_obj)

    @ts_interface
    def flush_post_results(self) -> None:
        self._com_obj.FlushPostResults()

    @ts_interface
    def get_sequence_context(self, call_stack_index: int) -> tuple[typing.Any, int]:
        from py_teststand.sequence.sequence_context import SequenceContext

        res = self._com_obj.GetSequenceContext(int(call_stack_index))
        return SequenceContext(res[0], self._engine_ref), int(res[1])

    @ts_interface
    def post_ui_message(
        self,
        event_code: int,
        numeric_data_param: float,
        string_data_param: str,
        synchronous: bool,
    ) -> None:
        self._com_obj.PostUIMessage(
            int(event_code),
            float(numeric_data_param),
            str(string_data_param),
            bool(synchronous),
        )

    @ts_interface
    def post_ui_message_ex(
        self,
        event_code: int,
        numeric_data_param: float,
        string_data_param: str,
        active_x_data_param: typing.Any,
        synchronous: bool,
    ) -> None:
        self._com_obj.PostUIMessageEx(
            int(event_code),
            float(numeric_data_param),
            str(string_data_param),
            active_x_data_param,
            bool(synchronous),
        )

    @ts_interface
    def resume(self) -> None:
        self._com_obj.Resume()

    @ts_interface
    def set_batch_rte_option(self, option: int) -> None:
        self._com_obj.SetBatchRTEOption(int(option))

    @ts_interface
    def set_step_into(self) -> None:
        self._com_obj.SetStepInto()

    @ts_interface
    def set_step_out(self) -> None:
        self._com_obj.SetStepOut()

    @ts_interface
    def set_step_over(self) -> None:
        self._com_obj.SetStepOver()

    @ts_interface
    def wait_for_end(
        self,
        timeout_ms: int = -1,
        process_windows_msgs: bool = True,
        step_to_store_results_in: typing.Any = None,
        calling_sequence_context: typing.Any = None,
    ) -> bool:
        return bool(
            self._com_obj.WaitForEnd(
                int(timeout_ms),
                bool(process_windows_msgs),
                step_to_store_results_in,
                calling_sequence_context,
            ),
        )
