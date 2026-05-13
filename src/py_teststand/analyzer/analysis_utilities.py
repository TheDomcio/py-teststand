from __future__ import annotations

import typing
from enum import IntFlag

from py_teststand.core.com_wrapper import ts_interface
from py_teststand.property.property_object import PropertyObject


class ValidateExpressionOption(IntFlag):
    NoneValue = 0x0
    Path = 0x1
    MustEvaluateToProperty = 0x2


class ValidatePathOption(IntFlag):
    NoneValue = 0x0
    IgnoreAbsolutePath = 0x1
    DoNotCheckIfExists = 0x2
    NotRequiredForExecution = 0x4
    IsCommand = 0x8


class AnalysisUtilities(PropertyObject):
    @property
    @ts_interface
    def automatic_property_checking_enabled(self) -> bool:
        return bool(self._com_obj.AutomaticPropertyCheckingEnabled)

    @automatic_property_checking_enabled.setter
    @ts_interface
    def automatic_property_checking_enabled(self, value: bool) -> None:
        self._com_obj.AutomaticPropertyCheckingEnabled = bool(value)

    @ts_interface
    def validate_expression(
        self,
        expression: str,
        options: ValidateExpressionOption | int = (ValidateExpressionOption.NoneValue),
    ) -> bool:
        return bool(self._com_obj.ValidateExpression(str(expression), int(options)))

    @ts_interface
    def validate_path(
        self,
        path: str,
        options: ValidatePathOption | int = ValidatePathOption.NoneValue,
    ) -> bool:
        return bool(self._com_obj.ValidatePath(str(path), int(options)))

    @ts_interface
    def validate_remote_host(self, host_name: str) -> bool:
        return bool(self._com_obj.ValidateRemoteHost(str(host_name)))

    @ts_interface
    def validate_code_module_up_to_date(self, step: PropertyObject, file_path: str) -> bool:
        return bool(self._com_obj.ValidateCodeModuleUpToDate(step._com_obj, str(file_path)))

    @staticmethod
    def auto_wire_parameters(module: typing.Any, sequence: typing.Any) -> None:
        import logging

        logger = logging.getLogger(__name__)

        if not hasattr(module, "parameters"):
            logger.warning(f"Module {module} does not support parameter wiring.")
            return
        params = module.parameters
        locals_po = sequence.locals
        for i in range(params.count):
            param = params.item(i)
            name = param.name
            try:
                direction = param.direction
                if direction in (1, 2, 3):
                    type_def = param.get_type_definition("")
                    type_name = type_def.name if type_def else "Number"
                    if not locals_po.exists(name):
                        from py_teststand.property.property_object import PropValType

                        locals_po.new_sub_property(name, PropValType.Number, False, type_name)
                    param.value_expr = f"Locals.{name}"
                    logger.info(f"Auto-wired parameter {name} (Dir: {direction}) to Locals.{name}")
            except Exception as e:
                logger.debug(f"Could not wire parameter {name}: {e}")


__all__ = ["AnalysisUtilities", "ValidateExpressionOption", "ValidatePathOption"]
