from __future__ import annotations

import typing
from enum import IntEnum, IntFlag

from py_teststand.analyzer.analysis_message import AnalysisMessage
from py_teststand.analyzer.analysis_utilities import AnalysisUtilities
from py_teststand.analyzer.rule_configuration import RuleConfiguration
from py_teststand.core.com_wrapper import ts_interface
from py_teststand.property.property_object import PropertyObject


class AnalysisTransition(IntEnum):
    NoneValue = 0
    BeforeSystem = 1
    BeforeTypePalettes = 2
    BeforeTypePalette = 3
    AfterTypePalette = 4
    AfterTypePalettes = 5
    BeforeUsersFile = 6
    BeforeUsers = 7
    AfterUsers = 8
    BeforeUserGroups = 9
    AfterUserGroups = 10
    AfterUsersFile = 11
    BeforeStationGlobalsFile = 12
    BeforeStationGlobals = 13
    AfterStationGlobals = 14
    AfterStationGlobalsFile = 15
    BeforeTemplatesFile = 16
    BeforeTemplates = 17
    AfterTemplates = 18
    AfterTemplatesFile = 19
    BeforeWorkspaceFile = 20
    AfterWorkspaceFile = 21
    BeforeSequenceFile = 22
    BeforeSequenceFileGlobals = 23
    AfterSequenceFileGlobals = 24
    BeforeSequences = 25
    BeforeSequence = 26
    BeforeSequenceVariables = 27
    BeforeSequenceLocals = 28
    AfterSequenceLocals = 29
    BeforeSequenceParameters = 30
    AfterSequenceParameters = 31
    AfterSequenceVariables = 32
    BeforeSteps = 33
    BeforeSetupStepGroup = 34
    AfterSetupStepGroup = 35
    BeforeMainStepGroup = 36
    AfterMainStepGroup = 37
    BeforeCleanupStepGroup = 38
    AfterCleanupStepGroup = 39
    AfterSteps = 40
    AfterSequence = 41
    AfterSequences = 42
    AfterSequenceFile = 43
    AfterSystem = 44
    BeforeStep = 45
    AfterStep = 46
    BeforeFileTypes = 47
    AfterFileTypes = 48


class RuleAnalysisDataScope(IntEnum):
    Global = 0
    File = 1


class GetRuleAnalysisDataOption(IntFlag):
    NoneValue = 0x0
    Lock = 0x1


if typing.TYPE_CHECKING:
    from py_teststand.core.engine import Engine
    from py_teststand.property.property_object_file import PropertyObjectFile
    from py_teststand.sequence.sequence_context import SequenceContext


class AnalysisContext(PropertyObject):
    @property
    @ts_interface
    def analysis_id(self) -> int:
        return int(self._com_obj.AnalysisId)

    @property
    @ts_interface
    def edit_context(self) -> SequenceContext:
        from py_teststand.sequence.sequence_context import SequenceContext

        return SequenceContext(self._com_obj.EditContext, self._engine_ref)

    @property
    @ts_interface
    def engine(self) -> Engine:
        from py_teststand.core.engine import Engine

        return Engine(com_obj=self._com_obj.Engine)

    @property
    @ts_interface
    def file(self) -> PropertyObjectFile:
        from py_teststand.property.property_object_file import PropertyObjectFile

        return PropertyObjectFile(self._com_obj.File, self._engine_ref)

    @property
    @ts_interface
    def object(self) -> PropertyObject:
        return PropertyObject(self._com_obj.Object, self._engine_ref)

    @property
    @ts_interface
    def stop_requested(self) -> bool:
        return bool(self._com_obj.StopRequested)

    @property
    @ts_interface
    def transition(self) -> AnalysisTransition:
        return AnalysisTransition(int(self._com_obj.Transition))

    @property
    @ts_interface
    def utilities(self) -> AnalysisUtilities:
        return AnalysisUtilities(self._com_obj.Utilities, self._engine_ref)

    @ts_interface
    def get_rule_analysis_data(
        self,
        scope: RuleAnalysisDataScope | int,
        options: GetRuleAnalysisDataOption | int = (GetRuleAnalysisDataOption.NoneValue),
    ) -> PropertyObject:
        return PropertyObject(
            self._com_obj.GetRuleAnalysisData(int(scope), int(options)),
            self._engine_ref,
        )

    @ts_interface
    def get_rule_configuration(self, rule_id: str) -> RuleConfiguration:
        return RuleConfiguration(self._com_obj.GetRuleConfiguration(str(rule_id)), self._engine_ref)

    @ts_interface
    def new_message(
        self,
        rule_id: str,
        text: str,
        location_object: PropertyObject | None = None,
    ) -> AnalysisMessage:
        location_com = location_object._com_obj if location_object is not None else None
        return AnalysisMessage(
            self._com_obj.NewMessage(str(rule_id), str(text), location_com),
            self._engine_ref,
        )

    @ts_interface
    def report_message(self, message: AnalysisMessage) -> None:
        self._com_obj.ReportMessage(message._com_obj)

    @ts_interface
    def stop_analysis(self) -> None:
        self._com_obj.StopAnalysis()

    def report(
        self,
        rule_id: str,
        text: str,
        location_object: PropertyObject | None = None,
    ) -> AnalysisMessage:
        message = self.new_message(rule_id, text, location_object)
        self.report_message(message)
        return message


__all__ = ["AnalysisContext"]
