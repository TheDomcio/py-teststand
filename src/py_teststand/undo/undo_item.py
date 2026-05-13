from __future__ import annotations

import typing

from py_teststand.core.com_wrapper import COMWrapper, ts_interface

if typing.TYPE_CHECKING:
    from py_teststand.core.engine import EditKind
    from py_teststand.property.property_object import PropertyObject
    from py_teststand.property.property_object_file import PropertyObjectFile
    from py_teststand.sequence.location import Locations
    from py_teststand.undo.undo_stack import UndoStack


class UndoItem(COMWrapper):
    @property
    @ts_interface
    def edited_file(self) -> PropertyObjectFile:
        from py_teststand.property.property_object_file import PropertyObjectFile

        return PropertyObjectFile(self._com_obj.EditedFile, self._engine_ref)

    @property
    @ts_interface
    def edited_objects(self) -> list[PropertyObject]:
        from py_teststand.property.property_object import PropertyObject

        return [PropertyObject(obj, self._engine_ref) for obj in self._com_obj.EditedObjects]

    @property
    @ts_interface
    def post_edit_change_count(self) -> int:
        return int(self._com_obj.PostEditChangeCount)

    @property
    @ts_interface
    def post_edit_locations(self) -> Locations:
        from py_teststand.sequence.location import Locations

        return Locations(self._com_obj.PostEditLocations, self._engine_ref)

    @property
    @ts_interface
    def pre_edit_change_count(self) -> int:
        return int(self._com_obj.PreEditChangeCount)

    @property
    @ts_interface
    def pre_edit_locations(self) -> Locations:
        from py_teststand.sequence.location import Locations

        return Locations(self._com_obj.PreEditLocations, self._engine_ref)

    @property
    @ts_interface
    def can_redo(self) -> bool:
        return bool(self._com_obj.CanRedo)

    @property
    @ts_interface
    def can_undo(self) -> bool:
        return bool(self._com_obj.CanUndo)

    @property
    @ts_interface
    def redo_description(self) -> str:
        return str(self._com_obj.RedoDescription)

    @property
    @ts_interface
    def redo_edit_kind(self) -> EditKind:
        from py_teststand.core.engine import EditKind

        return EditKind(self._com_obj.RedoEditKind)

    @property
    @ts_interface
    def refresh_enabled(self) -> bool:
        return bool(self._com_obj.RefreshEnabled)

    @property
    @ts_interface
    def undo_description(self) -> str:
        return str(self._com_obj.UndoDescription)

    @property
    @ts_interface
    def undo_edit_kind(self) -> EditKind:
        from py_teststand.core.engine import EditKind

        return EditKind(self._com_obj.UndoEditKind)

    @property
    @ts_interface
    def undo_stack(self) -> UndoStack:
        from py_teststand.undo.undo_stack import UndoStack

        return UndoStack(self._com_obj.UndoStack, self._engine_ref)

    @property
    @ts_interface
    def lookup_strings(self) -> list[str]:
        return list(self._com_obj.LookupStrings)

    @property
    @ts_interface
    def top_objects(self) -> list[PropertyObject]:
        from py_teststand.property.property_object import PropertyObject

        return [PropertyObject(obj, self._engine_ref) for obj in self._com_obj.TopObjects]

    @ts_interface
    def redo(self) -> None:
        return self._com_obj.Redo()

    @ts_interface
    def undo(self) -> None:
        return self._com_obj.Undo()
