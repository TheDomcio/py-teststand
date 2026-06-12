"""Build a TestStand sequence file from scratch with NumericLimitTest steps.

Creates a new sequence file, populates MainSequence with two
NumericLimitTest steps (a temperature check and a voltage monitor) whose
high/low limits are configured through the underlying
PropertyObject, adds a CustomSubsequence containing an Action
step so downstream examples (step_insert.py) have something to target,
prints a verification summary of the constructed sequence, and writes
the file to a temp directory.

Demonstrates:
- Creating sequence files and adding subsequences with new_sequence
- Building steps with Engine.new_step (no adapter / None adapter)
- Setting standard step properties (name, precondition, record_result)
- Reaching into nested TestStand properties (Limits.High / Limits.Low)
  via step.as_property_object()
- Inserting steps into a specific StepGroup at a chosen index
"""

from __future__ import annotations

import tempfile
import uuid
from pathlib import Path

from py_teststand import Engine, StepGroup

ROOT_TEMP_DIR = Path(tempfile.gettempdir()) / "py-teststand"
LATEST_POINTER = ROOT_TEMP_DIR / "latest_sequence.txt"


def main() -> None:
    run_dir = ROOT_TEMP_DIR / uuid.uuid4().hex
    run_dir.mkdir(parents=True, exist_ok=True)
    output_path = run_dir / "test_sequence.seq"

    with Engine() as engine:
        sequence_file = engine.new_sequence_file()
        main_sequence = sequence_file.get_sequence_by_name("MainSequence")

        first_step = engine.new_step(adapter_key_name="", step_type_name="NumericLimitTest")
        first_step.name = "Temperature Check"
        first_step.precondition = "Locals.TempSensorPresent == True"
        first_step.record_result = True

        first_step_property_object = first_step.as_property_object()
        first_step_property_object["Limits.High"] = 85.0
        first_step_property_object["Limits.Low"] = 15.0

        main_sequence.insert_step(first_step, 0, StepGroup.Main)

        second_step = engine.new_step(adapter_key_name="", step_type_name="NumericLimitTest")
        second_step.name = "Voltage Monitor"
        second_step.precondition = "Locals.DUTPowered == True"

        second_step_property_object = second_step.as_property_object()
        second_step_property_object["Limits.High"] = 5.25
        second_step_property_object["Limits.Low"] = 4.75

        main_sequence.insert_step(second_step, 1, StepGroup.Main)

        sub_seq = engine.new_sequence()
        sub_seq.name = "CustomSubsequence"
        sequence_file.insert_sequence(sub_seq)

        init_step = engine.new_step(adapter_key_name="", step_type_name="Action")
        init_step.name = "Initialize Hardware"
        sub_seq.insert_step(init_step, 0, StepGroup.Main)

        print(f"Created sequence with {main_sequence.get_num_steps()} steps:")
        for i in range(main_sequence.get_num_steps()):
            s = main_sequence.get_step(i)
            po_s = s.as_property_object()

            print(f"  [{i}] {s.name}")
            print(f"      Limits: Low={po_s['Limits.Low']}, High={po_s['Limits.High']}")
            print(f"      Precond: {s.precondition}")

        sequence_file.save(str(output_path))
        LATEST_POINTER.write_text(str(output_path), encoding="utf-8")
        print(f"\nSaved sequence file to {output_path}")
        print(f"Pointer written to {LATEST_POINTER}")


if __name__ == "__main__":
    main()
