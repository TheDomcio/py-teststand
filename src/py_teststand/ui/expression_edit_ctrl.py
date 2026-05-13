from __future__ import annotations

import typing
from enum import IntEnum

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.ui.styles import FontSource, MousePointerStyle

from .connections import Borders, Buttons, ComboBoxItems

if typing.TYPE_CHECKING:
    from py_teststand.core.engine import Engine
    from py_teststand.property.property_object import PropertyObject
    from py_teststand.sequence.expression import EvaluationTypes


class BooleanOrPreference(IntEnum):
    FalseValue = 0
    TrueValue = 1
    UsePreference = 3


class ExpressionEditStyles(IntEnum):
    Edit = 0
    DropDownCombo = 1


class ScrollBars(IntEnum):
    NoneValue = 0
    Both = 1
    Horizontal = 2
    Vertical = 3


class TextType(IntEnum):
    PlainText = 0
    Expression = 1
    ExpressionWithCppIdentifiers = 2


class ErrorCheck(IntEnum):
    NoneValue = 0
    Syntax = 1
    SyntaxAndEvaluation = 2


class ExpressionEdit(COMWrapper):
    @property
    @ts_interface
    def allow_empty(self) -> bool:
        return bool(self._com_obj.AllowEmpty)

    @allow_empty.setter
    @ts_interface
    def allow_empty(self, value: bool) -> None:
        self._com_obj.AllowEmpty = value

    @property
    @ts_interface
    def apply_default_style(self) -> bool:
        return bool(self._com_obj.ApplyDefaultStyle)

    @apply_default_style.setter
    @ts_interface
    def apply_default_style(self, value: bool) -> None:
        self._com_obj.ApplyDefaultStyle = value

    @property
    @ts_interface
    def auto_completion_h_wnd(self) -> int:
        return int(self._com_obj.AutoCompletionHWnd)

    @property
    @ts_interface
    def auto_localize(self) -> bool:
        return bool(self._com_obj.AutoLocalize)

    @auto_localize.setter
    @ts_interface
    def auto_localize(self, value: bool) -> None:
        self._com_obj.AutoLocalize = value

    @property
    @ts_interface
    def automatically_prefix_variables(self) -> bool:
        return bool(self._com_obj.AutomaticallyPrefixVariables)

    @automatically_prefix_variables.setter
    @ts_interface
    def automatically_prefix_variables(self, value: bool) -> None:
        self._com_obj.AutomaticallyPrefixVariables = value

    @property
    @ts_interface
    def back_color(self) -> int:
        return int(self._com_obj.BackColor)

    @back_color.setter
    @ts_interface
    def back_color(self, value: int) -> None:
        self._com_obj.BackColor = value

    @property
    @ts_interface
    def borders(self) -> Borders:
        from .connections import Borders

        return Borders(self._com_obj.Borders, self._engine_ref)

    @property
    @ts_interface
    def browse_expr_dialog_options(self) -> int:
        return int(self._com_obj.BrowseExprDialogOptions)

    @browse_expr_dialog_options.setter
    @ts_interface
    def browse_expr_dialog_options(self, value: int) -> None:
        self._com_obj.BrowseExprDialogOptions = value

    @property
    @ts_interface
    def browse_expr_dialog_title(self) -> str:
        return str(self._com_obj.BrowseExprDialogTitle)

    @browse_expr_dialog_title.setter
    @ts_interface
    def browse_expr_dialog_title(self, value: str) -> None:
        self._com_obj.BrowseExprDialogTitle = value

    @property
    @ts_interface
    def buttons(self) -> Buttons:
        from .connections import Buttons

        return Buttons(self._com_obj.Buttons, self._engine_ref)

    @property
    @ts_interface
    def combo_box_items(self) -> ComboBoxItems:
        from .connections import ComboBoxItems

        return ComboBoxItems(self._com_obj.ComboBoxItems, self._engine_ref)

    @property
    @ts_interface
    def context(self) -> PropertyObject | None:
        from py_teststand.property.property_object import PropertyObject

        com_obj = self._com_obj.Context
        return PropertyObject(com_obj, self._engine_ref) if com_obj else None

    @context.setter
    @ts_interface
    def context(self, value: PropertyObject | None) -> None:
        self._com_obj.Context = getattr(value, "_com_obj", value)

    @property
    @ts_interface
    def display_formatted_value(self) -> bool:
        return bool(self._com_obj.DisplayFormattedValue)

    @display_formatted_value.setter
    @ts_interface
    def display_formatted_value(self, value: bool) -> None:
        self._com_obj.DisplayFormattedValue = value

    @property
    @ts_interface
    def display_text(self) -> str:
        return str(self._com_obj.DisplayText)

    @property
    @ts_interface
    def drop_down_list_h_wnd(self) -> int:
        return int(self._com_obj.DropDownListHWnd)

    @property
    @ts_interface
    def enabled(self) -> bool:
        return bool(self._com_obj.Enabled)

    @enabled.setter
    @ts_interface
    def enabled(self, value: bool) -> None:
        self._com_obj.Enabled = value

    @property
    @ts_interface
    def engine(self) -> Engine:
        from py_teststand.core.engine import Engine

        return Engine(self._com_obj.Engine)

    @property
    @ts_interface
    def error_check(self) -> ErrorCheck:
        return ErrorCheck(self._com_obj.ErrorCheck)

    @error_check.setter
    @ts_interface
    def error_check(self, value: int | ErrorCheck) -> None:
        self._com_obj.ErrorCheck = int(value)

    @property
    @ts_interface
    def font(self) -> typing.Any:
        return self._com_obj.Font

    @font.setter
    @ts_interface
    def font(self, value: typing.Any) -> None:
        self._com_obj.Font = value

    @property
    @ts_interface
    def font_source(self) -> FontSource:
        return FontSource(self._com_obj.FontSource)

    @font_source.setter
    @ts_interface
    def font_source(self, value: int | FontSource) -> None:
        self._com_obj.FontSource = int(value)

    @property
    @ts_interface
    def function_tip_h_wnd(self) -> int:
        return int(self._com_obj.FunctionTipHWnd)

    @property
    @ts_interface
    def hide_selection(self) -> bool:
        return bool(self._com_obj.HideSelection)

    @hide_selection.setter
    @ts_interface
    def hide_selection(self, value: bool) -> None:
        self._com_obj.HideSelection = value

    @property
    @ts_interface
    def h_wnd(self) -> int:
        return int(self._com_obj.hWnd)

    @property
    @ts_interface
    def max_length(self) -> int:
        return int(self._com_obj.MaxLength)

    @max_length.setter
    @ts_interface
    def max_length(self, value: int) -> None:
        self._com_obj.MaxLength = value

    @property
    @ts_interface
    def mouse_icon(self) -> typing.Any:
        return self._com_obj.MouseIcon

    @mouse_icon.setter
    @ts_interface
    def mouse_icon(self, value: typing.Any) -> None:
        self._com_obj.MouseIcon = value

    @property
    @ts_interface
    def mouse_pointer(self) -> MousePointerStyle:
        return MousePointerStyle(self._com_obj.MousePointer)

    @mouse_pointer.setter
    @ts_interface
    def mouse_pointer(self, value: int | MousePointerStyle) -> None:
        self._com_obj.MousePointer = int(value)

    @property
    @ts_interface
    def multi_line(self) -> bool:
        return bool(self._com_obj.MultiLine)

    @multi_line.setter
    @ts_interface
    def multi_line(self, value: bool) -> None:
        self._com_obj.MultiLine = value

    @property
    @ts_interface
    def numeric_format(self) -> str:
        return str(self._com_obj.NumericFormat)

    @numeric_format.setter
    @ts_interface
    def numeric_format(self, value: str) -> None:
        self._com_obj.NumericFormat = value

    @property
    @ts_interface
    def read_only(self) -> bool:
        return bool(self._com_obj.ReadOnly)

    @read_only.setter
    @ts_interface
    def read_only(self, value: bool) -> None:
        self._com_obj.ReadOnly = value

    @property
    @ts_interface
    def scale_with_dpi(self) -> bool:
        return bool(self._com_obj.ScaleWithDPI)

    @scale_with_dpi.setter
    @ts_interface
    def scale_with_dpi(self, value: bool) -> None:
        self._com_obj.ScaleWithDPI = value

    @property
    @ts_interface
    def scroll_bars(self) -> ScrollBars:
        return ScrollBars(self._com_obj.ScrollBars)

    @scroll_bars.setter
    @ts_interface
    def scroll_bars(self, value: int | ScrollBars) -> None:
        self._com_obj.ScrollBars = int(value)

    @property
    @ts_interface
    def sel_length(self) -> int:
        return int(self._com_obj.SelLength)

    @sel_length.setter
    @ts_interface
    def sel_length(self, value: int) -> None:
        self._com_obj.SelLength = value

    @property
    @ts_interface
    def sel_start(self) -> int:
        return int(self._com_obj.SelStart)

    @sel_start.setter
    @ts_interface
    def sel_start(self, value: int) -> None:
        self._com_obj.SelStart = value

    @property
    @ts_interface
    def sel_text(self) -> str:
        return str(self._com_obj.SelText)

    @sel_text.setter
    @ts_interface
    def sel_text(self, value: str) -> None:
        self._com_obj.SelText = value

    @property
    @ts_interface
    def show_display_name_when_inactive(self) -> bool:
        return bool(self._com_obj.ShowDisplayNameWhenInactive)

    @show_display_name_when_inactive.setter
    @ts_interface
    def show_display_name_when_inactive(self, value: bool) -> None:
        self._com_obj.ShowDisplayNameWhenInactive = value

    @property
    @ts_interface
    def style(self) -> ExpressionEditStyles:
        return ExpressionEditStyles(self._com_obj.Style)

    @style.setter
    @ts_interface
    def style(self, value: int | ExpressionEditStyles) -> None:
        self._com_obj.Style = int(value)

    @property
    @ts_interface
    def syntax_highlighting_enabled(self) -> bool:
        return bool(self._com_obj.SyntaxHighlightingEnabled)

    @syntax_highlighting_enabled.setter
    @ts_interface
    def syntax_highlighting_enabled(self, value: bool) -> None:
        self._com_obj.SyntaxHighlightingEnabled = value

    @property
    @ts_interface
    def text(self) -> str:
        return str(self._com_obj.Text)

    @text.setter
    @ts_interface
    def text(self, value: str) -> None:
        self._com_obj.Text = value

    @property
    @ts_interface
    def text_length(self) -> int:
        return int(self._com_obj.TextLength)

    @property
    @ts_interface
    def text_type(self) -> TextType:
        return TextType(self._com_obj.TextType)

    @text_type.setter
    @ts_interface
    def text_type(self, value: int | TextType) -> None:
        self._com_obj.TextType = int(value)

    @property
    @ts_interface
    def want_return(self) -> bool:
        return bool(self._com_obj.WantReturn)

    @want_return.setter
    @ts_interface
    def want_return(self, value: bool) -> None:
        self._com_obj.WantReturn = value

    @property
    @ts_interface
    def word_wrap(self) -> bool:
        return bool(self._com_obj.WordWrap)

    @word_wrap.setter
    @ts_interface
    def word_wrap(self, value: bool) -> None:
        self._com_obj.WordWrap = value

    @ts_interface
    def check_expression2(self) -> tuple[int, str, int, int]:

        return self._com_obj.CheckExpression2("", 0, 0)

    @ts_interface
    def display_browse_expr_dialog(self) -> bool:
        return bool(self._com_obj.DisplayBrowseExprDialog())

    @ts_interface
    def display_error(self, error_code: int, error_description: str) -> None:
        self._com_obj.DisplayError(error_code, error_description)

    @ts_interface
    def evaluate(self, evaluation_options: int = 0) -> PropertyObject:
        from py_teststand.property.property_object import PropertyObject

        return PropertyObject(self._com_obj.Evaluate(evaluation_options), self._engine_ref)

    @ts_interface
    def get_additional_evaluation_constants(self) -> PropertyObject | None:
        from py_teststand.property.property_object import PropertyObject

        com_obj = self._com_obj.GetAdditionalEvaluationConstants()
        return PropertyObject(com_obj, self._engine_ref) if com_obj else None

    @ts_interface
    def get_valid_evaluation_types(self) -> EvaluationTypes:
        from py_teststand.sequence.expression import EvaluationTypes

        return EvaluationTypes(self._com_obj.GetValidEvaluationTypes(), self._engine_ref)

    @ts_interface
    def localize(self) -> None:
        self._com_obj.Localize()

    @ts_interface
    def select_all(self) -> None:
        self._com_obj.SelectAll()

    @ts_interface
    def set_additional_evaluation_constants(self, constants: PropertyObject | None) -> None:
        raw_obj = getattr(constants, "_com_obj", constants)
        self._com_obj.SetAdditionalEvaluationConstants(raw_obj)

    @ts_interface
    def set_valid_evaluation_types(self, types: EvaluationTypes | int) -> None:
        raw_types = getattr(types, "_com_obj", types)
        self._com_obj.SetValidEvaluationTypes(raw_types)
