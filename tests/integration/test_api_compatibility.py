from __future__ import annotations

import pytest

from py_teststand import (
    Engine,
    SourceControlStatus,
    WorkspaceFile,
    WorkspaceObject,
    WorkspaceObjectType,
)


@pytest.fixture(scope="module")
def engine():

    eng = Engine()

    yield eng

    eng.release()


@pytest.mark.live_com
@pytest.mark.integration
def test_engine_version_info(engine: Engine):

    assert isinstance(engine.major_version, int)

    assert isinstance(engine.minor_version, int)

    assert isinstance(engine.revision_version, int)

    assert isinstance(engine.is_64bit, bool)

    assert isinstance(engine.application_version_string, str)

    assert engine.major_version >= 16


@pytest.mark.live_com
@pytest.mark.integration
def test_workspace_api_compatibility(engine: Engine):

    ws = engine.new_workspace_file()

    try:
        assert isinstance(ws, WorkspaceFile)

        assert ws.path == ""

        root = ws.root_workspace_object

        assert isinstance(root, WorkspaceObject)

        assert isinstance(root.object_type, WorkspaceObjectType)

        assert root.object_type == WorkspaceObjectType.WorkspaceFile

        assert isinstance(root.source_control_status, SourceControlStatus)

        assert isinstance(root.display_name, str)

    finally:
        pass


@pytest.mark.live_com
@pytest.mark.integration
def test_engine_directories(engine: Engine):

    assert isinstance(engine.bin_directory, str)

    assert isinstance(engine.config_directory, str)

    assert isinstance(engine.test_stand_directory, str)
