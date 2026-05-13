from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import IntEnum
from typing import TYPE_CHECKING, Any, Callable, Iterable

if TYPE_CHECKING:
    from py_teststand.analyzer.analysis_context import AnalysisContext, AnalysisTransition


class RuleSeverity(IntEnum):
    Error = 0
    Warning = 1
    Information = 2
    Default = 3
    Unknown = 4


logger = logging.getLogger(__name__)


RuleCallback = Callable[["AnalysisContext"], None]


@dataclass
class Rule:
    rule_id: str
    description: str
    callback: RuleCallback
    transitions: tuple[AnalysisTransition, ...] = field(default_factory=tuple)  # type: ignore[type-arg]
    default_severity: RuleSeverity = RuleSeverity.Warning
    enabled: bool = True

    def matches(self, transition: int) -> bool:
        if not self.transitions:
            return True
        from py_teststand.analyzer.analysis_context import AnalysisTransition

        try:
            actual = AnalysisTransition(int(transition))
        except ValueError:
            return False
        return actual in self.transitions

    def invoke(self, context: AnalysisContext) -> None:  # type: ignore[name-defined]
        if not self.enabled:
            return
        if not self.matches(int(context.transition)):
            return
        try:
            self.callback(context)
        except Exception:
            logger.exception("rule %s callback raised", self.rule_id)


_REGISTERED: dict[str, Rule] = {}


def rule(
    rule_id: str,
    *,
    description: str = "",
    transitions: Iterable[AnalysisTransition] | None = None,  # type: ignore[name-defined]
    severity: RuleSeverity = RuleSeverity.Warning,
    enabled: bool = True,
) -> Callable[[RuleCallback], Rule]:

    def decorator(func: RuleCallback) -> Rule:
        if rule_id in _REGISTERED:
            raise ValueError(f"rule id {rule_id!r} already registered")
        instance = Rule(
            rule_id=rule_id,
            description=description or (func.__doc__ or "").strip(),
            callback=func,
            transitions=tuple(transitions or ()),
            default_severity=severity,
            enabled=enabled,
        )
        _REGISTERED[rule_id] = instance
        return instance

    return decorator


def registered_rules() -> dict[str, Rule]:
    return dict(_REGISTERED)


def clear_registered_rules() -> None:
    _REGISTERED.clear()


def dispatch(com_context: Any) -> None:
    from py_teststand.analyzer.analysis_context import AnalysisContext

    if isinstance(com_context, AnalysisContext):
        context = com_context
    else:
        context = AnalysisContext(com_context)
    for rule_obj in _REGISTERED.values():
        rule_obj.invoke(context)


__all__ = [
    "Rule",
    "RuleCallback",
    "clear_registered_rules",
    "dispatch",
    "registered_rules",
    "rule",
]
