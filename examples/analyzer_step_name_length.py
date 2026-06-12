"""This example builds a sequence the way sequence_build.py does, defines the rule
with the py_teststand.analyzer @rule framework, and drives it in process over the
sequence's steps with a small offline context. That lets you author and exercise
the rule logic without compiling and registering an analyzer module. The rule
callback itself is written exactly as it would be for a live AnalysisContext.

Demonstrates:
- Defining a rule with @rule (rule id, severity, the step transition it runs on)
- A rule callback shaped like an analyzer analysis module: read context.object
  (the step), check step.name length, and context.report(...) on a violation
- Driving the rule over every step of a built sequence and collecting violations
"""

from __future__ import annotations

from typing import Any, cast

from py_teststand import Engine, StepGroup
from py_teststand.analyzer import AnalysisContext, AnalysisTransition, RuleSeverity, rule

RULE_ID = "PyTS_CheckStepNameLength"
MAXIMUM_STEP_NAME_LENGTH = 15


@rule(
    RULE_ID,
    description=f"Step names must be {MAXIMUM_STEP_NAME_LENGTH} characters or fewer",
    transitions=(AnalysisTransition.BeforeStep,),
    severity=RuleSeverity.Warning,
)
def check_step_name_length(context: Any) -> None:
    """Report any step whose name is longer than MAXIMUM_STEP_NAME_LENGTH."""
    step = context.object
    name = step.name
    if len(name) > MAXIMUM_STEP_NAME_LENGTH:
        context.report(
            RULE_ID,
            f"Step name {name!r} is too long ({len(name)}). "
            f"The maximum is {MAXIMUM_STEP_NAME_LENGTH}.",
            step,
        )


class _Violation:
    def __init__(self, rule_id: str, text: str, location: Any) -> None:
        self.rule_id = rule_id
        self.text = text
        self.location = location


class _OfflineStepContext:
    """In-process stand-in for the analyzer-supplied AnalysisContext.

    Exposes the same surface a step-level rule uses (`object`, `transition`,
    `report`). During a real analysis the NI Sequence Analyzer passes a
    py_teststand.analyzer.AnalysisContext instead, whose `object` is the step.
    """

    def __init__(self, analyzed_object: Any) -> None:
        self.object = analyzed_object
        self.transition = AnalysisTransition.BeforeStep
        self.findings: list[_Violation] = []

    def report(self, rule_id: str, text: str, location_object: Any = None) -> None:
        self.findings.append(_Violation(rule_id, text, location_object))


def _build_sequence(engine: Engine):
    sequence_file = engine.new_sequence_file()
    main_sequence = sequence_file.get_sequence_by_name("MainSequence")
    for name in ("Init", "Temperature Check", "Measure Output Voltage Rail", "Cleanup"):
        step = engine.new_step(adapter_key_name="", step_type_name="Action")
        step.name = name
        main_sequence.insert_step(step, main_sequence.get_num_steps(), StepGroup.Main)
    return main_sequence


def main() -> None:
    with Engine() as engine:
        main_sequence = _build_sequence(engine)

        print(f"Rule {RULE_ID!r}: {check_step_name_length.description}\n")
        violations = 0
        for i in range(main_sequence.get_num_steps()):
            step = main_sequence.get_step(i)
            context = _OfflineStepContext(step)
            # The analyzer would pass a real AnalysisContext; the offline stand-in
            # provides the same surface the rule uses.
            check_step_name_length.invoke(cast("AnalysisContext", context))
            status = "VIOLATION" if context.findings else "ok"
            print(f"  [{status:9}] {step.name!r} (length {len(step.name)})")
            for finding in context.findings:
                print(f"               {finding.text}")
            violations += len(context.findings)
        print(f"\n{violations} violation(s) found.")


if __name__ == "__main__":
    main()
