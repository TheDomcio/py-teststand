from __future__ import annotations

import typing
from unittest.mock import MagicMock

import pytest

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.core.exceptions import Error


class DummyWrapper(COMWrapper):
    @ts_interface
    def failing_method(self):

        self._com_obj.FailingMethod()

    @ts_interface
    def working_method(self) -> typing.Any:

        return self._com().WorkingMethod()

    @property
    @ts_interface
    def some_property(self) -> typing.Any:

        return self._com().SomeProperty


class ComError(Exception):
    def __init__(
        self,
        hresult: int,
        msg: str,
        excinfo: tuple | None = None,
        argerr: int | None = None,
    ) -> None:

        self.hresult = hresult

        self.excepinfo = excinfo

        self.argerr = argerr

        super().__init__(hresult, msg, excinfo, argerr)


def test_ts_interface_exception_mapping() -> None:

    mock_com = MagicMock()

    mock_com.FailingMethod.side_effect = ComError(
        -2147467259,
        "Error",
        (0, "Source", "Description", None, 0, 0),
        0,
    )

    wrapper = DummyWrapper(mock_com)

    with pytest.raises(Error) as exc_info:
        wrapper.failing_method()

    assert "Description" in str(exc_info.value) or "Error" in str(exc_info.value)


def test_com_pointer_release() -> None:

    mock_com = MagicMock()

    wrapper = DummyWrapper(mock_com)

    wrapper.release()

    assert getattr(wrapper, "_com_obj", None) is None


def test_call_after_release_fails() -> None:

    mock_com = MagicMock()

    wrapper = DummyWrapper(mock_com)

    wrapper.release()

    with pytest.raises(Error):
        wrapper.working_method()

    with pytest.raises(Error):
        _ = wrapper.some_property
