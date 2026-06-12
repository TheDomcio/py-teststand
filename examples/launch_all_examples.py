from __future__ import annotations

import subprocess
import sys
from pathlib import Path

EXAMPLES_DIR: Path = Path(__file__).resolve().parent

# Script name, and what it does / how it relates to the rest.
EXAMPLES: list[tuple[str, str]] = [
    ("station_options_update", "Set station and debug options. Start here."),
    ("variables_create", "Add Locals and Parameters to a sequence."),
    ("data_type_create_custom", "Define a DigitalMultimeter custom data type."),
    ("property_object_serialize", "Dump variables and typedefs to JSON and back."),
    ("sequence_build", "Build a sequence file with steps and save it."),
    ("step_insert", "Insert a step into the sequence sequence_build made."),
    ("step_insert_from_template", "Add a step from a step-type template."),
    ("analyzer_step_name_length", "Walk a sequence and report on its step names."),
    ("workspace_create", "Create a workspace and project file."),
    ("users_manage", "Create users and set their privileges."),
    ("execution_run_test_headless", "Run real pass/fail tests and read their numeric results."),
    ("ui_messages_handle", "Receive UI messages from a running sequence without a GUI."),
    (
        "execution_run_subsequence",
        "Run a sequence and read its results. Last; it shuts the engine down.",
    ),
]


def main() -> None:
    for number, (name, note) in enumerate(EXAMPLES, start=1):
        print(f"\n[{number}/{len(EXAMPLES)}] {name}: {note}")
        result: subprocess.CompletedProcess[bytes] = subprocess.run(
            [sys.executable, str(EXAMPLES_DIR / f"{name}.py")],
        )
        print("    ok" if result.returncode == 0 else f"    exited with code {result.returncode}")


if __name__ == "__main__":
    main()
