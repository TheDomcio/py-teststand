"""Live-engine tests that run each example's ``main()`` against a real engine.

Examples double as documentation, so they must keep working. Running an example
on the live engine is a strong regression check: a renamed or hallucinated COM
member, a wrong argument order, or a broken signature raises here instead of
slipping past the docs. These are gated behind ``--run-teststand-engine``.

Two examples (variables_create, station_options_update) persist to the station
with ``commit_globals_to_disk``; that call is neutralised so the tests exercise
the example logic without modifying the developer's station configuration.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

EXAMPLES_DIR = Path(__file__).resolve().parents[2] / "examples"


def _load_example(name: str):
    spec = importlib.util.spec_from_file_location("example_" + name, EXAMPLES_DIR / (name + ".py"))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Examples whose main() is self-contained and side-effect-free beyond temp files.
_SELF_CONTAINED = [
    "sequence_build",
    "data_type_create_custom",
    "step_insert_from_template",
    "workspace_create",
    "users_manage",
    "analyzer_step_name_length",
    "property_object_serialize",
]


@pytest.mark.teststand_engine
@pytest.mark.integration
@pytest.mark.parametrize("name", _SELF_CONTAINED)
def test_example_main_runs_on_live_engine(name):
    _load_example(name).main()


@pytest.mark.teststand_engine
@pytest.mark.integration
def test_sequence_build_example_produces_valid_file():
    from py_teststand import Engine, StepGroup

    sequence_build = _load_example("sequence_build")
    sequence_build.main()

    pointer = sequence_build.LATEST_POINTER
    assert pointer.exists()
    saved_path = pointer.read_text(encoding="utf-8").strip()
    assert Path(saved_path).exists()

    with Engine() as engine:
        sequence_file = engine.get_sequence_file(saved_path)
        main_sequence = sequence_file.get_sequence_by_name("MainSequence")
        step_names = [
            main_sequence.get_step(i, StepGroup.Main).name
            for i in range(main_sequence.get_num_steps(StepGroup.Main))
        ]
        engine.release_sequence_file(sequence_file)

    assert "Temperature Check" in step_names
    assert "Voltage Monitor" in step_names


@pytest.mark.teststand_engine
@pytest.mark.integration
def test_step_insert_example_runs_on_live_engine():
    # step_insert opens the file sequence_build wrote (via LATEST_POINTER).
    _load_example("sequence_build").main()
    _load_example("step_insert").main()


@pytest.mark.teststand_engine
@pytest.mark.integration
def test_execution_run_subsequence_example_runs_on_live_engine():
    # Executes three None-adapter Action steps (no-ops) and reads the ResultList.
    # Run in a subprocess: the engine teardown after an execution currently aborts
    # the process (a known COM-apartment teardown defect, not an example bug), so
    # isolation keeps that crash from taking down the whole test session. Success
    # is judged by the per-step result output produced before teardown.
    import subprocess
    import sys

    completed = subprocess.run(
        [sys.executable, str(EXAMPLES_DIR / "execution_run_subsequence.py")],
        capture_output=True,
        text=True,
        timeout=180,
    )
    output = completed.stdout + completed.stderr
    # Each Action step ran and its recorded result was read back (Action steps
    # report status "Done"); this confirms the execution + ResultList walk worked.
    assert "Initialize: Done" in completed.stdout, output
    assert "Run Test: Done" in completed.stdout, output
    assert "Cleanup: Done" in completed.stdout, output


@pytest.mark.teststand_engine
@pytest.mark.integration
def test_execution_run_test_headless_example_runs_on_live_engine():
    # Runs NumericLimitTest steps (None adapter + DataSource expression) and reads
    # pass/fail + numeric. Subprocess-isolated for the same teardown reason as above.
    import subprocess
    import sys

    completed = subprocess.run(
        [sys.executable, str(EXAMPLES_DIR / "execution_run_test_headless.py")],
        capture_output=True,
        text=True,
        timeout=180,
    )
    output = completed.stdout + completed.stderr
    assert "Supply Voltage: Passed" in completed.stdout, output
    assert "Bias Current: Failed" in completed.stdout, output
    assert "Overall: FAILED" in completed.stdout, output


@pytest.mark.teststand_engine
@pytest.mark.integration
def test_ui_messages_handle_example_runs_on_live_engine():
    # Posts custom UI messages from Statement steps and receives them headless.
    # Subprocess-isolated for the same teardown reason as above.
    import subprocess
    import sys

    completed = subprocess.run(
        [sys.executable, str(EXAMPLES_DIR / "ui_messages_handle.py")],
        capture_output=True,
        text=True,
        timeout=180,
    )
    output = completed.stdout + completed.stderr
    assert "stage message" in completed.stdout, output
    assert "progress message" in completed.stdout, output
    assert "Both custom UI messages arrived" in completed.stdout, output


@pytest.mark.teststand_engine
@pytest.mark.integration
@pytest.mark.parametrize("name", ["variables_create", "station_options_update"])
def test_station_example_runs_without_persisting(name, monkeypatch):
    from py_teststand.core.engine.engine import Engine

    monkeypatch.setattr(Engine, "commit_globals_to_disk", lambda _self, *_args, **_kwargs: None)
    _load_example(name).main()
