from __future__ import annotations

import gc

import pytest

from py_teststand import Engine


@pytest.mark.live_com
@pytest.mark.integration
def test_engine_teardown_loop():

    for _ in range(5):
        engine = Engine()

        assert engine.version_string is not None

        engine.release()

        del engine

        gc.collect()


@pytest.mark.live_com
@pytest.mark.integration
def test_child_object_weakref_to_engine():

    engine = Engine()

    ws = engine.new_workspace_file()

    root = ws.root_workspace_object

    assert root.engine is engine

    del engine

    gc.collect()

    assert root.engine is None

    assert ws.engine is None


@pytest.mark.live_com
@pytest.mark.integration
def test_multiple_release_idempotency():

    engine = Engine()

    engine.release()

    engine.release()

    engine.release()
