"""Edge-case tests for PropertyObject and ResultList covering missing branches."""

from __future__ import annotations

from unittest.mock import MagicMock

from py_teststand.execution.result_list import ResultList
from py_teststand.property.property_object import PropertyObject, PropValType


def test_property_object_getitem_returns_scalar_for_non_container():
    """Mock objects short-circuit __getitem__ to GetValVariant directly."""
    com = MagicMock()
    com.GetValVariant.return_value = 42

    property_object = PropertyObject(com)
    result = property_object["Status"]

    com.GetValVariant.assert_called_once_with("Status", 0)
    assert result == 42


def test_property_object_len_returns_sub_property_count():
    """__len__ returns GetNumSubProperties when the object is not an array."""
    com = MagicMock()
    # get_type returns (PropValType, is_named_type, is_array, type_name)
    com.GetType.return_value = (int(PropValType.Container), False, False, "")
    com.GetNumSubProperties.return_value = 5

    property_object = PropertyObject(com)
    assert len(property_object) == 5
    com.GetNumSubProperties.assert_called_once_with("")


def test_property_object_len_returns_num_elements_for_array():
    """__len__ returns GetNumElements when the object is an array."""
    com = MagicMock()
    com.GetType.return_value = (int(PropValType.Array), False, True, "")
    com.GetNumElements.return_value = 7

    property_object = PropertyObject(com)
    assert len(property_object) == 7
    com.GetNumElements.assert_called_once()


def test_property_object_iter_yields_sub_properties():
    """__iter__ yields PropertyObject instances via GetNthSubProperty for non-arrays."""
    com = MagicMock()
    com.GetType.return_value = (int(PropValType.Container), False, False, "")
    com.GetNumSubProperties.return_value = 2

    sub_com_0 = MagicMock(name="sub0")
    sub_com_1 = MagicMock(name="sub1")
    com.GetNthSubProperty.side_effect = [sub_com_0, sub_com_1]

    property_object = PropertyObject(com)
    items = list(property_object)

    assert len(items) == 2
    assert all(isinstance(item, PropertyObject) for item in items)
    assert items[0]._com_obj is sub_com_0
    assert items[1]._com_obj is sub_com_1


def test_property_object_iter_array_yields_elements():
    """__iter__ yields elements via GetPropertyObjectByOffset for arrays."""
    com = MagicMock()
    com.GetType.return_value = (int(PropValType.Array), False, True, "")
    com.GetNumElements.return_value = 3

    element_coms = [MagicMock(name=f"elem{i}") for i in range(3)]
    com.GetPropertyObjectByOffset.side_effect = element_coms

    property_object = PropertyObject(com)
    items = list(property_object)

    assert len(items) == 3
    assert all(isinstance(item, PropertyObject) for item in items)
    for i, item in enumerate(items):
        assert item._com_obj is element_coms[i]


def test_property_object_is_array_delegates_to_get_type():
    """is_array reads the third element of the tuple returned by get_type."""
    com_array = MagicMock()
    com_array.GetType.return_value = (int(PropValType.Array), False, True, "")
    assert PropertyObject(com_array).is_array is True

    com_scalar = MagicMock()
    com_scalar.GetType.return_value = (int(PropValType.Number), False, False, "")
    assert PropertyObject(com_scalar).is_array is False


def test_result_list_parse_empty_returns_empty_list():
    """ResultList.parse() returns [] when the array has zero elements."""
    com = MagicMock()
    # is_array must be True for _walk to proceed
    com.GetType.return_value = (int(PropValType.Array), False, True, "")
    com.GetNumElements.return_value = 0

    result_list = ResultList(PropertyObject(com))
    results = result_list.parse()

    assert results == []
