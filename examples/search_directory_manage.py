"""Manage TestStand search directories via the Engine API.

TestStand uses search directories to locate code modules, sequences, and
configuration files. The Engine.search_directories property exposes these
as a collection. This script reads the station's configuration, resolves the
raw integer types to the SearchDirectoryType enum, and manipulates the
collection by adding, moving, and deleting entries.

Demonstrates:
- Reading the SearchDirectories collection from the Engine
- Mapping a raw integer type to the SearchDirectoryType enum
- Inserting a new search directory with specific attributes (disabled, subdirectories)
- Changing a directory's load order with move_search_directory
- Removing a directory from the collection
- Committing the changes to disk with commit_globals_to_disk
"""

from __future__ import annotations

import sys
from pathlib import Path

from py_teststand import Engine, SearchDirectoryType


def main() -> None:
    with Engine() as engine:
        search_directory_collection = engine.search_directories

        print(f"Total search directories: {search_directory_collection.count}")

        # Showcase iterating over them and reading attributes
        for index, search_directory in enumerate(search_directory_collection):
            # Try to map integer type to the official enum
            try:
                directory_type = SearchDirectoryType(search_directory.type)
                type_name = directory_type.name

                # Specifically showcase handling different types using the enum
                if directory_type == SearchDirectoryType.ExplicitDir:
                    type_string = "Explicit user directory (ExplicitDir)"
                elif directory_type in (
                    SearchDirectoryType.WindowsDir,
                    SearchDirectoryType.WindowsSystemDir,
                ):
                    type_string = f"OS-defined path ({type_name})"
                else:
                    type_string = type_name
            except ValueError:
                type_string = f"Unknown ({search_directory.type})"

            print(
                f"[{index}] Type: {type_string}, Path: '{search_directory.path}',\n"
                f"    Subdirs: {search_directory.search_subdirectories}, "
                f"Disabled: {search_directory.disabled}, "
                f"HiddenExcl: {search_directory.exclude_hidden_subdirectories},\n"
                f"    ExtRestrict: '{search_directory.file_extension_restrictions}', "
                f"ExtExcl: {search_directory.exclude_file_extension}"
            )

        # Showcase inserting a new directory
        print("\nInserting a new explicit search directory...")
        temporary_directory = Path(sys.executable).parent

        # Insert at the beginning (index 0)
        search_directory_collection.insert(
            path=str(temporary_directory),
            index=0,
            search_sub_dirs=True,
            file_ext_restrict="",
            exclude=False,
            disabled=False,
        )

        print(f"Total after insert: {search_directory_collection.count}")
        first_directory = search_directory_collection[0]
        print(
            f"New [0] Path: '{first_directory.path}', "
            f"Subdirs: {first_directory.search_subdirectories}"
        )

        # Manipulate attributes
        print("Disabling the new directory...")
        first_directory.disabled = True
        print(f"New [0] Disabled: {first_directory.disabled}")

        # Showcase move_search_directory
        print("Moving the new directory to index 1...")
        search_directory_collection.move_search_directory(0, 1)
        print(f"Directory at index 1 is now: '{search_directory_collection[1].path}'")

        # Showcase removing the directory we just added
        print("Removing the added directory to clean up...")
        search_directory_collection.remove(1)
        print(f"Total after cleanup: {search_directory_collection.count}")

        # TestStand typically saves search directories automatically at shutdown.
        # However, to ensure modifications are immediately committed to disk
        # (SearchDirectories.cfg) and available to other processes, force a commit:
        engine.commit_globals_to_disk(prompt_on_save_conflicts=False)
        print("Committed search directories configuration to disk.")


if __name__ == "__main__":
    main()
