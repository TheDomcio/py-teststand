from __future__ import annotations

from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COMWrapper, ts_interface

if TYPE_CHECKING:
    from py_teststand.sequence.sequence_file import SequenceFile


class SelectedBreakpointItem(COMWrapper):
    @ts_interface
    def is_end_selected(self) -> bool:
        return bool(self._com_obj.IsEndSelected())

    @property
    @ts_interface
    def sequence_file(self) -> SequenceFile:
        from py_teststand.sequence.sequence_file import SequenceFile

        return SequenceFile(self._com_obj.SequenceFile, self._engine_ref)

    @property
    @ts_interface
    def sequence_name(self) -> str:
        return str(self._com_obj.SequenceName)

    @property
    @ts_interface
    def step_group(self) -> int:
        return int(self._com_obj.StepGroup)

    @property
    @ts_interface
    def step_id(self) -> str:
        return str(self._com_obj.StepId)
