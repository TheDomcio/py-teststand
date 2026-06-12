"""Clone a configured step "template" into a sequence.

TestStand's Templates pane (Engine.GetTemplatesFile) holds reusable step
prototypes that you build in the Sequence Editor. On a fresh station that pane
is empty, so this example builds its own configured prototype step the way
step_insert.py does, then uses the part of the workflow that applies to any
template source: PropertyObject.clone copies the prototype, Sequence.insert_step
places each copy, and Step.create_new_unique_step_id gives every copy its own
step ID instead of leaving it sharing the prototype's.

Demonstrates:
- Reading the Templates pane with Engine.get_templates_file
- Building and configuring a prototype LabVIEW VI-call step (see step_insert.py)
- Copying it with PropertyObject.clone and re-wrapping the copy as a Step
- Inserting clones into MainSequence and giving each a unique step ID
- Saving the resulting sequence file
"""

from __future__ import annotations

import tempfile
import uuid
from pathlib import Path

from py_teststand import (
    AdapterKeyName,
    Engine,
    GetTemplatesFileOption,
    RunMode,
    Step,
    StepGroup,
)

ROOT_TEMP_DIR = Path(tempfile.gettempdir()) / "py-teststand"


def _build_prototype_step(engine: Engine) -> Step:
    """Build one configured VI-call step to act as the template to clone."""
    step = engine.new_step(
        adapter_key_name=AdapterKeyName.LVAdapterKeyName,
        step_type_name="Action",
    )
    step.name = "Measure (VI)"

    step_properties = step.as_property_object()
    step_properties["TS.SData.ViCall.VIPath"] = r"example.lvlibp\measure.vi"
    step.run_mode = RunMode.Normal
    return step


def _clone_step(prototype: Step, engine: Engine) -> Step:
    """Copy a step through its PropertyObject and wrap the copy for insertion.

    Clone lives on PropertyObject, so the copy comes back on the PropertyObject
    interface. InsertStep still accepts it because COM resolves it to a step. To
    call step-only methods such as create_new_unique_step_id, fetch the inserted
    step back from the sequence (see main), which returns the Step interface.
    """
    cloned = prototype.as_property_object().clone()
    return Step(cloned._com_obj, engine)


def main() -> None:
    run_dir = ROOT_TEMP_DIR / uuid.uuid4().hex
    run_dir.mkdir(parents=True, exist_ok=True)
    sequence_path = run_dir / "from_template.seq"

    with Engine() as engine:
        # The Templates pane is where the Sequence Editor stores reusable step
        # prototypes. It is empty on a fresh station, so report what is there and
        # then fall back to a prototype we build ourselves.
        templates_file = engine.get_templates_file(GetTemplatesFileOption.LoadIfNotLoaded)
        templates_root = templates_file.data.get_property_object("Root")
        template_count = 0
        if templates_root is not None:
            template_steps = templates_root.get_property_object_by_offset(0)
            if template_steps is not None:
                template_count = template_steps.get_num_elements()
        print(f"Template steps defined on this station: {template_count}")

        prototype = _build_prototype_step(engine)

        sequence_file = engine.new_sequence_file()
        main_sequence = sequence_file.get_sequence_by_name("MainSequence")

        # Clone the prototype twice and insert both copies. Without
        # create_new_unique_step_id each clone would keep the prototype's step ID.
        for copy_number in (1, 2):
            insert_index = main_sequence.get_num_steps(StepGroup.Main)
            main_sequence.insert_step(_clone_step(prototype, engine), insert_index, StepGroup.Main)

            inserted = main_sequence.get_step(insert_index, StepGroup.Main)
            inserted.name = f"Measure {copy_number} (from template)"
            inserted.create_new_unique_step_id()

        sequence_file.save(str(sequence_path))

        print(f"\nMainSequence now has {main_sequence.get_num_steps()} steps:")
        for index in range(main_sequence.get_num_steps()):
            step = main_sequence.get_step(index, StepGroup.Main)
            print(f"  [{index}] {step.name}")
        print(f"\nSaved sequence file to {sequence_path}")


if __name__ == "__main__":
    main()
