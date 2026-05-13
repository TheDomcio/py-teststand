from __future__ import annotations

import typing
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COMWrapper, ts_interface


class EntryPoint(COMWrapper):
    @property
    @ts_interface
    def name(self) -> str:
        return str(self._com_obj.Name)

    @property
    @ts_interface
    def enabled(self) -> bool:
        return bool(self._com_obj.Enabled)

    @property
    @ts_interface
    def interactive_execution_allowed(self) -> bool:
        return bool(self._com_obj.InteractiveExecutionAllowed)

    @property
    @ts_interface
    def sequence(self) -> Sequence | None:
        from py_teststand.sequence.sequence import Sequence

        obj = self._com_obj.Sequence
        return Sequence(obj, self._engine_ref) if obj else None

    @ts_interface
    def run(self, edit_args_val: typing.Any = None) -> Execution:
        from py_teststand.execution.execution import Execution

        raw_args = getattr(edit_args_val, "_com_obj", edit_args_val) if edit_args_val else None
        return Execution(self._com_obj.Run(raw_args), self._engine_ref)

    @ts_interface
    def run_selected_steps(self, edit_args_val: typing.Any = None) -> Execution:
        from py_teststand.execution.execution import Execution

        raw_args = getattr(edit_args_val, "_com_obj", edit_args_val) if edit_args_val else None
        return Execution(self._com_obj.RunSelectedSteps(raw_args), self._engine_ref)

    @ts_interface
    def loop_on_selected_steps(self, edit_args_val: typing.Any = None) -> Execution:
        from py_teststand.execution.execution import Execution

        raw_args = getattr(edit_args_val, "_com_obj", edit_args_val) if edit_args_val else None
        return Execution(self._com_obj.LoopOnSelectedSteps(raw_args), self._engine_ref)


if TYPE_CHECKING:
    from py_teststand.execution.execution import Execution
    from py_teststand.sequence.sequence import Sequence


class EntryPoints(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index_or_name: typing.Any) -> EntryPoint:
        return EntryPoint(self._com_obj.Item(index_or_name), self._engine_ref)

    def __len__(self) -> int:

        return self.count

    def __getitem__(self, key: typing.Any) -> EntryPoint:

        return self.item(key)

    def __iter__(self):

        for i in range(self.count):
            yield self.item(i)
