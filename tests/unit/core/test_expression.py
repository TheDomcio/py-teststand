from __future__ import annotations

from unittest.mock import MagicMock

from py_teststand.sequence.expression import EvaluationType, Expression


def test_evaluation_types_named_types():

    mock_com_obj = MagicMock()

    mock_com_obj.NamedTypes = ["Type1", "Type2"]

    et = EvaluationType(mock_com_obj, None)

    assert et.named_types == ["Type1", "Type2"]


def test_evaluation_types_array_of_named_types():

    mock_com_obj = MagicMock()

    mock_com_obj.ArrayOfNamedTypes = ["ArrayType1"]

    et = EvaluationType(mock_com_obj, None)

    assert et.array_of_named_types == ["ArrayType1"]


def test_expression_evaluate_with_options():

    from py_teststand.property.property_object import EvaluationOption

    mock_com_obj = MagicMock()

    mock_com_obj.Evaluate.return_value = "result"

    expr = Expression(mock_com_obj, None)

    _result = expr.evaluate("Locals.X", EvaluationOption.NoneValue)

    mock_com_obj.Evaluate.assert_called_once_with("Locals.X", 0)
