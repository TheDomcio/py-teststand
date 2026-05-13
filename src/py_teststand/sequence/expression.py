from __future__ import annotations

import typing
from enum import IntEnum, IntFlag
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COMWrapper, ts_interface


class PropertyValueTypeFlag(IntFlag):
    Any = -1
    Boolean = 0x1
    Number = 0x2
    String = 0x4
    Reference = 0x8
    Container = 0x10
    NamedType = 0x20
    BooleanArray = 0x40
    NumberArray = 0x80
    StringArray = 0x100
    ReferenceArray = 0x200
    ContainerArray = 0x400
    ArrayOfNamedType = 2048
    Enum = 131072
    Nothing = 4096
    Object = 16384
    PlainContainer = 65536
    PlainReference = 32768


class ValidateExpressionOption(IntFlag):
    NoneValue = 0x0
    Path = 0x1
    MustEvaluateToProperty = 0x2


class SpecifyExpressionEditButton(IntEnum):
    ByIndex = 0
    ByKind = 1


class TokenCode(IntEnum):
    Assignment = 27
    Bad = 4
    BinaryInteger = 48
    BitwiseAnd = 21
    BitwiseAndAssignment = 32
    BitwiseNot = 24


class TokenizeOption(IntFlag):
    NoneValue = 0x0
    PreserveComments = 0x1
    RecognizeCPPIdentifiers = 0x4


class WatchExpressionBreakType(IntEnum):
    NoneValue = 0x0
    OnChange = 0x1
    OnExpressionTrue = 0x2


class PropertyRepresentation(IntEnum):
    Float64 = 1
    Int64 = 2
    NoneValue = 0
    UInt64 = 3


if TYPE_CHECKING:
    from py_teststand.core.engine import Engine


class EvaluationType(COMWrapper):
    def __init__(self, com_obj: typing.Any, engine: Engine | typing.Any | None = None) -> None:

        super().__init__(com_obj, engine)

    @property
    @ts_interface
    def property_value_type_flags(self) -> int:
        return int(self._com_obj.PropertyValueTypeFlags)

    @property_value_type_flags.setter
    @ts_interface
    def property_value_type_flags(self, value: int) -> None:
        self._com_obj.PropertyValueTypeFlags = int(value)

    @property
    @ts_interface
    def named_types(self) -> list[str]:
        return list(self._com_obj.NamedTypes)

    @named_types.setter
    @ts_interface
    def named_types(self, value: list[str]) -> None:
        self._com_obj.NamedTypes = value

    @property
    @ts_interface
    def array_of_named_types(self) -> list[str]:
        return list(self._com_obj.ArrayOfNamedTypes)

    @array_of_named_types.setter
    @ts_interface
    def array_of_named_types(self, value: list[str]) -> None:
        self._com_obj.ArrayOfNamedTypes = value

    @property
    @ts_interface
    def allowed_array_representations(self) -> typing.Any:
        return int(self._com_obj.AllowedArrayRepresentations)

    @allowed_array_representations.setter
    @ts_interface
    def allowed_array_representations(self, value: int) -> None:
        self._com_obj.AllowedArrayRepresentations = int(value)

    @property
    @ts_interface
    def allowed_representations(self) -> typing.Any:
        return int(self._com_obj.AllowedRepresentations)

    @allowed_representations.setter
    @ts_interface
    def allowed_representations(self, value: int) -> None:
        self._com_obj.AllowedRepresentations = int(value)


class Expression(COMWrapper):
    def __init__(self, com_obj: typing.Any, engine: Engine | typing.Any | None = None) -> None:

        super().__init__(com_obj, engine)

    @property
    @ts_interface
    def text(self) -> typing.Any:
        return str(self._com_obj.Text)

    @text.setter
    @ts_interface
    def text(self, value: str) -> None:
        self._com_obj.Text = str(value)

    @property
    @ts_interface
    def num_tokens(self) -> int:
        return int(self._com_obj.NumTokens)

    @ts_interface
    def evaluate(self, evaluation_context: typing.Any = None, options: int = 0) -> typing.Any:
        com_ctx = (
            getattr(evaluation_context, "_com_obj", evaluation_context)
            if evaluation_context
            else None
        )
        com_res = self._com_obj.Evaluate(com_ctx, int(options))
        if com_res:
            from py_teststand.property.property_object import PropertyObject

            return PropertyObject(com_res, self._engine_ref)
        return None

    @ts_interface
    def get_constant_value(self) -> typing.Any:
        com_res = self._com_obj.GetConstantValue()
        if com_res:
            from py_teststand.property.property_object import PropertyObject

            return PropertyObject(com_res, self._engine_ref)
        return None

    @ts_interface
    def get_token(self, token_index: int) -> tuple[TokenCode, int, int, str]:
        res = self._com_obj.GetToken(int(token_index))
        if isinstance(res, tuple) and len(res) >= 4:
            return TokenCode(res[0]), int(res[1]), int(res[2]), str(res[3])
        return TokenCode.Bad, 0, 0, ""

    @ts_interface
    def tokenize(self, options: int = 0, initial_parse_state: int = 0) -> None:
        self._com_obj.Tokenize(int(options), int(initial_parse_state))

    @ts_interface
    def validate(
        self,
        evaluation_context: typing.Any = None,
        check_syntax_only: bool = True,
        evaluation_options: int = 0,
    ) -> tuple[bool, str, int, int]:
        com_ctx = (
            getattr(evaluation_context, "_com_obj", evaluation_context)
            if evaluation_context
            else None
        )
        res = self._com_obj.Validate(
            com_ctx,
            bool(check_syntax_only),
            int(evaluation_options),
        )
        if isinstance(res, tuple) and len(res) >= 4:
            return bool(res[0]), str(res[1]), int(res[2]), int(res[3])
        return bool(res), "", 0, 0

    @ts_interface
    def validate_evaluation_type(
        self,
        valid_evaluation_types: EvaluationType,
        additional_constants: typing.Any = None,
        evaluation_context: typing.Any = None,
        evaluation_options: int = 0,
    ) -> tuple[int, str, int, int]:
        com_types = getattr(valid_evaluation_types, "_com_obj", valid_evaluation_types)
        com_ctx = (
            getattr(evaluation_context, "_com_obj", evaluation_context)
            if evaluation_context
            else None
        )
        res = self._com_obj.ValidateEvaluationType(
            com_types,
            additional_constants,
            com_ctx,
            int(evaluation_options),
        )
        if isinstance(res, tuple) and len(res) >= 4:
            return int(res[0]), str(res[1]), int(res[2]), int(res[3])
        return int(res), "", 0, 0


EvaluationTypes = EvaluationType
