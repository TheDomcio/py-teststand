from __future__ import annotations

import functools
import typing
from typing import Callable

StepLogic = Callable[..., typing.Any]


def py_teststand_step(name: str | None = None) -> Callable[[StepLogic], StepLogic]:

    def decorator(func: StepLogic) -> StepLogic:
        @functools.wraps(func)
        def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            return func(*args, **kwargs)

        typing.cast(typing.Any, wrapper).__teststand_step__ = True
        if name is not None:
            typing.cast(typing.Any, wrapper).__teststand_step_name__ = name
        return wrapper

    return decorator


class StepTypeBuilder:
    def __init__(self, engine: typing.Any):
        self.engine = engine

    def create_python_step_type(
        self, palette_file: typing.Any, type_name: str, module_path: str, function_name: str
    ) -> None:
        raise NotImplementedError
