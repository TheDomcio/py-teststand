"""Manage TestStand variables: create across every scope, then add and remove one.

Opens the sequence file produced by sequence_build.py and creates string
variables across the four standard TestStand scopes:

- Sequence Locals: per-call storage on MainSequence (Locals.OperatorName).
- Sequence Parameters: caller-supplied inputs on MainSequence (Parameters.DUTSerial).
- File Globals: shared across every sequence in the file (FileGlobals.BatchID).
- Station Globals: shared across every sequence file on this station, persisted
  via Engine.commit_globals_to_disk (StationInfo.StationName).

It also adds a second subsequence, MeasurementRoutine, with its own parameter and
local, so the example shows variables scoped per sequence rather than per file.

Finally it walks the full lifecycle of a throwaway variable. A property's value
type is fixed when it is created, so "changing the type" of a variable means
deleting it and recreating it with the new type, which is what the editor does
for you. The example creates Locals.TempScratch as a String, retypes it to a
Boolean and then a Number, clones the numeric variable into TempScratchCopy with
PropertyObject.clone, and removes both with PropertyObject.delete_sub_property.

Demonstrates:
- Creating sub-properties of any type via PropertyObject.new_sub_property + PropValType
- Reading and writing values with PropertyObject.__setitem__ / __getitem__
- Reaching Sequence.locals / Sequence.parameters / SequenceFile.file_globals / Engine.globals
- Adding subsequences with SequenceFile.new_sequence
- Changing a variable's type (delete + recreate)
- Cloning a variable (clone + set_property_object) and removing it (delete_sub_property)
- Committing station-globals changes to disk
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from py_teststand import Engine, PropertyOption, PropValType

INSERT_IF_MISSING = int(PropertyOption.InsertIfMissing)


def _ensure_string_var(container, name: str, value: str) -> None:
    """Create a scalar string sub-property and assign it if it does not exist."""
    if not container.exists(name, 0):
        container.new_sub_property(name, PropValType.String, False, "")
    container[name] = value


def _demonstrate_temp_variable(container) -> None:
    """Create a throwaway variable, retype it, clone it numeric, then remove both."""
    name = "TempScratch"
    clone_name = "TempScratchCopy"

    container.new_sub_property(name, PropValType.String, False, "", INSERT_IF_MISSING)
    container[name] = "scratch"
    print(f"  created {name}: type={container.get_type(name)[0].name} value={container[name]!r}")

    # A property's value type is fixed at creation, so retyping is delete + recreate.
    container.delete_sub_property(name, 0)
    container.new_sub_property(name, PropValType.Boolean, False, "", INSERT_IF_MISSING)
    container.set_val_boolean(name, 0, True)
    print(f"  retyped {name} -> Boolean = {container.get_val_boolean(name, 0)}")

    # Retype once more to Number so the clone made from it is numeric.
    container.delete_sub_property(name, 0)
    container.new_sub_property(name, PropValType.Number, False, "", INSERT_IF_MISSING)
    container.set_val_number(name, 0, 42.0)
    print(f"  retyped {name} -> Number = {container.get_val_number(name, 0)}")

    # Duplicate it: clone copies the value and type, then attach under a new name.
    container.set_property_object(clone_name, INSERT_IF_MISSING, container.clone(name, 0))
    clone_type = container.get_type(clone_name)[0].name
    clone_value = container.get_val_number(clone_name, 0)
    print(f"  cloned {name} -> {clone_name}: type={clone_type} value={clone_value}")

    container.delete_sub_property(clone_name, 0)
    container.delete_sub_property(name, 0)
    print(
        f"  removed both: {name} exists={container.exists(name, 0)}, "
        f"{clone_name} exists={container.exists(clone_name, 0)}"
    )


ROOT_TEMP_DIR = Path(tempfile.gettempdir()) / "py-teststand"
LATEST_POINTER = ROOT_TEMP_DIR / "latest_sequence.txt"


def main() -> None:
    if not LATEST_POINTER.exists():
        print(f"Error: Pointer file not found at {LATEST_POINTER}")
        print("Run sequence_build.py first.")
        return

    sequence_path = Path(LATEST_POINTER.read_text(encoding="utf-8").strip())

    if not sequence_path.exists():
        print(f"Error: Sequence file not found at {sequence_path}")
        return

    with Engine() as engine:
        with engine.get_sequence_file(str(sequence_path)) as seq_file:
            main_sequence = seq_file.get_sequence_by_name("MainSequence")

            with main_sequence.locals as main_locals:
                _ensure_string_var(main_locals, "OperatorName", "Alice")

            with main_sequence.parameters as main_params:
                _ensure_string_var(main_params, "DUTSerial", "SN-000000")

            with seq_file.file_globals as file_globals:
                _ensure_string_var(file_globals, "BatchID", "BATCH-2026-Q2-001")

            measurement_seq = seq_file.new_sequence("MeasurementRoutine")
            with measurement_seq.parameters as measurement_params:
                _ensure_string_var(measurement_params, "ChannelLabel", "CH-A")
            with measurement_seq.locals as measurement_locals:
                _ensure_string_var(measurement_locals, "LastReading", "")

            seq_file.save()

            print("Variables created:")
            with main_sequence.locals as ml:
                print(f"  MainSequence.Locals.OperatorName     = {ml['OperatorName']!r}")
            with main_sequence.parameters as mp:
                print(f"  MainSequence.Parameters.DUTSerial    = {mp['DUTSerial']!r}")
            with seq_file.file_globals as fg:
                print(f"  FileGlobals.BatchID                  = {fg['BatchID']!r}")
            with measurement_seq.parameters as msp:
                print(f"  MeasurementRoutine.Parameters.Channel= {msp['ChannelLabel']!r}")
            with measurement_seq.locals as msl:
                print(f"  MeasurementRoutine.Locals.LastReading= {msl['LastReading']!r}")

            print("\nTemporary variable lifecycle (Locals.TempScratch):")
            with main_sequence.locals as scratch_locals:
                _demonstrate_temp_variable(scratch_locals)

        with engine.globals as station_globals:
            if not station_globals.exists("StationInfo", 0):
                station_globals.new_sub_property("StationInfo", PropValType.Container, False, "")
            station_info = station_globals.get_property_object("StationInfo", 0)
            assert station_info is not None
            with station_info as info:
                _ensure_string_var(info, "StationName", "STATION_01")
                print(f"\n  StationGlobals.StationInfo.StationName = {info['StationName']!r}")

        engine.commit_globals_to_disk(prompt_on_save_conflicts=False)


if __name__ == "__main__":
    main()
