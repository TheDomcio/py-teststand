"""Round-trip a TestStand PropertyObject through a plain dict and a JSON file.

TestStand keeps variables, parameters, and custom data types as PropertyObjects: a
tree of named sub-properties. A sub-property can be a scalar (number, string,
boolean), a nested container (including a typedef such as the DigitalMultimeter
type from data_type_create_custom.py), or an array of any of those.

property_object_to_dict walks that tree into an ordinary dict; dict_to_property_object
rebuilds an equivalent PropertyObject. The walk asks PropertyObject.get_type what
each sub-property is, so containers and typedefs are recursed into by their fields
instead of being read as a value. A container arrives over COM as an IDispatch, so
reading it with get_val_variant would hand you a COM object, not data.
"""

from __future__ import annotations

import json
import tempfile
import uuid
from pathlib import Path
from typing import Any

from py_teststand import Engine, PropertyOption, PropValType

INSERT_IF_MISSING = int(PropertyOption.InsertIfMissing)
ROOT_TEMP_DIR = Path(tempfile.gettempdir()) / "py-teststand"


def property_object_to_dict(container: Any) -> dict[str, Any]:
    """Walk a container PropertyObject's sub-properties into a plain dict."""
    result: dict[str, Any] = {}
    for index in range(container.get_num_sub_properties("")):
        name = container.get_nth_sub_property_name("", index)
        result[name] = _to_python(container.get_property_object(name, 0))
    return result


def _to_python(obj: Any) -> Any:
    """Convert one sub-property object to a list (array), dict (container), or scalar."""
    value_type, _is_object, is_array, _type_name = obj.get_type("")
    if is_array:
        return [
            _to_python(obj.get_property_object_by_offset(offset, 0))
            for offset in range(obj.get_num_elements())
        ]
    if int(value_type) == int(PropValType.Container) or obj.get_num_sub_properties("") > 0:
        return property_object_to_dict(obj)
    if int(value_type) == int(PropValType.Boolean):
        return bool(obj.get_val_boolean("", 0))
    if int(value_type) == int(PropValType.Number):
        return obj.get_val_number("", 0)
    return obj.get_val_string("", 0)


def dict_to_property_object(engine: Engine, data: dict[str, Any], container: Any = None) -> Any:
    """Rebuild a container PropertyObject from a dict produced by the walk above."""
    if container is None:
        container = engine.new_property_object(PropValType.Container, False, "", 0)
    for name, value in data.items():
        _set_member(engine, container, name, value)
    return container


def _set_member(engine: Engine, container: Any, name: str, value: Any) -> None:
    """Create one sub-property (container, array, or scalar) from a Python value."""
    if isinstance(value, dict):
        container.new_sub_property(name, PropValType.Container, False, "", INSERT_IF_MISSING)
        dict_to_property_object(engine, value, container.get_property_object(name, 0))
    elif isinstance(value, list):
        items: list[Any] = value
        container.new_sub_property(name, _element_type(items), True, "", INSERT_IF_MISSING)
        array = container.get_property_object(name, 0)
        array.set_num_elements(len(items), 0)
        for offset, item in enumerate(items):
            if isinstance(item, dict):
                element = array.get_property_object_by_offset(offset, 0)
                dict_to_property_object(engine, item, element)
            elif isinstance(item, bool):
                array.set_val_boolean_by_offset(offset, 0, item)
            elif isinstance(item, (int, float)):
                array.set_val_number_by_offset(offset, 0, float(item))
            else:
                array.set_val_string_by_offset(offset, 0, str(item))
    elif isinstance(value, bool):
        container.set_val_boolean(name, INSERT_IF_MISSING, value)
    elif isinstance(value, (int, float)):
        container.set_val_number(name, INSERT_IF_MISSING, float(value))
    else:
        container.set_val_string(name, INSERT_IF_MISSING, str(value))


def _element_type(items: list[Any]) -> PropValType:
    """Pick an array's element type from its first item (TestStand arrays are homogeneous)."""
    first = items[0] if items else ""
    if isinstance(first, dict):
        return PropValType.Container
    if isinstance(first, bool):
        return PropValType.Boolean
    if isinstance(first, (int, float)):
        return PropValType.Number
    return PropValType.String


def _child(container: Any, name: str) -> Any:
    """Fetch a sub-property object, asserting it exists (keeps type-checkers happy)."""
    obj = container.get_property_object(name, 0)
    assert obj is not None
    return obj


def _build_example_container(engine: Engine) -> Any:
    """Scalars, a scalar array, a nested DigitalMultimeter container, and an array of them."""
    data = engine.new_property_object(PropValType.Container, False, "", 0)
    data.set_val_number("TestResult", INSERT_IF_MISSING, 0.0)
    data.set_val_string("SerialNumber", INSERT_IF_MISSING, "SN-001")
    data.set_val_boolean("Passed", INSERT_IF_MISSING, True)

    data.new_sub_property("Readings", PropValType.Number, True, "", INSERT_IF_MISSING)
    readings = _child(data, "Readings")
    readings.set_num_elements(3, 0)
    for offset, value in enumerate([1.5, 2.5, 3.5]):
        readings.set_val_number_by_offset(offset, 0, value)

    data.new_sub_property("Instrument", PropValType.Container, False, "", INSERT_IF_MISSING)
    instrument = _child(data, "Instrument")
    instrument.set_val_number("Resolution", INSERT_IF_MISSING, 6.5)
    instrument.set_val_boolean("AutoZero", INSERT_IF_MISSING, False)
    instrument.set_val_string("Mode", INSERT_IF_MISSING, "Voltage")
    instrument.set_val_number("Range", INSERT_IF_MISSING, 100.0)

    data.new_sub_property("Instruments", PropValType.Container, True, "", INSERT_IF_MISSING)
    instruments = _child(data, "Instruments")
    instruments.set_num_elements(2, 0)
    for offset, (resolution, mode) in enumerate([(6.5, "Voltage"), (4.5, "Current")]):
        element = _child_by_offset(instruments, offset)
        element.set_val_number("Resolution", INSERT_IF_MISSING, resolution)
        element.set_val_string("Mode", INSERT_IF_MISSING, mode)
    return data


def _child_by_offset(array: Any, offset: int) -> Any:
    """Fetch an array element object, asserting it exists (keeps type-checkers happy)."""
    element = array.get_property_object_by_offset(offset, 0)
    assert element is not None
    return element


def main() -> None:
    run_dir = ROOT_TEMP_DIR / uuid.uuid4().hex
    run_dir.mkdir(parents=True, exist_ok=True)
    json_path = run_dir / "property_object.json"

    with Engine() as engine:
        source = _build_example_container(engine)

        # Walk the PropertyObject into a dict and write it as JSON.
        as_dict = property_object_to_dict(source)
        json_path.write_text(json.dumps(as_dict, indent=2), encoding="utf-8")
        print(f"Wrote {json_path}")
        print(json.dumps(as_dict, indent=2))

        # Read the JSON back, rebuild a PropertyObject, and confirm it matches.
        loaded = json.loads(json_path.read_text(encoding="utf-8"))
        rebuilt = dict_to_property_object(engine, loaded)

        assert property_object_to_dict(rebuilt) == as_dict, "round-trip mismatch"
        print("\nRound-trip preserved scalars, the nested container, and the arrays.")


if __name__ == "__main__":
    main()
