from __future__ import annotations

import typing
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COMWrapper, ts_interface

if TYPE_CHECKING:
    from py_teststand.core.engine import ApplicationSite, CreateUndoItemOption
    from py_teststand.undo.undo_item import UndoItem


class UndoItemCreator(COMWrapper):
    @property
    @ts_interface
    def have_edits_been_made(self) -> bool:
        return bool(self._com_obj.HaveEditsBeenMade)

    @ts_interface
    def begin_batch_edit(self, objects: list[typing.Any]) -> None:
        com_objects = [getattr(obj, "_com_obj", obj) for obj in objects]
        self._com_obj.BeginBatchEdit(com_objects)

    @ts_interface
    def begin_edit(self, object_to_edit: typing.Any) -> None:
        com_obj = getattr(object_to_edit, "_com_obj", object_to_edit)
        self._com_obj.BeginEdit(com_obj)

    @ts_interface
    def begin_edit_ex(self, object_to_edit: typing.Any, lookup_string: str) -> None:
        com_obj = getattr(object_to_edit, "_com_obj", object_to_edit)
        self._com_obj.BeginEditEx(com_obj, str(lookup_string))

    @ts_interface
    def create_and_post_undo_item(
        self,
        options: CreateUndoItemOption | int = 0,
        locations_application_site: ApplicationSite | int = 0,
        locations_user_data: typing.Any = None,
    ) -> UndoItem | None:
        from py_teststand.undo.undo_item import UndoItem

        user_data = getattr(locations_user_data, "_com_obj", locations_user_data)
        com_obj = self._com_obj.CreateAndPostUndoItem(
            int(options),
            int(locations_application_site),
            user_data,
        )
        if com_obj is None:
            return None
        return UndoItem(com_obj, self._engine_ref)

    @ts_interface
    def end_batch_edit(self) -> None:
        self._com_obj.EndBatchEdit()

    @ts_interface
    def end_edit(self) -> None:
        self._com_obj.EndEdit()
