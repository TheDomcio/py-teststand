from __future__ import annotations

from enum import IntEnum, IntFlag

from py_teststand.core.com_wrapper import ts_interface
from py_teststand.property.array_dimensions import ArrayDimensions
from py_teststand.property.property_object import PropertyObject, PropValType  # noqa: F401


class PropertyValueTypeFlag(IntFlag):
    Boolean = 1
    Number = 2
    String = 4
    Reference = 8
    Container = 16
    NamedType = 32
    BooleanArray = 64
    NumberArray = 128
    StringArray = 256
    ReferenceArray = 512
    ContainerArray = 1024
    ArrayOfNamedType = 2048
    Nothing = 4096
    Object = 16384
    PlainReference = 32768
    PlainContainer = 65536
    Enum = 131072
    Any = -1


class PropertyRepresentation(IntEnum):
    NoneValue = 0
    Float64 = 1
    Int64 = 2
    UInt64 = 3


class DataType(PropertyObject):
    pass


class PropertyObjectType(PropertyObject):
    @property
    @ts_interface
    def value_type(self) -> int:
        return int(self._com_obj.ValueType)

    @property
    @ts_interface
    def is_object(self) -> bool:
        return bool(self._com_obj.IsObject)

    @property
    @ts_interface
    def class_name(self) -> str:
        return str(self._com_obj.ClassName)

    @property
    @ts_interface
    def type_name(self) -> str:
        return str(self._com_obj.TypeName)

    @property
    @ts_interface
    def display_string(self) -> str:
        return str(self._com_obj.DisplayString)

    @property
    @ts_interface
    def element_type(self) -> PropertyObjectType | None:
        com = self._com_obj.ElementType
        if com is None:
            return None
        return PropertyObjectType(com, self._engine_ref)

    @property
    @ts_interface
    def array_dimensions(self) -> ArrayDimensions | None:
        com = self._com_obj.ArrayDimensions
        if com is None:
            return None
        return ArrayDimensions(com, self._engine_ref)

    @property
    @ts_interface
    def representation(self) -> int:
        return int(self._com_obj.Representation)

    @representation.setter
    @ts_interface
    def representation(self, value: int) -> None:
        self._com_obj.Representation = int(value)

    @ts_interface
    def is_equal_to(self, object_to_compare: PropertyObjectType, options: int = 0) -> bool:
        return bool(self._com_obj.IsEqualTo(object_to_compare._com_obj, int(options)))
