from __future__ import annotations

from enum import IntEnum


class StepGroup(IntEnum):
    Setup = 0
    Main = 1
    Cleanup = 2


class StepGroupMode(IntEnum):
    OneGroup = 1
    AllGroups = 2
