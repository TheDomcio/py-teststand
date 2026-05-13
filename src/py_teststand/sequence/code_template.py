from __future__ import annotations

import typing
from enum import IntFlag

from py_teststand.core.com_wrapper import ts_interface
from py_teststand.property.property_object import PropertyObject


class CodeTemplateType(IntFlag):
    NoneValue = 0
    LabVIEW = 2
    CVI = 3
    CppOrC = 4
    HTBasic = 8
    LabVIEWNXG = 9
    CodeTemplateType_Legacy = 1
    CodeTemplateType_VisualBasicDotNet = 7
    CodeTemplateType_VisualCppDotNet = 5
    CodeTemplateType_VisualCSharpDotNet = 6


class CodeTemplate(PropertyObject):
    @property
    @ts_interface
    def type(self) -> typing.Any:
        return int(self._com_obj.Type)

    @property
    @ts_interface
    def name(self) -> str:
        return str(self._com_obj.Name)

    @property
    @ts_interface
    def description(self) -> str:
        return str(self._com_obj.Description)


class CodeTemplates(PropertyObject):
    @ts_interface
    def __len__(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def __getitem__(self, index: int | str) -> CodeTemplate:
        return CodeTemplate(self._com_obj.Item(index), self._engine_ref)

    @ts_interface
    def get_by_index(self, index: int) -> CodeTemplate:
        if index < 0 or index >= self.count:
            raise IndexError("Index out of range")
        return self[index]

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)
