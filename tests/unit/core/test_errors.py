from __future__ import annotations

import typing

import pytest

try:
    import pythoncom


except ImportError:
    pythoncom: typing.Any = None


from py_teststand.core.com_wrapper import ts_interface
from py_teststand.core.exceptions import (
    AccessDeniedError,
    COMError,
    FileNotFoundError,
    IndexOutOfRangeError,
)


def test_hresult_mapping_file_not_found():

    @ts_interface
    def fail_file():

        assert pythoncom is not None

        raise pythoncom.com_error(-17208, "File not found", None, None)

    with pytest.raises(FileNotFoundError):
        fail_file()


def test_hresult_mapping_index_out_of_range():

    @ts_interface
    def fail_index():

        assert pythoncom is not None

        raise pythoncom.com_error(-17301, "Index out of range", None, None)

    with pytest.raises(IndexOutOfRangeError):
        fail_index()


def test_hresult_mapping_access_denied():

    @ts_interface
    def fail_access():

        assert pythoncom is not None

        raise pythoncom.com_error(-17205, "Access denied", None, None)

    with pytest.raises(AccessDeniedError):
        fail_access()


def test_fallback_to_generic_error():

    @ts_interface
    def fail_unknown():

        assert pythoncom is not None

        raise pythoncom.com_error(-999999, "Unknown COM error", None, None)

    with pytest.raises(COMError) as excinfo:
        fail_unknown()

    assert "Unknown COM error" in str(excinfo.value)
