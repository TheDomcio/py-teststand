from __future__ import annotations

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.messaging.output_message import OutputMessage
from py_teststand.property.property_object import PropertyObject


class OutputMessages(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index: int) -> OutputMessage:
        return OutputMessage(self._com_obj.Item(int(index)), self._engine_ref)

    @ts_interface
    def add(self, output_message: OutputMessage) -> None:
        self._com_obj.Add(output_message._com_obj)

    @ts_interface
    def remove(self, index: int) -> None:
        self._com_obj.Remove(int(index))

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def copy_messages_to_collection(self, target: OutputMessages) -> None:
        self._com_obj.CopyMessagesToCollection(target._com_obj)

    @ts_interface
    def transfer_messages_to_collection(self, target: OutputMessages) -> None:
        self._com_obj.TransferMessagesToCollection(target._com_obj)

    @ts_interface
    def find_index(self, output_message_id: int) -> int:
        return int(self._com_obj.FindIndex(int(output_message_id)))

    @ts_interface
    def to_property_object(self, store_execution_locations: bool) -> PropertyObject:
        return PropertyObject(
            self._com_obj.ToPropertyObject(bool(store_execution_locations)), self._engine_ref
        )

    @ts_interface
    def from_property_object(self, val: PropertyObject) -> None:
        self._com_obj.FromPropertyObject(val._com_obj)

    def __len__(self) -> int:
        return self.count

    def __getitem__(self, index: int) -> OutputMessage:
        return self.item(index)

    def __iter__(self):
        for i in range(self.count):
            yield self.item(i)
