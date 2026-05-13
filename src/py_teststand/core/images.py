from __future__ import annotations

import typing
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COMWrapper, ts_interface

if TYPE_CHECKING:
    from py_teststand.core.engine import Engine


class Images(COMWrapper):
    def __init__(self, com_obj: typing.Any, engine: Engine) -> None:
        super().__init__(com_obj, engine)

    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, image_index: int) -> typing.Any:
        return self._com_obj.Item(int(image_index))

    def __len__(self) -> int:
        return self.count

    def __getitem__(self, image_index: int) -> typing.Any:
        return self.item(image_index)

    @ts_interface
    def find_image(self, icon_name: str, desired_width: int, desired_height: int) -> typing.Any:
        return self._com_obj.FindImage(str(icon_name), int(desired_width), int(desired_height))
