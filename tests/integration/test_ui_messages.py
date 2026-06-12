"""Live-engine tests for headless UI-message handling.

The stress run executes in a subprocess (same isolation rationale as the
execution examples: a process that ran an execution can abort during final COM
teardown, after the work has completed). Success is judged by the OK marker
the helper prints once all of its assertions pass: 150 messages, none lost,
single-poster FIFO order, payloads intact, synchronous posts acknowledged
under load.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

HELPER = Path(__file__).resolve().parent / "_ui_message_stress.py"


@pytest.mark.teststand_engine
@pytest.mark.integration
def test_ui_message_stress_no_loss_in_order_acknowledged():
    completed = subprocess.run(
        [sys.executable, str(HELPER)],
        capture_output=True,
        text=True,
        timeout=300,
    )
    output = completed.stdout + completed.stderr
    assert "STRESS OK count=150 ordered=True" in completed.stdout, output
