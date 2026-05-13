from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.property.property_object import PropertyObject

if TYPE_CHECKING:
    from py_teststand.sequence.sequence import Sequence


class InteractiveBranchMode(IntEnum):
    NoneValue = 0
    Ignore = 1
    GotoEnd = 2
    RaiseRTE = 3
    AllowAll = 4


class InteractiveContext(COMWrapper):
    @ts_interface
    def as_property_object(self) -> PropertyObject:
        return PropertyObject(self._com_obj.AsPropertyObject(), self._engine_ref)

    @property
    @ts_interface
    def is_root_execution(self) -> bool:
        return bool(self._com_obj.IsRootExecution)

    @property
    @ts_interface
    def saved_previous_step_index(self) -> int:
        return int(self._com_obj.SavedPreviousStepIndex)

    @property
    @ts_interface
    def saved_next_step_index(self) -> int:
        return int(self._com_obj.SavedNextStepIndex)

    @property
    @ts_interface
    def saved_step_index(self) -> int:
        return int(self._com_obj.SavedStepIndex)

    @property
    @ts_interface
    def interactive_args(self) -> InteractiveArgs:
        return InteractiveArgs(self._com_obj.InteractiveArgs, self._engine_ref)


class InteractiveArgs(COMWrapper):
    @ts_interface
    def as_property_object(self) -> PropertyObject:
        return PropertyObject(self._com_obj.AsPropertyObject(), self._engine_ref)

    @ts_interface
    def get_step_index(self, array_index: int) -> int:
        return int(self._com_obj.GetStepIndex(int(array_index)))

    @ts_interface
    def add_step_index(self, step_index: int) -> None:
        self._com_obj.AddStepIndex(int(step_index))

    @ts_interface
    def contains_step(self, step_index: int) -> bool:
        return bool(self._com_obj.ContainsStep(int(step_index)))

    @ts_interface
    def clear_step_list(self) -> None:
        self._com_obj.ClearStepList()

    @property
    @ts_interface
    def step_group(self) -> int:
        return int(self._com_obj.StepGroup)

    @step_group.setter
    @ts_interface
    def step_group(self, value: int) -> None:
        self._com_obj.StepGroup = int(value)

    @property
    @ts_interface
    def num_steps(self) -> int:
        return int(self._com_obj.NumSteps)

    @property
    @ts_interface
    def sequence(self) -> Sequence:
        from py_teststand.sequence.sequence import Sequence

        return Sequence(self._com_obj.Sequence, self._engine_ref)

    @sequence.setter
    @ts_interface
    def sequence(self, value: Sequence) -> None:
        self._com_obj.Sequence = value._com_obj

    @property
    @ts_interface
    def loop_count(self) -> int:
        return int(self._com_obj.LoopCount)

    @loop_count.setter
    @ts_interface
    def loop_count(self, value: int) -> None:
        self._com_obj.LoopCount = int(value)

    @property
    @ts_interface
    def stop_expression(self) -> str:
        return str(self._com_obj.StopExpression)

    @stop_expression.setter
    @ts_interface
    def stop_expression(self, value: str) -> None:
        self._com_obj.StopExpression = str(value)
