from __future__ import annotations

from py_teststand.core.com_wrapper import ts_interface
from py_teststand.property.property_object_file import PropertyObjectFile
from py_teststand.sequence.step_type import StepType


class TypePalette(PropertyObjectFile):
    @ts_interface
    def get_step_types(self) -> list[StepType]:
        root = self.as_property_object()
        step_types_prop = root.get_property_object("StepTypes")
        if not step_types_prop:
            return []

        num_types = step_types_prop.get_num_elements()
        types = []
        for i in range(num_types):
            type_com = step_types_prop.get_property_object_by_offset(i)
            if type_com:
                types.append(StepType(type_com.get_com_obj()))
        return types
