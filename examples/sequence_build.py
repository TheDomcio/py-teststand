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

from py_teststand import Engine, PropertyObject, Sequence, SequenceFile, Step, StepGroup

ROOT_TEMP_DIR: Path = Path(tempfile.gettempdir()) / "py-teststand"
LATEST_POINTER: Path = ROOT_TEMP_DIR / "latest_sequence.txt"


def main() -> None:
    run_dir: Path = ROOT_TEMP_DIR / uuid.uuid4().hex
    run_dir.mkdir(parents=True, exist_ok=True)
    output_path: Path = run_dir / "test_sequence.seq"

    with Engine() as engine:
        sequence_file: SequenceFile = engine.new_sequence_file()
        main_sequence: Sequence = sequence_file.get_sequence_by_name("MainSequence")

        first_step: Step = engine.new_step(adapter_key_name="", step_type_name="NumericLimitTest")
        first_step.name = "Temperature Check"
        first_step.precondition = "Locals.TempSensorPresent == True"
        first_step.record_result = True

        first_step_property_object: PropertyObject = first_step.as_property_object()
        first_step_property_object["Limits.High"] = 85.0
        first_step_property_object["Limits.Low"] = 15.0

        main_sequence.insert_step(first_step, index=0, group=StepGroup.Main)

        second_step: Step = engine.new_step(adapter_key_name="", step_type_name="NumericLimitTest")
        second_step.name = "Voltage Monitor"
        second_step.precondition = "Locals.DUTPowered == True"

        second_step_property_object: PropertyObject = second_step.as_property_object()
        second_step_property_object["Limits.High"] = 5.25
        second_step_property_object["Limits.Low"] = 4.75

        main_sequence.insert_step(second_step, index=1, group=StepGroup.Main)

        subsequence: Sequence = engine.new_sequence()
        subsequence.name = "CustomSubsequence"
        sequence_file.insert_sequence(sequence=subsequence)

        init_step: Step = engine.new_step(adapter_key_name="", step_type_name="Action")
        init_step.name = "Initialize Hardware"
        subsequence.insert_step(init_step, index=0, group=StepGroup.Main)

        print(f"Created sequence with {main_sequence.get_num_steps()} steps:")
        for i in range(main_sequence.get_num_steps()):
            s: Step = main_sequence.get_step(index=i)
            po_s: PropertyObject = s.as_property_object()

            print(f"  [{i}] {s.name}")
            print(f"      Limits: Low={po_s['Limits.Low']}, High={po_s['Limits.High']}")
            print(f"      Precond: {s.precondition}")

        sequence_file.save(path=str(object=output_path))
        LATEST_POINTER.write_text(data=str(object=output_path), encoding="utf-8")
        print(f"\nSaved sequence file to {output_path}")
        print(f"Pointer written to {LATEST_POINTER}")


if __name__ == "__main__":
    main()
