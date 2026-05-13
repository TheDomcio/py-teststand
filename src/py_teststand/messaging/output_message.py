from __future__ import annotations

import typing
from enum import IntEnum

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.sequence.location import Locations


class ResourceUsageOutputMessageSubProperties:
    OutputMessageSubProperty_BatchType = "ResourceUsage.BatchType"
    OutputMessageSubProperty_ExecutionDisplayName = "ResourceUsage.ExecutionDisplayName"
    OutputMessageSubProperty_ExecutionId = "ResourceUsage.ExecutionId"
    OutputMessageSubProperty_FromProcessModel = "ResourceUsage.FromProcessModel"
    OutputMessageSubProperty_Operation = "ResourceUsage.Operation"
    OutputMessageSubProperty_ResourceAlternativeIndex = "ResourceUsage.ResourceAlternativeIndex"
    OutputMessageSubProperty_ResourceName = "ResourceUsage.ResourceName"
    OutputMessageSubProperty_SocketCount = "ResourceUsage.TestSockets.Count"
    OutputMessageSubProperty_SocketIndex = "ResourceUsage.TestSockets.MyIndex"
    OutputMessageSubProperty_SynchronizationMechanism = "SynchronizationMechanism"
    OutputMessageSubProperty_SynchronizationState = "ResourceUsage.SynchronizationState"
    OutputMessageSubProperty_ThreadDisplayName = "ResourceUsage.ThreadDisplayName"
    OutputMessageSubProperty_ThreadId = "ResourceUsage.ThreadId"
    OutputMessageSubProperty_TimeoutPeriod = "ResourceUsage.TimeoutPeriod"
    OutputMessageSubProperty_UseResourceStepDescription = "ResourceUsage.UseResourceStepDescription"


class OutputMessageSeverity(IntEnum):
    Information = 0
    Warning = 1
    Error = 2


class OutputMessage(COMWrapper):
    @property
    @ts_interface
    def message(self) -> str:
        return str(self._com_obj.Message)

    @message.setter
    @ts_interface
    def message(self, value: str) -> None:
        self._com_obj.Message = str(value)

    @property
    @ts_interface
    def timestamp(self) -> typing.Any:
        return self._com_obj.TimeStamp

    @timestamp.setter
    @ts_interface
    def timestamp(self, value: typing.Any) -> None:
        self._com_obj.TimeStamp = value

    @property
    @ts_interface
    def category(self) -> str:
        return str(self._com_obj.Category)

    @category.setter
    @ts_interface
    def category(self, value: str) -> None:
        self._com_obj.Category = str(value)

    @property
    @ts_interface
    def severity(self) -> int:
        return int(self._com_obj.Severity)

    @severity.setter
    @ts_interface
    def severity(self, value: int) -> None:
        self._com_obj.Severity = int(value)

    @property
    @ts_interface
    def icon_name(self) -> str:
        return str(self._com_obj.IconName)

    @icon_name.setter
    @ts_interface
    def icon_name(self, value: str) -> None:
        self._com_obj.IconName = str(value)

    @property
    @ts_interface
    def id(self) -> int:
        return int(self._com_obj.Id)

    @property
    @ts_interface
    def text_color(self) -> int:
        return int(self._com_obj.TextColor)

    @text_color.setter
    @ts_interface
    def text_color(self, value: int) -> None:
        self._com_obj.TextColor = int(value)

    @property
    @ts_interface
    def time_in_seconds(self) -> float:
        return float(self._com_obj.TimeInSeconds)

    @time_in_seconds.setter
    @ts_interface
    def time_in_seconds(self, value: float) -> None:
        self._com_obj.TimeInSeconds = float(value)

    @ts_interface
    def post(self) -> None:
        self._com_obj.Post()

    @property
    @ts_interface
    def execution_locations(self) -> Locations:
        return Locations(self._com_obj.ExecutionLocations, self._engine_ref)

    @property
    @ts_interface
    def file_locations(self) -> Locations:
        return Locations(self._com_obj.FileLocations, self._engine_ref)
