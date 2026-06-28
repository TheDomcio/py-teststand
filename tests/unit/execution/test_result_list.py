from __future__ import annotations

from unittest.mock import MagicMock

from py_teststand import ResultList


def test_result_list_parse() -> None:
    # Mocking result list array
    result_list_com = MagicMock()
    result_list_com.GetType.return_value = (0, False, True, "ResultList")  # is_array = True
    result_list_com.GetNumElements.return_value = 1

    # Mock the step result
    step_result_com = MagicMock()
    step_result_com.GetType.return_value = (0, False, False, "StepResult")  # not an array

    # Setup exists queries for step result
    def step_result_exists(path: str, _options: int) -> bool:
        return path in ["TS.StepName", "TS.StepType", "Status", "Numeric", "Limits"]

    step_result_com.Exists.side_effect = step_result_exists

    def step_result_get_string(path: str, _options: int) -> str:
        return {
            "TS.StepName": "Measure Voltage",
            "TS.StepType": "NumericLimitTest",
            "Status": "Passed",
        }.get(path, "")

    step_result_com.GetValString.side_effect = step_result_get_string

    step_result_com.GetValNumber.side_effect = lambda path, _options: (
        5.0 if path == "Numeric" else 0.0
    )

    # Mock Limits sub-property
    limits_com = MagicMock()
    limits_com.GetType.return_value = (0, False, False, "Limits")
    limits_com.Exists.side_effect = lambda path, _options: path in ["Low", "High"]
    limits_com.GetValNumber.side_effect = lambda path, _options: {
        "Low": 4.75,
        "High": 5.25,
    }.get(path, 0.0)

    # Configure GetPropertyObject of step result
    def step_result_get_prop(path: str, _options: int) -> MagicMock | None:
        if path == "Limits":
            return limits_com
        return None

    step_result_com.GetPropertyObject.side_effect = step_result_get_prop

    # Configure result_list_com's GetPropertyObjectByOffset to return our step result
    result_list_com.GetPropertyObjectByOffset.return_value = step_result_com

    res = ResultList(result_list_com).parse()
    assert len(res) == 1
    step = res[0]
    assert step["name"] == "Measure Voltage"
    assert step["type"] == "NumericLimitTest"
    assert step["status"] == "Passed"
    assert step["value"] == 5.0
    assert step["limits"] == {"low": 4.75, "high": 5.25}


def test_execution_result_list() -> None:
    # Mocking Execution result_object
    exec_com = MagicMock()

    # Configure ResultObject
    result_object_com = MagicMock()
    result_object_com.GetType.return_value = (0, False, False, "ResultObject")

    # Exists result list
    result_object_com.Exists.side_effect = lambda path, _options: path == "ResultList"

    # ResultList property object
    result_list_com = MagicMock()
    result_list_com.GetType.return_value = (0, False, True, "ResultList")  # is_array = True
    result_list_com.GetNumElements.return_value = 1

    # Step result
    step_result_com = MagicMock()
    step_result_com.GetType.return_value = (0, False, False, "StepResult")
    step_result_com.Exists.side_effect = lambda path, _options: (
        path in ["TS.StepName", "TS.StepType", "Status"]
    )
    step_result_com.GetValString.side_effect = lambda path, _options: {
        "TS.StepName": "Verify Power Rail",
        "TS.StepType": "PassFailTest",
        "Status": "Passed",
    }.get(path, "")

    result_list_com.GetPropertyObjectByOffset.return_value = step_result_com
    result_object_com.GetPropertyObject.return_value = result_list_com

    exec_com.ResultObject = result_object_com

    from py_teststand.execution.execution import Execution

    exec_obj = Execution(exec_com)

    res = exec_obj.result_list.parse()
    assert len(res) == 1
    assert res[0]["name"] == "Verify Power Rail"
    assert res[0]["type"] == "PassFailTest"
    assert res[0]["status"] == "Passed"


def test_sequence_context_result_list() -> None:
    context_com = MagicMock()

    # Configure Locals and Parameters mock COM
    locals_com = MagicMock()
    locals_com.GetType.return_value = (0, False, False, "Locals")
    locals_com.Exists.side_effect = lambda path, _options: path == "ResultList"

    result_list_com = MagicMock()
    result_list_com.GetType.return_value = (0, False, True, "ResultList")  # is_array = True
    result_list_com.GetNumElements.return_value = 1

    # Step result
    step_result_com = MagicMock()
    step_result_com.GetType.return_value = (0, False, False, "StepResult")
    step_result_com.Exists.side_effect = lambda path, _options: (
        path in ["TS.StepName", "TS.StepType", "Status"]
    )
    step_result_com.GetValString.side_effect = lambda path, _options: {
        "TS.StepName": "Verify Current",
        "TS.StepType": "NumericLimitTest",
        "Status": "Passed",
    }.get(path, "")

    result_list_com.GetPropertyObjectByOffset.return_value = step_result_com
    locals_com.GetPropertyObject.return_value = result_list_com

    context_com.Locals = locals_com
    context_com.Parameters = MagicMock()
    context_com.Parameters.Exists.return_value = False
    context_com.Sequence = None

    from py_teststand.sequence.sequence_context import SequenceContext

    ctx_obj = SequenceContext(context_com)

    res = ctx_obj.result_list.parse()
    assert len(res) == 1
    assert res[0]["name"] == "Verify Current"
    assert res[0]["type"] == "NumericLimitTest"
    assert res[0]["status"] == "Passed"
