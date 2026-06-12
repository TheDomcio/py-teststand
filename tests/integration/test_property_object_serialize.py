"""Live-engine tests for the PropertyObject JSON round-trip example.

The serializer in examples/property_object_serialize.py has to walk typedef'd
subcontainers and arrays of them. A typedef instance arrives over COM as an
IDispatch (VT_DISPATCH), so it must be recursed into structurally, not read as a
value. These tests build a real registered DigitalMultimeter type (the same way
data_type_create_custom.py does), put a single instance and an array of instances
into a sequence's Locals, and check that both serialize and round-trip.

Gated behind --run-teststand-engine.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

EXAMPLES_DIR = Path(__file__).resolve().parents[2] / "examples"

DIGITAL_MULTIMETER_DEFAULTS = {
    "Resolution": 6.5,
    "AutoZero": False,
    "Mode": "Voltage",
    "Range": 100.0,
}


def _load_example(name: str):
    spec = importlib.util.spec_from_file_location("example_" + name, EXAMPLES_DIR / (name + ".py"))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.teststand_engine
@pytest.mark.integration
def test_serializes_nested_typedef_and_array_of_typedefs():
    from py_teststand import Engine, PropertyOption, PropValType, TypeCategory

    serialize = _load_example("property_object_serialize")
    custom_type = _load_example("data_type_create_custom")
    insert = int(PropertyOption.InsertIfMissing)

    with Engine() as engine:
        sequence_file = engine.new_sequence_file()
        type_usage_list = sequence_file.as_property_object_file().type_usage_list
        data_type = custom_type._build_digital_multimeter_type(engine)
        type_usage_list.insert_type(
            data_type,
            type_usage_list.num_types,
            TypeCategory.CustomDataTypes,
        )

        sequence_locals = sequence_file.new_sequence("MainSequence").locals
        # One typedef instance as a nested subproperty.
        sequence_locals.new_sub_property(
            "Meter",
            PropValType.NamedType,
            False,
            "DigitalMultimeter",
            insert,
        )
        # An array of the same typedef.
        sequence_locals.new_sub_property(
            "Meters",
            PropValType.NamedType,
            True,
            "DigitalMultimeter",
            insert,
        )
        meters = sequence_locals.get_property_object("Meters", 0)
        assert meters is not None
        meters.set_num_elements(2, 0)
        second_meter = meters.get_property_object_by_offset(1, 0)
        assert second_meter is not None
        second_meter.set_val_string("Mode", insert, "Current")

        as_dict = serialize.property_object_to_dict(sequence_locals)

        # The nested typedef came across as a container and was recursed into,
        # not read as a single dispatch value.
        assert as_dict["Meter"] == DIGITAL_MULTIMETER_DEFAULTS

        # The array of typedefs serialized element by element.
        assert isinstance(as_dict["Meters"], list)
        assert len(as_dict["Meters"]) == 2
        assert as_dict["Meters"][0] == DIGITAL_MULTIMETER_DEFAULTS
        assert as_dict["Meters"][1]["Mode"] == "Current"

        # Rebuilding from the dict yields an equivalent structure.
        rebuilt = serialize.dict_to_property_object(engine, as_dict)
        assert serialize.property_object_to_dict(rebuilt) == as_dict


@pytest.mark.teststand_engine
@pytest.mark.integration
def test_example_round_trip_preserves_scalars_container_and_array():
    from py_teststand import Engine

    serialize = _load_example("property_object_serialize")

    with Engine() as engine:
        source = serialize._build_example_container(engine)
        as_dict = serialize.property_object_to_dict(source)

        assert as_dict["TestResult"] == 0.0
        assert as_dict["SerialNumber"] == "SN-001"
        assert as_dict["Passed"] is True
        assert as_dict["Readings"] == [1.5, 2.5, 3.5]
        assert as_dict["Instrument"]["Mode"] == "Voltage"
        assert [item["Mode"] for item in as_dict["Instruments"]] == ["Voltage", "Current"]

        rebuilt = serialize.dict_to_property_object(engine, as_dict)
        assert serialize.property_object_to_dict(rebuilt) == as_dict
