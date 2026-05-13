from __future__ import annotations

from enum import IntFlag
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.property.property_object import PropertyObject

if TYPE_CHECKING:
    from py_teststand.execution.execution import Execution
    from py_teststand.sequence.sequence_context import SequenceContext


class WatchExpressionBreakType(IntFlag):
    NoneValue = 0
    OnChange = 1
    OnExpressionTrue = 2


class WatchExpression(COMWrapper):
    @property
    @ts_interface
    def breakpoint_type(self) -> int:
        return int(self._com_obj.BreakpointType)

    @breakpoint_type.setter
    @ts_interface
    def breakpoint_type(self, value: int) -> None:
        self._com_obj.BreakpointType = int(value)

    @property
    @ts_interface
    def client_sequence_file(self) -> str:
        return str(self._com_obj.ClientSequenceFile)

    @client_sequence_file.setter
    @ts_interface
    def client_sequence_file(self, value: str) -> None:
        self._com_obj.ClientSequenceFile = str(value)

    @property
    @ts_interface
    def execution_scope(self) -> Execution:
        from py_teststand.execution.execution import Execution

        return Execution(self._com_obj.ExecutionScope, self._engine_ref)

    @execution_scope.setter
    @ts_interface
    def execution_scope(self, value: Execution) -> None:
        self._com_obj.ExecutionScope = value._com_obj

    @property
    @ts_interface
    def expression(self) -> str:
        return str(self._com_obj.Expression)

    @expression.setter
    @ts_interface
    def expression(self, value: str) -> None:
        self._com_obj.Expression = str(value)

    @property
    @ts_interface
    def numeric_format(self) -> str:
        return str(self._com_obj.NumericFormat)

    @numeric_format.setter
    @ts_interface
    def numeric_format(self, value: str) -> None:
        self._com_obj.NumericFormat = str(value)

    @property
    @ts_interface
    def sequence_file_scope(self) -> str:
        return str(self._com_obj.SequenceFileScope)

    @sequence_file_scope.setter
    @ts_interface
    def sequence_file_scope(self, value: str) -> None:
        self._com_obj.SequenceFileScope = str(value)

    @property
    @ts_interface
    def sequence_scope(self) -> str:
        return str(self._com_obj.SequenceScope)

    @sequence_scope.setter
    @ts_interface
    def sequence_scope(self, value: str) -> None:
        self._com_obj.SequenceScope = str(value)

    @property
    @ts_interface
    def unique_watch_id(self) -> str:
        return str(self._com_obj.UniqueWatchId)

    @property
    @ts_interface
    def use_scoping_context(self) -> bool:
        return bool(self._com_obj.UseScopingContext)

    @use_scoping_context.setter
    @ts_interface
    def use_scoping_context(self, value: bool) -> None:
        self._com_obj.UseScopingContext = bool(value)

    @ts_interface
    def breakpoint_triggered(self, seq_context: SequenceContext) -> bool:
        return bool(self._com_obj.BreakpointTriggered(seq_context._com_obj))

    @ts_interface
    def display_configuration_dialog(
        self, title: str, context: SequenceContext, options: int = 0
    ) -> bool:
        return bool(
            self._com_obj.DisplayConfigurationDialog(str(title), context._com_obj, int(options))
        )

    @ts_interface
    def evaluate(self, seq_context: SequenceContext, reserved: int = 0) -> PropertyObject:
        return PropertyObject(
            self._com_obj.Evaluate(seq_context._com_obj, int(reserved)), self._engine_ref
        )

    @ts_interface
    def get_scoping_context(self, current_seq_context: SequenceContext) -> SequenceContext:
        from py_teststand.sequence.sequence_context import SequenceContext

        return SequenceContext(
            self._com_obj.GetScopingContext(current_seq_context._com_obj), self._engine_ref
        )


class WatchExpressions(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index: int) -> WatchExpression:
        return WatchExpression(self._com_obj.Item(index), self._engine_ref)

    @ts_interface
    def insert(
        self,
        before_pos: int = 0,
        client_sequence_file_param: str = "",
        insert_in_engine: bool = True,
    ) -> WatchExpression:
        return WatchExpression(
            self._com_obj.Insert(
                int(before_pos), str(client_sequence_file_param), bool(insert_in_engine)
            ),
            self._engine_ref,
        )

    @ts_interface
    def remove(self, watch_expression: WatchExpression) -> None:
        self._com_obj.Remove(watch_expression._com_obj)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def clone(self, insert_in_engine: bool = True) -> WatchExpressions:
        return WatchExpressions(self._com_obj.Clone(bool(insert_in_engine)), self._engine_ref)

    def __len__(self) -> int:
        return self.count

    def __getitem__(self, index: int) -> WatchExpression:
        return self.item(index)

    def __iter__(self):
        for i in range(self.count):
            yield self.item(i)
