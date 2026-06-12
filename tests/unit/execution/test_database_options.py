from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from py_teststand.execution.database_options import DatabaseLogOptions


@pytest.fixture
def mock_engine():

    return MagicMock()


@pytest.fixture
def mock_database_options_com():

    class State:
        def __init__(self):

            self.values = {
                "DisableDatabaseLogging": False,
                "UseOnTheFlyLogging": True,
                "IncludeExecutionTimes": True,
                "UseTransactionProcessing": False,
                "IncludeStepResults": True,
                "IncludeMeasurements": True,
                "IncludeTestLimits": True,
                "ResultFilteringExpression": "True",
                "DatabaseManagementSystem": "SQL Server",
                "ConnectionStringExpression": (
                    '"DRIVER={SQL Server};SERVER=myserver;DATABASE=mydb;UID=user;PWD=password"'
                ),
                "ShareDataLinkBetweenExecutions": True,
            }

    state = State()

    mock_com = MagicMock()

    def get_val_variant(name, _options):

        return state.values.get(name)

    def set_val_variant(name, _options, value):

        if type(value).__name__ == "VARIANT":
            value = True if value.value else False if isinstance(value.value, int) else value.value

        state.values[name] = value

    mock_com.GetValVariant.side_effect = get_val_variant

    mock_com.SetValVariant.side_effect = set_val_variant

    return mock_com


def test_database_options_properties(mock_engine, mock_database_options_com):

    options = DatabaseLogOptions(mock_database_options_com, mock_engine)

    assert options.disable_database_logging is False

    assert options.use_on_the_fly_logging is True

    assert options.include_execution_times is True

    assert options.use_transaction_processing is False

    assert options.include_step_results is True

    assert options.include_measurements is True

    assert options.include_test_limits is True

    assert options.result_filtering_expression == "True"

    assert options.database_management_system == "SQL Server"

    assert (
        options.connection_string_expression
        == '"DRIVER={SQL Server};SERVER=myserver;DATABASE=mydb;UID=user;PWD=password"'
    )

    assert options.share_data_link_between_executions is True


def test_database_options_setters(mock_engine, mock_database_options_com):

    options = DatabaseLogOptions(mock_database_options_com, mock_engine)

    options.disable_database_logging = True

    assert mock_database_options_com.SetValVariant.called

    assert options.disable_database_logging is True

    options.use_on_the_fly_logging = False

    assert options.use_on_the_fly_logging is False

    options.include_execution_times = False

    assert options.include_execution_times is False

    options.use_transaction_processing = True

    assert options.use_transaction_processing is True

    options.include_step_results = False

    assert options.include_step_results is False

    options.include_measurements = False

    assert options.include_measurements is False

    options.include_test_limits = False

    assert options.include_test_limits is False

    options.result_filtering_expression = "False"

    assert options.result_filtering_expression == "False"

    options.database_management_system = "Oracle"

    assert options.database_management_system == "Oracle"

    options.connection_string_expression = '"New Connection String"'

    assert options.connection_string_expression == '"New Connection String"'

    options.share_data_link_between_executions = False

    assert options.share_data_link_between_executions is False
