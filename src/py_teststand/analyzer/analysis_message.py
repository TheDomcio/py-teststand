from __future__ import annotations

from py_teststand.core.com_wrapper import ts_interface
from py_teststand.property.property_object import PropertyObject


class AnalysisMessage(PropertyObject):
    @property
    @ts_interface
    def text(self) -> str:
        return str(self._com_obj.Text)

    @text.setter
    @ts_interface
    def text(self, value: str) -> None:
        self._com_obj.Text = str(value)

    @property
    @ts_interface
    def rule_id(self) -> str:
        return str(self._com_obj.RuleId)

    @rule_id.setter
    @ts_interface
    def rule_id(self, value: str) -> None:
        self._com_obj.RuleId = str(value)

    @property
    @ts_interface
    def locations(self) -> PropertyObject:
        return PropertyObject(self._com_obj.Locations, self._engine_ref)


__all__ = ["AnalysisMessage"]
