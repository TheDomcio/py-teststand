"""Create string variables across every TestStand variable scope.

Opens the sequence file produced by sequence_build.py and populates it
with new string variables across the four standard TestStand scopes:

- **Sequence Locals** — temporary per-call storage on MainSequence
  (Locals.OperatorName).
- **Sequence Parameters** — caller-supplied inputs on MainSequence
  (Parameters.DUTSerial).
- **File Globals** — values shared across every sequence in the file
  (FileGlobals.BatchID).
- **Station Globals** — values shared across every sequence file run on
  this station, persisted via Engine.commit_globals_to_disk
  (StationInfo.StationName).

Also adds a second subsequence MeasurementRoutine with its own
parameter and local so the example shows how variables are scoped per
sequence rather than per file.

Demonstrates:
- Creating sub-properties of arbitrary type via
  PropertyObject.new_sub_property + PropValType
- Reading and writing values with PropertyObject.__setitem__ / __getitem__
- Reaching Sequence.locals / Sequence.parameters /
  SequenceFile.file_globals / Engine.globals
- Adding subsequences with SequenceFile.new_sequence
- Committing station-globals changes to disk
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from py_teststand import Engine, PropValType


def _ensure_string_var(container, name: str, value: str) -> None:
    """Create a scalar string sub-property and assign it if it does not exist."""
    if not container.exists(name, 0):
        container.new_sub_property(name, PropValType.String, False, "")
    container[name] = value


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

        with engine.globals as station_globals:
            if not station_globals.exists("StationInfo", 0):
                station_globals.new_sub_property("StationInfo", PropValType.Container, False, "")
            station_info = station_globals.get_property_object("StationInfo", 0)
            assert station_info is not None
            with station_info as info:
                _ensure_string_var(info, "StationName", "STATION_01")
                print(f"  StationGlobals.StationInfo.StationName = {info['StationName']!r}")

        engine.commit_globals_to_disk(prompt_on_save_conflicts=False)


if __name__ == "__main__":
    main()
