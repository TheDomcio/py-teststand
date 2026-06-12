"""Create a custom TestStand data type programmatically and store it in a sequence file.

A type can live in a type-palette file (such as MyTypes.ini) or in a specific file.
This example stores it in a sequence file (built the way sequence_build.py does) and
also enumerates the loaded type palettes with Engine.get_type_palette_file_list, which
is how you would reach a palette's TypeUsageList instead.

The type "DigitalMultimeter" has fields:
- Resolution (Number,  default 6.5)
- AutoZero   (Boolean, default False)
- Mode       (String,  default "Voltage")
- Range      (Number,  default 100)

Workflow:
- Engine.new_property_object(Container, ...) creates the container.
- set_val_number / set_val_boolean / set_val_string with PropertyOption.InsertIfMissing
  create each field and set its default value.
- The type's name comes from the container's `name`.
- TypeUsageList.insert_type registers it under TypeCategory.CustomDataTypes.
- PropertyObjectFile.inc_change_count + SequenceFile.save persist it.
"""

from __future__ import annotations

import tempfile
import uuid
from pathlib import Path

from py_teststand import Engine, PropertyOption, PropValType, TypeCategory

ROOT_TEMP_DIR = Path(tempfile.gettempdir()) / "py-teststand"
INSERT_IF_MISSING = int(PropertyOption.InsertIfMissing)


def _build_digital_multimeter_type(engine: Engine):
    """Build the DigitalMultimeter container type; field defaults define field types."""
    data_type = engine.new_property_object(PropValType.Container, False, "", 0)
    data_type.set_val_number("Resolution", INSERT_IF_MISSING, 6.5)
    data_type.set_val_boolean("AutoZero", INSERT_IF_MISSING, False)
    data_type.set_val_string("Mode", INSERT_IF_MISSING, "Voltage")
    data_type.set_val_number("Range", INSERT_IF_MISSING, 100.0)
    data_type.name = "DigitalMultimeter"
    return data_type


def main() -> None:
    run_dir = ROOT_TEMP_DIR / uuid.uuid4().hex
    run_dir.mkdir(parents=True, exist_ok=True)
    sequence_path = run_dir / "with_custom_type.seq"

    with Engine() as engine:
        # The other place data types can live: type-palette files such as MyTypes.ini.
        # To target one, find it here and use palette.type_usage_list instead.
        print("Loaded type-palette files:")
        for palette in engine.get_type_palette_file_list():
            print(f"  {palette.display_name}")

        sequence_file = engine.new_sequence_file()
        property_object_file = sequence_file.as_property_object_file()
        type_usage_list = property_object_file.type_usage_list

        data_type = _build_digital_multimeter_type(engine)
        type_usage_list.insert_type(
            data_type,
            type_usage_list.num_types,
            TypeCategory.CustomDataTypes,
        )
        property_object_file.inc_change_count()
        sequence_file.save(str(sequence_path))

        # Read the registered type back to confirm its fields and defaults.
        index = type_usage_list.get_type_index("DigitalMultimeter")
        definition = type_usage_list.get_type_definition(index)
        print(f"\nCreated data type 'DigitalMultimeter' (type index {index}):")
        print(f"  Resolution = {definition.get_val_number('Resolution', 0)}")
        print(f"  AutoZero   = {definition.get_val_boolean('AutoZero', 0)}")
        print(f"  Mode       = {definition.get_val_string('Mode', 0)!r}")
        print(f"  Range      = {definition.get_val_number('Range', 0)}")
        print(f"\nSaved sequence file with the type to {sequence_path}")


if __name__ == "__main__":
    main()
