from __future__ import annotations

import functools
import logging
import typing
import warnings
import weakref
from typing import TYPE_CHECKING, Callable, TypeVar, cast

if TYPE_CHECKING:
    from typing import Protocol

    from typing_extensions import Self

    from py_teststand.core.engine import Engine

    class COMObject(Protocol):
        def __getattr__(self, name: str) -> typing.Any: ...
        def __setattr__(self, name: str, value: typing.Any) -> None: ...

    class COMErrorType(Protocol):
        hresult: int
        excepinfo: typing.Any
        argerror: typing.Any

    COM = typing.Any
else:
    COM = object

logger = logging.getLogger("py_teststand.com_trace")


T = TypeVar("T", bound=Callable[..., typing.Any])


def raw_engine_from_wrapper(engine: Engine | typing.Any) -> typing.Any:

    store = getattr(engine, "__dict__", None)
    if store is not None:
        inner = store.get("_engine")
        if inner is not None:
            return inner
    return engine


def ts_interface(func: T) -> T:

    @functools.wraps(func)
    def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:

        instance = args[0] if args else None
        handling = getattr(instance, "_handling_error", False) if instance is not None else False
        if handling:
            return func(*args, **kwargs)

        try:
            return func(*args, **kwargs)
        except Exception as e:
            from py_teststand.core.exceptions import (
                ERROR_MAP,
                TestStandCOMError,
                TestStandError,
            )

            hresult = getattr(e, "hresult", None)
            if hresult is None:
                if type(e).__name__ == "com_error" and e.args:
                    first = e.args[0]
                    if isinstance(first, int):
                        hresult = first
                    elif isinstance(first, tuple) and len(first) > 0:
                        hresult = first[0]

            if hresult is None:
                raise

            if instance is not None:
                instance._handling_error = True
            try:
                msg = str(e)
                source = None
                description = None

                if len(e.args) > 1:
                    second = e.args[1]
                    if isinstance(second, str):
                        description = second
                        msg = description

                if len(e.args) > 2 and isinstance(e.args[2], tuple):
                    extra = e.args[2]
                    if len(extra) >= 2:
                        source = str(extra[1]) if extra[1] else source
                        if len(extra) >= 3 and extra[2]:
                            description = str(extra[2])

                engine = getattr(instance, "engine", None) if instance is not None else None
                if engine is not None:
                    try:
                        raw_eng = raw_engine_from_wrapper(engine)
                        eng_msg = raw_eng.GetErrorString(hresult)
                        if eng_msg:
                            msg = str(eng_msg)
                    except Exception:
                        pass

                exc_cls = ERROR_MAP.get(hresult, TestStandCOMError)
                if not issubclass(exc_cls, TestStandError):
                    exc_cls = TestStandCOMError
                raise exc_cls(msg, hresult, source=source, description=description) from e
            finally:
                if instance is not None:
                    instance._handling_error = False

    return cast(T, wrapper)


class COMWrapper:
    _com_obj: COM

    def __init__(self, com_obj: COM, engine: Engine | typing.Any | None = None) -> None:

        if com_obj is None:
            raise ValueError("COM object cannot be None")
        if engine is None:
            self._engine_ref = lambda: None
        elif isinstance(engine, weakref.ReferenceType):
            self._engine_ref = engine
        else:
            try:
                self._engine_ref = weakref.ref(engine)
            except TypeError:
                referent = engine
                self._engine_ref = lambda: referent
        self._com_obj = com_obj

    @property
    def engine(self) -> Engine | None:

        if self._engine_ref is None:
            return None
        return cast("Engine | None", self._engine_ref())

    def _com(self) -> COM:
        from py_teststand.core.exceptions import TestStandError

        if not hasattr(self, "_com_obj") or self._com_obj is None:
            raise TestStandError("Cannot access COM object on a released wrapper.")
        return self._com_obj

    def get_com_obj(self) -> typing.Any:
        warnings.warn(
            "get_com_obj() is deprecated and will be removed in a future release. "
            "Access internal state via wrapper methods only.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._com()

    def __getattr__(self, name: str) -> typing.Any:

        if name.startswith("_") or name.startswith("__"):
            raise AttributeError(name)
        return getattr(self._com(), name)

    def __setattr__(self, name: str, value: typing.Any) -> None:

        if name.startswith("_"):
            super().__setattr__(name, value)
            return

        cls_attr = getattr(type(self), name, None)
        if isinstance(cls_attr, property) and cls_attr.fset is not None:
            super().__setattr__(name, value)
            return

        if hasattr(self, "_com_obj") and self._com_obj is not None:
            setattr(self._com_obj, name, value)
        else:
            super().__setattr__(name, value)

    def __repr__(self) -> str:

        status = "Active" if hasattr(self, "_com_obj") and self._com_obj is not None else "Released"
        return f"<{self.__class__.__name__} [{status}] at {id(self):#x}>"

    def __enter__(self) -> Self:

        return self

    def __exit__(self, exc_type: typing.Any, exc_val: typing.Any, exc_tb: typing.Any) -> None:

        self.release()

    def release(self) -> None:

        try:
            if hasattr(self, "_com_obj") and self._com_obj is not None:
                object.__setattr__(self, "_com_obj", None)
        except Exception:
            pass

    def __del__(self) -> None:
        try:
            self.release()
        except Exception:
            pass

    @ts_interface
    def as_property_object(self) -> typing.Any:
        from py_teststand.property.property_object import PropertyObject

        return PropertyObject(self._com_obj.AsPropertyObject(), self._engine_ref)
