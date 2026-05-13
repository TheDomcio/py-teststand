from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from py_teststand.analyzer import (
    AnalysisContext,
    AnalysisTransition,
    Rule,
    RuleSeverity,
    clear_registered_rules,
    dispatch,
    registered_rules,
    rule,
)


@pytest.fixture(autouse=True)
def _reset_registry():

    clear_registered_rules()

    yield

    clear_registered_rules()


def _ctx_for(transition_value: int) -> AnalysisContext:

    com = MagicMock()

    com.Transition = transition_value

    com.NewMessage.return_value = MagicMock()

    return AnalysisContext(com)


def test_rule_decorator_registers_with_metadata():

    @rule(
        "PY_FirstRule",
        description="example",
        transitions=[AnalysisTransition.BeforeStep],
        severity=RuleSeverity.Error,
    )
    def cb(_ctx):

        pass

    assert isinstance(cb, Rule)

    assert cb.rule_id == "PY_FirstRule"

    assert cb.default_severity == RuleSeverity.Error

    assert "PY_FirstRule" in registered_rules()


def test_duplicate_rule_id_raises():

    @rule("DUP")
    def cb(_ctx):

        pass

    with pytest.raises(ValueError):

        @rule("DUP")
        def cb2(_ctx):

            pass


def test_dispatch_filters_by_transition():

    seen: list[int] = []

    @rule("BS", transitions=[AnalysisTransition.BeforeStep])
    def cb(ctx):

        seen.append(int(ctx.transition))

    dispatch(_ctx_for(AnalysisTransition.AfterStep))

    assert seen == []

    dispatch(_ctx_for(AnalysisTransition.BeforeStep))

    assert seen == [int(AnalysisTransition.BeforeStep)]


def test_dispatch_invokes_unfiltered_rule_for_any_transition():

    seen: list[int] = []

    @rule("ALL")
    def cb(ctx):

        seen.append(int(ctx.transition))

    dispatch(_ctx_for(AnalysisTransition.BeforeSystem))

    dispatch(_ctx_for(AnalysisTransition.AfterSystem))

    assert seen == [
        int(AnalysisTransition.BeforeSystem),
        int(AnalysisTransition.AfterSystem),
    ]


def test_callback_exception_does_not_break_other_rules():

    second_called: list[bool] = []

    @rule("BAD")
    def bad(_ctx):

        raise RuntimeError("boom")

    @rule("GOOD")
    def good(_ctx):

        second_called.append(True)

    dispatch(_ctx_for(AnalysisTransition.BeforeStep))

    assert second_called == [True]


def test_disabled_rule_skipped():

    seen: list[int] = []

    @rule("OFF", enabled=False)
    def cb(_ctx):

        seen.append(1)

    dispatch(_ctx_for(AnalysisTransition.BeforeStep))

    assert seen == []


def test_context_report_helper_builds_and_reports_message():

    com = MagicMock()

    com.Transition = AnalysisTransition.BeforeStep

    new_msg_com = MagicMock()

    com.NewMessage.return_value = new_msg_com

    ctx = AnalysisContext(com)

    msg = ctx.report("missing precondition", rule_id="PY_Pre")

    assert msg.text == "missing precondition" or new_msg_com.Text == "missing precondition"

    com.ReportMessage.assert_called_once_with(new_msg_com)
