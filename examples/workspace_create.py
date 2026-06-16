"""Create a TestStand workspace containing a project and a built sequence file.

This example builds a small sequence file (the same way sequence_build.py does),
creates a project and a workspace on disk, nests the sequence under the project
and the project under the workspace, then saves all three files.

Demonstrates:
- Building and saving a sequence file with Engine.new_sequence_file / new_step
- Creating a project file with Engine.new_property_object_file(ProjectFile)
- Creating a workspace with Engine.new_workspace_file
- Nesting items: WorkspaceObject.new_file creates the object and
  WorkspaceObject.insert_object attaches it (workspace -> project -> sequence)
- Saving with PropertyObjectFile.write_file and
  WorkspaceFile.save_workspace_and_project_files
"""

from __future__ import annotations

import tempfile
import uuid
from pathlib import Path

from py_teststand import Engine, PropertyObjectFileType, StepGroup
from py_teststand.property.property_object_file import PropertyObjectFile
from py_teststand.sequence.sequence import Sequence
from py_teststand.sequence.sequence_file import SequenceFile
from py_teststand.sequence.step import Step
from py_teststand.workspace.workspace_file import WorkspaceFile
from py_teststand.workspace.workspace_object import WorkspaceObject

ROOT_TEMP_DIR: Path = Path(tempfile.gettempdir()) / "py-teststand"

# WriteFile takes a file-format version, not a writing-format enum; 1 is current.
CURRENT_FILE_FORMAT_VERSION = 1


def _build_sequence_file(engine: Engine, output_path: Path) -> None:
    """Build a MainSequence with two Action steps and save it to output_path."""
    sequence_file: SequenceFile = engine.new_sequence_file()
    main_sequence: Sequence = sequence_file.get_sequence_by_name(name="MainSequence")
    for name in ("Initialize Hardware", "Measure"):
        step: Step = engine.new_step(adapter_key_name="", step_type_name="Action")
        step.name = name
        main_sequence.insert_step(step, index=main_sequence.get_num_steps(), group=StepGroup.Main)
    sequence_file.save(path=str(object=output_path))


def main() -> None:
    run_dir: Path = ROOT_TEMP_DIR / uuid.uuid4().hex
    run_dir.mkdir(parents=True, exist_ok=True)
    sequence_path: Path = run_dir / "test_sequence.seq"
    project_path: Path = run_dir / "MyProject.tpj"
    workspace_path: Path = run_dir / "MyWorkspace.tsw"

    with Engine() as engine:
        _build_sequence_file(engine, output_path=sequence_path)

        # A project must exist on disk before it can be added to a workspace.
        project_file: PropertyObjectFile = engine.new_property_object_file(
            file_type=PropertyObjectFileType.ProjectFile
        )
        project_file.path = str(object=project_path)
        project_file.write_file(write_format=CURRENT_FILE_FORMAT_VERSION)

        workspace: WorkspaceFile = engine.new_workspace_file()
        workspace.as_property_object_file().path = str(workspace_path)
        root: WorkspaceObject = workspace.root_workspace_object

        # new_file() creates the workspace object; insert_object() attaches it to
        # its parent. Nest the project under the workspace, the sequence under it.
        project: WorkspaceObject = root.new_file(str(project_path))
        root.insert_object(object_to_insert=project, index=root.num_contained_objects)
        sequence_item: WorkspaceObject = project.new_file(path_string=str(sequence_path))
        project.insert_object(object_to_insert=sequence_item, index=project.num_contained_objects)

        # Persist the project file (now holding the sequence), then the workspace.
        project_data_file: PropertyObjectFile | None = project.project_file
        if project_data_file is not None:
            project_data_file.write_file(write_format=CURRENT_FILE_FORMAT_VERSION)
        workspace.as_property_object_file().write_file(write_format=CURRENT_FILE_FORMAT_VERSION)
        workspace.save_workspace_and_project_files()

        print(f"Workspace: {workspace_path}")
        for i in range(root.num_contained_objects):
            contained_project: WorkspaceObject = root.get_contained_object(index=i)
            print(f"  {contained_project.object_type.name}: {contained_project.display_name}")
            for j in range(contained_project.num_contained_objects):
                item: WorkspaceObject = contained_project.get_contained_object(index=j)
                print(f"    {item.object_type.name}: {item.display_name}")

        print("\nFiles written:")
        for label, path in (
            ("workspace", workspace_path),
            ("project", project_path),
            ("sequence", sequence_path),
        ):
            print(f"  {label:9} {'OK' if path.exists() else 'MISSING'}  {path}")


if __name__ == "__main__":
    main()
