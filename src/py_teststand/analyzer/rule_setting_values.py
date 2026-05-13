from __future__ import annotations

from py_teststand.core.com_wrapper import ts_interface
from py_teststand.property.property_object import PropertyObject


class RuleSettingValues(PropertyObject):
    @ts_interface
    def get_boolean_value(self, name: str) -> bool:
        return bool(self._com_obj.GetBooleanValue(str(name)))

    @ts_interface
    def get_number_value(self, name: str) -> float:
        return float(self._com_obj.GetNumberValue(str(name)))

    @ts_interface
    def get_string_value(self, name: str) -> str:
        return str(self._com_obj.GetStringValue(str(name)))


__all__ = ["RuleSettingValues"]
