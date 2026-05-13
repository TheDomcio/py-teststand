from __future__ import annotations

import typing
from enum import IntEnum

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.property.data_type import PropertyObjectType
from py_teststand.property.property_object import PropertyObject


class CheckedState(IntEnum):
    Unchecked = 1
    Checked = 2
    Indeterminate = 3


class AdditionalResultKind(IntEnum):
    Custom = 1
    InParameter = 2
    OutParameter = 3
    Call = 4


class AdditionalResult(COMWrapper):
    @property
    @ts_interface
    def name(self) -> str:
        return str(self._com_obj.Name)

    @name.setter
    @ts_interface
    def name(self, value: str) -> None:
        self._com_obj.Name = str(value)

    @property
    @ts_interface
    def checked_state(self) -> int:
        return int(self._com_obj.CheckedState)

    @checked_state.setter
    @ts_interface
    def checked_state(self, value: int) -> None:
        self._com_obj.CheckedState = value

    @property
    @ts_interface
    def value_to_log(self) -> str:
        return str(self._com_obj.ValueToLog)

    @value_to_log.setter
    @ts_interface
    def value_to_log(self, value: str) -> None:
        self._com_obj.ValueToLog = value

    @property
    @ts_interface
    def condition(self) -> str:
        return str(self._com_obj.Condition)

    @condition.setter
    @ts_interface
    def condition(self, value: str) -> None:
        self._com_obj.Condition = value

    @property
    @ts_interface
    def flags(self) -> int:
        return int(self._com_obj.Flags)

    @flags.setter
    @ts_interface
    def flags(self, value: int) -> None:
        self._com_obj.Flags = value

    @property
    @ts_interface
    def is_any_type(self) -> bool:
        return bool(self._com_obj.IsAnyType)

    @is_any_type.setter
    @ts_interface
    def is_any_type(self, value: bool) -> None:
        self._com_obj.IsAnyType = value

    @property
    @ts_interface
    def type(self) -> PropertyObjectType | None:
        com = self._com_obj.Type
        return PropertyObjectType(com, self._engine_ref) if com else None

    @type.setter
    @ts_interface
    def type(self, value: PropertyObjectType | None) -> None:
        self._com_obj.Type = value._com_obj if value else None

    @property
    @ts_interface
    def elements(self) -> AdditionalResults:
        return AdditionalResults(self._com_obj.Elements, self._engine_ref)

    @property
    @ts_interface
    def parent_additional_result(self) -> AdditionalResult | None:
        com = self._com_obj.ParentAdditionalResult
        if com is None:
            return None
        return AdditionalResult(com, self._engine_ref)

    @property
    @ts_interface
    def are_elements_incompatible_with_type(self) -> bool:
        return bool(self._com_obj.AreElementsIncompatibleWithType)

    @property
    @ts_interface
    def kind(self) -> int:
        return int(self._com_obj.Kind)

    @property
    @ts_interface
    def parameter_object(self) -> PropertyObject | None:
        com = self._com_obj.ParameterObject
        return PropertyObject(com, self._engine_ref) if com else None

    @property
    @ts_interface
    def unmapped_additional_results(self) -> AdditionalResults:
        return AdditionalResults(self._com_obj.UnmappedAdditionalResults, self._engine_ref)


class AdditionalResults(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @property
    @ts_interface
    def checked_item_count(self) -> int:
        return int(self._com_obj.CheckedItemCount)

    def __len__(self) -> int:
        return self.count

    def __getitem__(self, index: int | str) -> AdditionalResult:
        return AdditionalResult(self._com_obj.Item(index), self._engine_ref)

    def __iter__(self) -> typing.Iterator[AdditionalResult]:
        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def insert(
        self,
        name: str = "",
        value_to_log: str = "",
        condition: str = "",
        flags: int = 0x2000,
        index: int = -1,
    ) -> AdditionalResult:
        return AdditionalResult(
            self._com_obj.Insert(name, value_to_log, condition, flags, index),
            self._engine_ref,
        )

    @ts_interface
    def move(self, index: int | str, new_index: int) -> None:
        self._com_obj.Move(index, new_index)

    @ts_interface
    def remove(self, index: int | str) -> AdditionalResult:
        return AdditionalResult(self._com_obj.Remove(index), self._engine_ref)


class StepAdditionalResults(COMWrapper):
    @property
    @ts_interface
    def parameter_results(self) -> AdditionalResults:
        return AdditionalResults(self._com_obj.ParameterResults, self._engine_ref)

    @property
    @ts_interface
    def custom_results(self) -> AdditionalResults:
        return AdditionalResults(self._com_obj.CustomResults, self._engine_ref)
