from __future__ import annotations

import typing

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.undo.undo_item import UndoItem


class UndoStack(COMWrapper):
    @property
    @ts_interface
    def undo_items(self) -> UndoItems:
        return UndoItems(self._com_obj.UndoItems, self._engine_ref)

    @property
    @ts_interface
    def redo_items(self) -> UndoItems:
        return UndoItems(self._com_obj.RedoItems, self._engine_ref)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def undo(self) -> None:
        self._com_obj.Undo()

    @ts_interface
    def redo(self) -> None:
        self._com_obj.Redo()

    @property
    @ts_interface
    def can_undo(self) -> bool:
        return bool(self._com_obj.CanUndo)

    @property
    @ts_interface
    def can_redo(self) -> bool:
        return bool(self._com_obj.CanRedo)

    @property
    @ts_interface
    def in_redo(self) -> bool:
        return bool(self._com_obj.InRedo)

    @property
    @ts_interface
    def in_undo(self) -> bool:
        return bool(self._com_obj.InUndo)

    @ts_interface
    def aggregate_top_undo_items(
        self,
        num_items_to_aggregate: int,
        description: str = "",
        pre_edit_locations: typing.Any = None,
        post_edit_locations: typing.Any = None,
    ) -> None:
        com_pre = getattr(pre_edit_locations, "_com_obj", pre_edit_locations)
        com_post = getattr(post_edit_locations, "_com_obj", post_edit_locations)
        self._com_obj.AggregateTopUndoItems(
            int(num_items_to_aggregate), str(description), com_pre, com_post
        )

    @ts_interface
    def get_redo_description(self, accelerator_prefix: str = "") -> typing.Any:
        return str(self._com_obj.GetRedoDescription(str(accelerator_prefix)))

    @ts_interface
    def get_undo_description(self, accelerator_prefix: str = "") -> typing.Any:
        return str(self._com_obj.GetUndoDescription(str(accelerator_prefix)))

    @ts_interface
    def push(self, item: typing.Any) -> typing.Any:
        com_item = getattr(item, "_com_obj", item)
        self._com_obj.Push(com_item)


class UndoItems(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index: int) -> UndoItem:
        return UndoItem(self._com_obj.Item(index), self._engine_ref)

    @ts_interface
    def remove(self, index: int) -> typing.Any:
        self._com_obj.Remove(index)

    @property
    @ts_interface
    def top_item(self) -> UndoItem:
        return UndoItem(self._com_obj.TopItem, self._engine_ref)

    def __len__(self) -> int:

        return self.count

    def __getitem__(self, index: int) -> UndoItem:

        return self.item(index)
