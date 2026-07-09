"""Build in-memory templates and insert cloned copies into a sequence file.

The example creates step, sequence, and local-variable PropertyObject templates,
stores them in an in-memory template group, inserts cloned copies into a new
sequence file, and saves the file in a system temporary location without printing
that path.
"""

from __future__ import annotations

import tempfile
import uuid
from pathlib import Path

from py_teststand import (
    AdapterKeyName,
    Engine,
    GetSeqFileOption,
    PropertyObject,
    PropertyOption,
    PropValType,
    Sequence,
    SequenceFile,
    Step,
    StepGroup,
)

ROOT_TEMPORARY_DIRECTORY: Path = Path(tempfile.gettempdir()) / "py-teststand"
MAIN_SEQUENCE_NAME = "MainSequence"
STEP_TEMPLATE_NAME = "My_Custom_Step_Template"
SEQUENCE_TEMPLATE_NAME = "My_Custom_Sequence_Template"
VARIABLE_TEMPLATE_NAME = "My_Custom_Variable_Template"


def _create_sequence_file(engine: Engine, sequence_file_path: Path) -> None:
    """Create a sequence file with a MainSequence ready for template insertion."""
    sequence_file: SequenceFile = engine.new_sequence_file()
    sequence_file.save(str(sequence_file_path))


def _create_template_group(engine: Engine) -> PropertyObject:
    """Create an in-memory array container for the template PropertyObjects."""
    return engine.new_property_object(PropValType.Container, True, "", 0)


def _append_template_property_object(
    template_group: PropertyObject,
    template_property_object: PropertyObject,
) -> None:
    """Append a cloned PropertyObject to the in-memory template group."""
    insert_index = template_group.get_num_elements()
    template_group.set_num_elements(insert_index + 1, 0)
    template_group.set_property_object(
        f"[{insert_index}]",
        0,
        template_property_object.clone("", 0),
    )


def _create_step_template(engine: Engine) -> PropertyObject:
    """Create a Statement step template and return its PropertyObject."""
    step_template: Step = engine.new_step(AdapterKeyName.NoneAdapterKeyName, "Statement")
    step_template.name = STEP_TEMPLATE_NAME
    step_template.post_expression = 'Locals.Result = "Hello from step template!"'
    return step_template.as_property_object()


def _create_sequence_template(engine: Engine) -> PropertyObject:
    """Create a sequence template containing one Statement step."""
    sequence_template: Sequence = engine.new_sequence()
    sequence_template.name = SEQUENCE_TEMPLATE_NAME

    template_step: Step = engine.new_step(AdapterKeyName.NoneAdapterKeyName, "Statement")
    template_step.name = "Inside_Sequence_Template"
    sequence_template.insert_step(template_step, 0, StepGroup.Main)

    return sequence_template.as_property_object()


def _create_variable_template(engine: Engine) -> PropertyObject:
    """Create a string variable template and set its default value."""
    variable_template: PropertyObject = engine.new_property_object(PropValType.String, False, "", 0)
    variable_template.name = VARIABLE_TEMPLATE_NAME
    variable_template.set_val_string("", 0, "Template Variable Value")
    return variable_template


def _find_template_property_objects(
    template_group: PropertyObject,
) -> tuple[PropertyObject | None, PropertyObject | None, PropertyObject | None]:
    """Find the step, sequence, and variable templates by name."""
    step_property_object = None
    sequence_property_object = None
    variable_property_object = None

    template_count = template_group.get_num_elements()
    for template_index in range(template_count):
        template_property_object = template_group.get_property_object_by_offset(template_index, 0)
        if template_property_object is None:
            continue
        if template_property_object.name == STEP_TEMPLATE_NAME:
            step_property_object = template_property_object
        elif template_property_object.name == SEQUENCE_TEMPLATE_NAME:
            sequence_property_object = template_property_object
        elif template_property_object.name == VARIABLE_TEMPLATE_NAME:
            variable_property_object = template_property_object

    return step_property_object, sequence_property_object, variable_property_object


def _insert_template_copies(
    engine: Engine,
    sequence_file_path: Path,
    step_property_object: PropertyObject,
    sequence_property_object: PropertyObject,
    variable_property_object: PropertyObject,
) -> None:
    """Insert cloned template objects into the saved sequence file."""
    target_sequence_file: SequenceFile = engine.get_sequence_file_ex(
        str(sequence_file_path),
        GetSeqFileOption.DoNotRunLoadCallback,
    )
    target_sequence: Sequence = target_sequence_file.get_sequence_by_name(MAIN_SEQUENCE_NAME)

    print("Inserting step from template...")
    cloned_step_property_object = step_property_object.clone("", 0)
    inserted_step = Step(cloned_step_property_object._com_obj, engine)
    target_sequence.insert_step(inserted_step, 0, StepGroup.Main)

    print("Inserting sequence from template...")
    cloned_sequence_property_object = sequence_property_object.clone("", 0)
    inserted_sequence = Sequence(cloned_sequence_property_object._com_obj, engine)
    target_sequence_file.insert_sequence(inserted_sequence)

    print("Inserting local variable from template...")
    with target_sequence.locals as target_locals:
        target_locals.set_property_object(
            variable_property_object.name,
            int(PropertyOption.InsertIfMissing),
            variable_property_object.clone("", 0),
        )

    target_sequence_file.as_property_object_file().inc_change_count()
    target_sequence_file.save(str(sequence_file_path))


def main() -> None:
    run_directory: Path = ROOT_TEMPORARY_DIRECTORY / uuid.uuid4().hex
    run_directory.mkdir(parents=True, exist_ok=True)
    sequence_file_path: Path = run_directory / "template_test.seq"

    print("Initializing Engine...")
    with Engine() as engine:
        _create_sequence_file(engine, sequence_file_path)

        print("Creating in-memory template group...")
        template_group = _create_template_group(engine)

        print("Creating step template...")
        _append_template_property_object(template_group, _create_step_template(engine))

        print("Creating sequence template...")
        _append_template_property_object(template_group, _create_sequence_template(engine))

        print("Creating variable template...")
        _append_template_property_object(template_group, _create_variable_template(engine))

        step_property_object, sequence_property_object, variable_property_object = (
            _find_template_property_objects(template_group)
        )
        if (
            step_property_object is None
            or sequence_property_object is None
            or variable_property_object is None
        ):
            print("Error: Could not find all templates in the group.")
            return

        print("\nRe-opening sequence file to insert templates...")
        _insert_template_copies(
            engine,
            sequence_file_path,
            step_property_object,
            sequence_property_object,
            variable_property_object,
        )

    print("\nSuccess! All templates were created, cloned, inserted, and saved.")


if __name__ == "__main__":
    main()
