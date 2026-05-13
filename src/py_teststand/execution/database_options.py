from __future__ import annotations

from py_teststand.core.com_wrapper import ts_interface
from py_teststand.property.property_object import PropertyObject


class DatabaseLogOptions(PropertyObject):
    @property
    @ts_interface
    def disable_database_logging(self) -> bool:
        return bool(self.get_val_variant("DisableDatabaseLogging"))

    @disable_database_logging.setter
    @ts_interface
    def disable_database_logging(self, value: bool) -> None:
        self.set_val_variant("DisableDatabaseLogging", 0, bool(value))

    @property
    @ts_interface
    def use_on_the_fly_logging(self) -> bool:
        return bool(self.get_val_variant("UseOnTheFlyLogging"))

    @use_on_the_fly_logging.setter
    @ts_interface
    def use_on_the_fly_logging(self, value: bool) -> None:
        self.set_val_variant("UseOnTheFlyLogging", 0, bool(value))

    @property
    @ts_interface
    def include_execution_times(self) -> bool:
        return bool(self.get_val_variant("IncludeExecutionTimes"))

    @include_execution_times.setter
    @ts_interface
    def include_execution_times(self, value: bool) -> None:
        self.set_val_variant("IncludeExecutionTimes", 0, bool(value))

    @property
    @ts_interface
    def use_transaction_processing(self) -> bool:
        return bool(self.get_val_variant("UseTransactionProcessing"))

    @use_transaction_processing.setter
    @ts_interface
    def use_transaction_processing(self, value: bool) -> None:
        self.set_val_variant("UseTransactionProcessing", 0, bool(value))

    @property
    @ts_interface
    def include_step_results(self) -> bool:
        return bool(self.get_val_variant("IncludeStepResults"))

    @include_step_results.setter
    @ts_interface
    def include_step_results(self, value: bool) -> None:
        self.set_val_variant("IncludeStepResults", 0, bool(value))

    @property
    @ts_interface
    def include_measurements(self) -> bool:
        return bool(self.get_val_variant("IncludeMeasurements"))

    @include_measurements.setter
    @ts_interface
    def include_measurements(self, value: bool) -> None:
        self.set_val_variant("IncludeMeasurements", 0, bool(value))

    @property
    @ts_interface
    def include_test_limits(self) -> bool:
        return bool(self.get_val_variant("IncludeTestLimits"))

    @include_test_limits.setter
    @ts_interface
    def include_test_limits(self, value: bool) -> None:
        self.set_val_variant("IncludeTestLimits", 0, bool(value))

    @property
    @ts_interface
    def result_filtering_expression(self) -> str:
        return str(self.get_val_variant("ResultFilteringExpression"))

    @result_filtering_expression.setter
    @ts_interface
    def result_filtering_expression(self, value: str) -> None:
        self.set_val_variant("ResultFilteringExpression", 0, str(value))

    @property
    @ts_interface
    def database_management_system(self) -> str:
        return str(self.get_val_variant("DatabaseManagementSystem"))

    @database_management_system.setter
    @ts_interface
    def database_management_system(self, value: str) -> None:
        self.set_val_variant("DatabaseManagementSystem", 0, str(value))

    @property
    @ts_interface
    def connection_string_expression(self) -> str:
        return str(self.get_val_variant("ConnectionStringExpression"))

    @connection_string_expression.setter
    @ts_interface
    def connection_string_expression(self, value: str) -> None:
        self.set_val_variant("ConnectionStringExpression", 0, str(value))

    @property
    @ts_interface
    def share_data_link_between_executions(self) -> bool:
        return bool(self.get_val_variant("ShareDataLinkBetweenExecutions"))

    @share_data_link_between_executions.setter
    @ts_interface
    def share_data_link_between_executions(self, value: bool) -> None:
        self.set_val_variant("ShareDataLinkBetweenExecutions", 0, bool(value))
