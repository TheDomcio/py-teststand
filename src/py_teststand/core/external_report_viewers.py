from __future__ import annotations

import typing
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COMWrapper, ts_interface

if TYPE_CHECKING:
    from py_teststand.core.engine import Engine


class ExternalReportViewer(COMWrapper):
    @property
    @ts_interface
    def arguments(self) -> str:
        return str(self._com_obj.Arguments)

    @arguments.setter
    @ts_interface
    def arguments(self, value: str) -> None:
        self._com_obj.Arguments = str(value)

    @property
    @ts_interface
    def auto_launch(self) -> bool:
        return bool(self._com_obj.AutoLaunch)

    @auto_launch.setter
    @ts_interface
    def auto_launch(self, value: bool) -> None:
        self._com_obj.AutoLaunch = bool(value)

    @property
    @ts_interface
    def format(self) -> str:
        return str(self._com_obj.Format)

    @format.setter
    @ts_interface
    def format(self, value: str) -> None:
        self._com_obj.Format = str(value)

    @property
    @ts_interface
    def path(self) -> str:
        return str(self._com_obj.Path)

    @path.setter
    @ts_interface
    def path(self, value: str) -> None:
        self._com_obj.Path = str(value)


class ExternalReportViewers(COMWrapper):
    def __init__(self, com_obj: typing.Any, engine: Engine | typing.Any | None = None) -> None:
        super().__init__(com_obj, engine)

    @property
    @ts_interface
    def auto_launch_default_external_viewers(self) -> bool:
        return bool(self._com_obj.AutoLaunchDefaultExternalViewers)

    @auto_launch_default_external_viewers.setter
    @ts_interface
    def auto_launch_default_external_viewers(self, value: bool) -> None:
        self._com_obj.AutoLaunchDefaultExternalViewers = bool(value)

    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index: int | str) -> ExternalReportViewer:
        return ExternalReportViewer(self._com_obj.Item(index), self._engine_ref)

    @ts_interface
    def add(
        self,
        format: str,
        path: str,
        arguments: str,
        auto_launch: bool,
    ) -> None:
        self._com_obj.Add(str(format), str(path), str(arguments), bool(auto_launch))

    @ts_interface
    def remove(self, index: int) -> None:
        self._com_obj.Remove(int(index))

    def __iter__(self) -> typing.Iterator[ExternalReportViewer]:
        for i in range(self.count):
            yield self.item(i)

    def __len__(self) -> int:
        return self.count

    def __getitem__(self, index: int | str) -> ExternalReportViewer:
        return self.item(index)
