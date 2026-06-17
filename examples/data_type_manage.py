"""Create and evolve custom TestStand data types in a sequence file.

A custom data type can be a Number, Enumeration, String, Boolean, Object
Reference, Container, or an n-dimensional array of those. This example registers
two of them in a sequence file and then evolves one, which is the part that
matters in practice: a type ships, instances of it exist, and later you need to
change the type without breaking those instances.

It builds:
- DigitalMultimeter, a container type (Resolution, AutoZero, Mode, Range).
- Coupling, a strict enumeration (AC = 0, DC = 1). Strict means a variable of
  this type only accepts the defined enumerators, which is the default in the
  sequence editor, so the example sets it explicitly.

Then it evolves Coupling: prints the current TypeVersion, adds a GND enumerator,
and bumps the minor version (0.0.0.0 to 0.1.0.0). TestStand type versions are
"major.minor.revision.build". A bump of the build field (the lowest) signals an
automatic conversion that updates instances silently; bumping a higher field
like minor marks a deliberate change. UpdateEnumerators updates every loaded
instance of the type, so the InputCoupling variable created here reflects the
new enumerator immediately.
"""

from __future__ import annotations

import tempfile
import uuid
from pathlib import Path

from py_teststand import (
    Engine,
    PropertyObject,
    PropertyOption,
    PropValType,
    TypeCategory,
    TypeUsageList,
)

ROOT_TEMP_DIR: Path = Path(tempfile.gettempdir()) / "py-teststand"
INSERT_IF_MISSING = int(PropertyOption.InsertIfMissing)
COERCE_TO_NUMBER = int(PropertyOption.CoerceToNumber)


def _build_digital_multimeter_type(engine: Engine) -> PropertyObject:
    """Build the DigitalMultimeter container type; field defaults define field types."""
    data_type: PropertyObject = engine.new_property_object(
        value_type=PropValType.Container, as_array=False, type_name_param="", options=0
    )
    data_type.set_val_number(lookup_string="Resolution", options=INSERT_IF_MISSING, value=6.5)
    data_type.set_val_boolean(lookup_string="AutoZero", options=INSERT_IF_MISSING, value=False)
    data_type.set_val_string(lookup_string="Mode", options=INSERT_IF_MISSING, value="Voltage")
    data_type.set_val_number(lookup_string="Range", options=INSERT_IF_MISSING, value=100.0)
    data_type.name = "DigitalMultimeter"
    return data_type


def _enumerator_array(
    engine: Engine, named_values: list[tuple[str, float]], *, strict: bool
) -> PropertyObject:
    """Build the array UpdateEnumerators expects: one container per enumerator.

    Each element carries EnumeratorName and EnumeratorValue. IsStrict rides along
    as a boolean attribute on the array, not as a sub-property.
    """
    array: PropertyObject = engine.new_property_object(PropValType.Container, True, "", 0)
    array.set_num_elements(len(named_values), 0)
    for index, (name, value) in enumerate(named_values):
        element = array.get_property_object_by_offset(index, 0)
        assert element is not None
        element.set_val_string("EnumeratorName", INSERT_IF_MISSING, name)
        element.set_val_number("EnumeratorValue", INSERT_IF_MISSING, value)
    array.attributes.set_val_boolean("TestStand.Enum.IsStrict", INSERT_IF_MISSING, strict)
    return array


def _register_enum(
    engine: Engine,
    type_usage_list: TypeUsageList,
    name: str,
    named_values: list[tuple[str, float]],
    *,
    strict: bool,
) -> PropertyObject:
    """Register an empty enumeration type, then set its enumerators on the root definition."""
    enum_type = engine.new_property_object(PropValType.Enum, False, "", 0)
    enum_type.name = name
    type_usage_list.insert_type(enum_type, type_usage_list.num_types, TypeCategory.CustomDataTypes)
    # UpdateEnumerators only works on the registered root definition, not the loose object.
    definition = type_usage_list.get_type_definition(type_usage_list.get_type_index(name))
    definition.update_enumerators(_enumerator_array(engine, named_values, strict=strict))
    return definition


def _print_enumerators(definition: PropertyObject) -> None:
    enumerators = definition.enumerators
    assert enumerators is not None
    strict = enumerators.attributes.get_val_boolean("TestStand.Enum.IsStrict", 0)
    print(f"  {definition.name} v{definition.type_version} (strict={strict}):")
    for index in range(enumerators.get_num_elements()):
        element = enumerators.get_property_object_by_offset(index, 0)
        assert element is not None
        value = int(element.get_val_number("", COERCE_TO_NUMBER))
        print(f"    {element.get_value_display_name('', 0)} -> {value}")


def main() -> None:
    run_dir = ROOT_TEMP_DIR / uuid.uuid4().hex
    run_dir.mkdir(parents=True, exist_ok=True)
    sequence_path = run_dir / "with_custom_types.seq"

    with Engine() as engine:
        sequence_file = engine.new_sequence_file()
        property_object_file = sequence_file.as_property_object_file()
        type_usage_list = property_object_file.type_usage_list

        type_usage_list.insert_type(
            _build_digital_multimeter_type(engine),
            type_usage_list.num_types,
            TypeCategory.CustomDataTypes,
        )
        coupling = _register_enum(
            engine, type_usage_list, "Coupling", [("AC", 0), ("DC", 1)], strict=True
        )

        # A variable typed as the enum, so the type change below has an instance to update.
        main_sequence = sequence_file.get_sequence_by_name("MainSequence")
        main_sequence.locals.new_sub_property(
            "InputCoupling", PropValType.NamedType, False, "Coupling", INSERT_IF_MISSING
        )

        property_object_file.inc_change_count()
        sequence_file.save(str(sequence_path))
        print("Registered custom data types:")
        _print_enumerators(coupling)

        # Evolve the type: read the current version, add an enumerator, bump minor.
        print(f"\nCoupling version before update: {coupling.type_version}")
        coupling.update_enumerators(
            _enumerator_array(engine, [("AC", 0), ("DC", 1), ("GND", 2)], strict=True)
        )
        major, minor, *_rest = (coupling.type_version + ".0.0.0").split(".")
        coupling.type_version = f"{int(major)}.{int(minor) + 1}.0.0"
        print(f"Coupling version after  update: {coupling.type_version}")

        property_object_file.inc_change_count()
        sequence_file.save(path=str(object=sequence_path))

        print("\nCoupling now defines (the InputCoupling variable reflects this):")
        _print_enumerators(definition=coupling)
        print(f"\nSaved sequence file with the evolved types to {sequence_path}")


if __name__ == "__main__":
    main()
