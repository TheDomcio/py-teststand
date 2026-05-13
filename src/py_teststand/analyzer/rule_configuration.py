from __future__ import annotations

from py_teststand.analyzer.rule import RuleSeverity
from py_teststand.analyzer.rule_setting_values import RuleSettingValues
from py_teststand.core.com_wrapper import ts_interface
from py_teststand.property.property_object import PropertyObject


class RuleConfiguration(PropertyObject):
    @property
    @ts_interface
    def rule_id(self) -> str:
        return str(self._com_obj.RuleId)

    @property
    @ts_interface
    def description(self) -> str:
        return str(self._com_obj.Description)

    @description.setter
    @ts_interface
    def description(self, value: str) -> None:
        self._com_obj.Description = str(value)

    @property
    @ts_interface
    def enabled(self) -> bool:
        return bool(self._com_obj.Enabled)

    @enabled.setter
    @ts_interface
    def enabled(self, value: bool) -> None:
        self._com_obj.Enabled = bool(value)

    @property
    @ts_interface
    def severity(self) -> RuleSeverity:
        return RuleSeverity(int(self._com_obj.Severity))

    @severity.setter
    @ts_interface
    def severity(self, value: RuleSeverity | int) -> None:
        self._com_obj.Severity = int(value)

    @property
    @ts_interface
    def configuration_data(self) -> PropertyObject:
        return PropertyObject(self._com_obj.ConfigurationData, self._engine_ref)

    @property
    @ts_interface
    def rule_setting_values(self) -> RuleSettingValues:
        return RuleSettingValues(self._com_obj.RuleSettingValues, self._engine_ref)


class RuleConfigurationContext(PropertyObject):
    @property
    @ts_interface
    def engine(self) -> PropertyObject:
        return PropertyObject(self._com_obj.Engine, self._engine_ref)

    @property
    @ts_interface
    def is_modified(self) -> bool:
        return bool(self._com_obj.IsModified)

    @is_modified.setter
    @ts_interface
    def is_modified(self, value: bool) -> None:
        self._com_obj.IsModified = bool(value)

    @property
    @ts_interface
    def rule_configuration(self) -> RuleConfiguration:
        return RuleConfiguration(self._com_obj.RuleConfiguration, self._engine_ref)


__all__ = ["RuleConfiguration", "RuleConfigurationContext"]
