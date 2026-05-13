from __future__ import annotations

import typing
from enum import IntEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pythoncom

    from py_teststand.core.engine import Engine
    from py_teststand.property.property_object_file import PropertyObjectFileType
else:
    try:
        import pythoncom
    except ImportError:
        pythoncom = None

from py_teststand.core.com_wrapper import COMWrapper, ts_interface


class FileWritingFormat(IntEnum):
    Ini = 1
    Binary = 2
    Xml = 3


class WriteFileFormat(IntEnum):
    Current = 1
    TestStand4 = 8
    TestStand41 = 9
    TestStand42 = 10
    TestStand45 = 11
    TestStand50 = 12
    TestStand51 = 13
    TestStand_14_0 = 14
    TestStand_16_0 = 15
    TestStand_17 = 16
    TestStand_19 = 17
    TestStand_20 = 18
    TestStand_21 = 19
    TestStand_22 = 20
    TestStand_23 = 21


class FileInformation(COMWrapper):
    def __init__(self, com_obj: typing.Any, engine: Engine | typing.Any | None = None) -> None:
        super().__init__(com_obj, engine)

    @property
    @ts_interface
    def file_exists(self) -> bool:
        return bool(self._com_obj.FileExists)

    @property
    @ts_interface
    def file_writing_format(self) -> int:
        return int(self._com_obj.FileWritingFormat)

    @property
    @ts_interface
    def is_custom_file(self) -> bool:
        return bool(self._com_obj.IsCustomFile)

    @property
    @ts_interface
    def is_cvi_dll(self) -> bool:
        return bool(self._com_obj.IsCVIDll)

    @property
    @ts_interface
    def is_dot_net_assembly(self) -> bool:
        return bool(self._com_obj.IsDotNetAssembly)

    @property
    @ts_interface
    def is_property_object_file(self) -> bool:
        return bool(self._com_obj.IsPropertyObjectFile)

    @property
    @ts_interface
    def is_sequence_file(self) -> bool:
        return bool(self._com_obj.IsSequenceFile)

    @property
    @ts_interface
    def property_object_file_type(self) -> PropertyObjectFileType:
        from py_teststand.property.property_object_file import PropertyObjectFileType

        return PropertyObjectFileType(self._com_obj.PropertyObjectFileType)

    @ts_interface
    def get_file_format_display_version(self) -> str:
        return str(self._com_obj.GetFileFormatDisplayVersion())

    @ts_interface
    def get_file_format_version(self) -> str:
        return str(self._com_obj.GetFileFormatVersion())

    @ts_interface
    def get_file_version(self, val: typing.Any = None) -> typing.Any:
        if val is None:
            if pythoncom is not None:
                val = pythoncom.Missing
            else:
                val = ""
        return self._com_obj.GetFileVersion(val)
