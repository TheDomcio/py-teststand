"""Insert LabVIEW VI-call steps into an existing sequence at a target location.

Opens the sequence file produced by build_sequence.py, navigates into
CustomSubsequence, locates the existing Initialize Hardware step,
constructs two LabVIEW Action steps that wrap real VIs from a packed
library / LabVIEW project, configures their ViCall paths, custom icon and
runtime mode, and inserts both steps directly in front of the target step.
Falls back to appending at the end of the step group if the target step
cannot be found.

Demonstrates:
- Opening existing sequence files with the with statement
- Looking up sequences and steps by name and reading step_index
- Creating steps with a real adapter (AdapterKeyName.LVAdapterKeyName)
- Configuring LabVIEW step module properties through the underlying
  PropertyObject (TS.SData.ViCall.VIPath, TS.SData.ViCall.ProjectPath)
- Setting the per-step icon (TS.Icon / Step.icon_name)
- Toggling the per-step run mode (TS.Mode / Step.run_mode) between
  Skip and Normal
- Inserting multiple steps at a computed index inside a StepGroup
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from py_teststand import Engine
from py_teststand.core.engine import AdapterKeyName
from py_teststand.core.exceptions import TestStandError
from py_teststand.sequence.step import RunMode
from py_teststand.sequence.step_group import StepGroup


def _new_vi_call_step(
    engine: Engine,
    name: str,
    vi_path: str,
    project_path: str = "",
    icon: str = "",
    run_mode: RunMode = RunMode.Normal,
):
    """Build a configured LabVIEW VI-call step ready for insertion."""
    step = engine.new_step(
        adapter_key_name=AdapterKeyName.LVAdapterKeyName,
        step_type_name="Action",
    )
    step.name = name

    step_po = step.as_property_object()
    step_po["TS.SData.ViCall.VIPath"] = vi_path
    if project_path:
        step_po["TS.SData.ViCall.ProjectPath"] = project_path
    if icon:
        step.icon_name = icon

    step.run_mode = run_mode
    return step


ROOT_TEMP_DIR = Path(tempfile.gettempdir()) / "py-teststand"
LATEST_POINTER = ROOT_TEMP_DIR / "latest_sequence.txt"


def main() -> None:
    if not LATEST_POINTER.exists():
        print(f"Error: Pointer file not found at {LATEST_POINTER}")
        print("Run build_sequence.py first.")
        return

    sequence_path = Path(LATEST_POINTER.read_text(encoding="utf-8").strip())

    if not sequence_path.exists():
        print(f"Error: Sequence file not found at {sequence_path}")
        return

    with Engine() as engine:
        with engine.get_sequence_file(str(sequence_path)) as seq_file:
            sub_sequence = seq_file.get_sequence_by_name("CustomSubsequence")

            voltage_step = _new_vi_call_step(
                engine,
                name="Voltage Monitor (VI)",
                vi_path=r"example.lvlibp\voltage_monitor.vi",
                project_path="Libraries.lvproj",
                icon="insert.ico",
                run_mode=RunMode.Skip,
            )

            temperature_step = _new_vi_call_step(
                engine,
                name="Temperature Check (VI)",
                vi_path=r"example.lvlibp\temperature_check.vi",
                icon="insert.ico",
                run_mode=RunMode.Normal,
            )

            target_step_group = StepGroup.Main
            target_step_name = "Initialize Hardware"

            try:
                target_step = sub_sequence.get_step_by_name(target_step_name, target_step_group)
                insert_index = target_step.step_index

                sub_sequence.insert_step(voltage_step, insert_index, target_step_group)
                sub_sequence.insert_step(temperature_step, insert_index + 1, target_step_group)

                print(
                    f"Success! Inserted '{voltage_step.name}' (mode={voltage_step.run_mode.name}) "
                    f"and '{temperature_step.name}' (mode={temperature_step.run_mode.name}) "
                    f"starting at index {insert_index}."
                )

            except TestStandError as e:
                print(f"Could not find target step '{target_step_name}'. Error: {e}")
                fallback_index = sub_sequence.get_num_steps(target_step_group)
                sub_sequence.insert_step(voltage_step, fallback_index, target_step_group)
                sub_sequence.insert_step(temperature_step, fallback_index + 1, target_step_group)
                print(f"Fallback: Appended both steps at end (starting index {fallback_index}).")

            seq_file.save()


if __name__ == "__main__":
    main()
