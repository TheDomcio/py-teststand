from __future__ import annotations

from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COMWrapper, ts_interface

if TYPE_CHECKING:
    from py_teststand.execution.execution import Execution
    from py_teststand.property.property_object import PropertyObject
    from py_teststand.property.property_object_file import PropertyObjectFile
    from py_teststand.sequence.sequence import Sequence
    from py_teststand.sequence.sequence_file import SequenceFile
    from py_teststand.sequence.step import Step


class EditArgs(COMWrapper):
    @ts_interface
    def set_selected_sequence_file(self, sequence_file: SequenceFile | None) -> None:
        self._com_obj.SetSelectedSequenceFile(sequence_file._com_obj if sequence_file else None)

    @ts_interface
    def add_selected_sequence(self, sequence: Sequence) -> None:
        self._com_obj.AddSelectedSequence(sequence._com_obj)

    @ts_interface
    def add_selected_step(self, step: Step) -> None:
        self._com_obj.AddSelectedStep(step._com_obj)

    @ts_interface
    def clear_selected_sequences(self) -> None:
        self._com_obj.ClearSelectedSequences()

    @ts_interface
    def clear_selected_steps(self) -> None:
        self._com_obj.ClearSelectedSteps()

    @ts_interface
    def set_selected_execution(self, execution: Execution | None) -> None:
        self._com_obj.SetSelectedExecution(execution._com_obj if execution else None)

    @ts_interface
    def add_selected_property_object(self, property_object: PropertyObject) -> None:
        self._com_obj.AddSelectedPropertyObject(property_object._com_obj)

    @ts_interface
    def clear_selected_property_objects(self) -> None:
        self._com_obj.ClearSelectedPropertyObjects()

    @ts_interface
    def set_selected_property_object_file(self, property_file: PropertyObjectFile | None) -> None:
        self._com_obj.SetSelectedPropertyObjectFile(
            property_file._com_obj if property_file else None,
        )

    @ts_interface
    def set_selected_step_group(self, step_group: int) -> None:
        self._com_obj.SetSelectedStepGroup(int(step_group))

    @ts_interface
    def as_property_object(self) -> PropertyObject:
        from py_teststand.property.property_object import PropertyObject

        return PropertyObject(self._com_obj.AsPropertyObject(), self._engine_ref)
