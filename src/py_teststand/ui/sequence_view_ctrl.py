from __future__ import annotations

import typing
from enum import IntEnum, IntFlag

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.ui.styles import FontSource, MousePointerStyle

if typing.TYPE_CHECKING:
    from .connections import Borders, SeqViewColumns


class BlockDisplayOption(IntFlag):
    NoneValue = 0x0
    Indent = 0x1
    ShowLines = 0x2
    DottedLines = 0x4
    ShowStepIcons = 0x8
    BoldStepFont = 0x10
    HighlightMismatchErrors = 0x20
    ShowGroupLines = 0x40


class CheckedState(IntEnum):
    Unchecked = 1
    Checked = 2
    Indeterminate = 3


class SequenceViewCtrl(COMWrapper):
    @property
    @ts_interface
    def auto_size_columns(self) -> bool:
        return bool(self._com_obj.AutoSizeColumns)

    @auto_size_columns.setter
    @ts_interface
    def auto_size_columns(self, value: bool) -> None:
        self._com_obj.AutoSizeColumns = value

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
    def block_display_options(self) -> BlockDisplayOption:
        return BlockDisplayOption(self._com_obj.BlockDisplayOptions)

    @block_display_options.setter
    @ts_interface
    def block_display_options(self, value: int | BlockDisplayOption) -> None:
        self._com_obj.BlockDisplayOptions = int(value)

    @property
    @ts_interface
    def borders(self) -> Borders:
        from .connections import Borders

        return Borders(self._com_obj.Borders, self._engine_ref)

    @property
    @ts_interface
    def can_edit_label(self) -> bool:
        return bool(self._com_obj.CanEditLabel)

    @can_edit_label.setter
    @ts_interface
    def can_edit_label(self, value: bool) -> None:
        self._com_obj.CanEditLabel = value

    @property
    @ts_interface
    def columns(self) -> SeqViewColumns:
        from .connections import SeqViewColumns

        return SeqViewColumns(self._com_obj.Columns, self._engine_ref)

    @property
    @ts_interface
    def comments_color(self) -> int:
        return int(self._com_obj.CommentsColor)

    @comments_color.setter
    @ts_interface
    def comments_color(self, value: int) -> None:
        self._com_obj.CommentsColor = value

    @property
    @ts_interface
    def comments_font(self) -> typing.Any:
        return self._com_obj.CommentsFont

    @comments_font.setter
    @ts_interface
    def comments_font(self, value: typing.Any) -> None:
        self._com_obj.CommentsFont = value

    @property
    @ts_interface
    def comments_font_source(self) -> FontSource:
        return FontSource(self._com_obj.CommentsFontSource)

    @comments_font_source.setter
    @ts_interface
    def comments_font_source(self, value: int | FontSource) -> None:
        self._com_obj.CommentsFontSource = int(value)

    @property
    @ts_interface
    def comments_offset(self) -> int:
        return int(self._com_obj.CommentsOffset)

    @comments_offset.setter
    @ts_interface
    def comments_offset(self, value: int) -> None:
        self._com_obj.CommentsOffset = value

    @property
    @ts_interface
    def cursor(self) -> int:
        return int(self._com_obj.Cursor)

    @cursor.setter
    @ts_interface
    def cursor(self, value: int) -> None:
        self._com_obj.Cursor = value

    @property
    @ts_interface
    def editing_flags(self) -> int:
        return int(self._com_obj.EditingFlags)

    @editing_flags.setter
    @ts_interface
    def editing_flags(self, value: int) -> None:
        self._com_obj.EditingFlags = value

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
    def focus_index(self) -> int:
        return int(self._com_obj.FocusIndex)

    @focus_index.setter
    @ts_interface
    def focus_index(self, value: int) -> None:
        self._com_obj.FocusIndex = value

    @property
    @ts_interface
    def header_font(self) -> typing.Any:
        return self._com_obj.HeaderFont

    @header_font.setter
    @ts_interface
    def header_font(self, value: typing.Any) -> None:
        self._com_obj.HeaderFont = value

    @property
    @ts_interface
    def header_font_source(self) -> FontSource:
        return FontSource(self._com_obj.HeaderFontSource)

    @header_font_source.setter
    @ts_interface
    def header_font_source(self, value: int | FontSource) -> None:
        self._com_obj.HeaderFontSource = int(value)

    @property
    @ts_interface
    def horiz_lines(self) -> bool:
        return bool(self._com_obj.HorizLines)

    @horiz_lines.setter
    @ts_interface
    def horiz_lines(self, value: bool) -> None:
        self._com_obj.HorizLines = value

    @property
    @ts_interface
    def h_wnd(self) -> int:
        return int(self._com_obj.hWnd)

    @property
    @ts_interface
    def icon_size(self) -> int:
        return int(self._com_obj.IconSize)

    @icon_size.setter
    @ts_interface
    def icon_size(self, value: int) -> None:
        self._com_obj.IconSize = value

    @property
    @ts_interface
    def item_back_color_expression(self) -> str:
        return str(self._com_obj.ItemBackColorExpression)

    @item_back_color_expression.setter
    @ts_interface
    def item_back_color_expression(self, value: str) -> None:
        self._com_obj.ItemBackColorExpression = value

    @property
    @ts_interface
    def item_text_color_expression(self) -> str:
        return str(self._com_obj.ItemTextColorExpression)

    @item_text_color_expression.setter
    @ts_interface
    def item_text_color_expression(self, value: str) -> None:
        self._com_obj.ItemTextColorExpression = value

    @property
    @ts_interface
    def lines_color(self) -> int:
        return int(self._com_obj.LinesColor)

    @lines_color.setter
    @ts_interface
    def lines_color(self, value: int) -> None:
        self._com_obj.LinesColor = value

    @property
    @ts_interface
    def max_comments_height(self) -> int:
        return int(self._com_obj.MaxCommentsHeight)

    @max_comments_height.setter
    @ts_interface
    def max_comments_height(self, value: int) -> None:
        self._com_obj.MaxCommentsHeight = value

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
    def read_only(self) -> bool:
        return bool(self._com_obj.ReadOnly)

    @read_only.setter
    @ts_interface
    def read_only(self, value: bool) -> None:
        self._com_obj.ReadOnly = value

    @property
    @ts_interface
    def round_item_rects(self) -> bool:
        return bool(self._com_obj.RoundItemRects)

    @round_item_rects.setter
    @ts_interface
    def round_item_rects(self, value: bool) -> None:
        self._com_obj.RoundItemRects = value

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
    def shade_alternate_columns(self) -> bool:
        return bool(self._com_obj.ShadeAlternateColumns)

    @shade_alternate_columns.setter
    @ts_interface
    def shade_alternate_columns(self, value: bool) -> None:
        self._com_obj.ShadeAlternateColumns = value

    @property
    @ts_interface
    def show_comments(self) -> bool:
        return bool(self._com_obj.ShowComments)

    @show_comments.setter
    @ts_interface
    def show_comments(self, value: bool) -> None:
        self._com_obj.ShowComments = value

    @property
    @ts_interface
    def show_comments_bars(self) -> bool:
        return bool(self._com_obj.ShowCommentsBars)

    @show_comments_bars.setter
    @ts_interface
    def show_comments_bars(self, value: bool) -> None:
        self._com_obj.ShowCommentsBars = value

    @property
    @ts_interface
    def show_headers(self) -> bool:
        return bool(self._com_obj.ShowHeaders)

    @show_headers.setter
    @ts_interface
    def show_headers(self, value: bool) -> None:
        self._com_obj.ShowHeaders = value

    @property
    @ts_interface
    def show_item_tip_strips(self) -> bool:
        return bool(self._com_obj.ShowItemTipStrips)

    @show_item_tip_strips.setter
    @ts_interface
    def show_item_tip_strips(self, value: bool) -> None:
        self._com_obj.ShowItemTipStrips = value

    @property
    @ts_interface
    def step_icons_enabled(self) -> bool:
        return bool(self._com_obj.StepIconsEnabled)

    @step_icons_enabled.setter
    @ts_interface
    def step_icons_enabled(self, value: bool) -> None:
        self._com_obj.StepIconsEnabled = value

    @property
    @ts_interface
    def text_color(self) -> int:
        return int(self._com_obj.TextColor)

    @text_color.setter
    @ts_interface
    def text_color(self, value: int) -> None:
        self._com_obj.TextColor = value

    @property
    @ts_interface
    def text_font(self) -> typing.Any:
        return self._com_obj.TextFont

    @text_font.setter
    @ts_interface
    def text_font(self, value: typing.Any) -> None:
        self._com_obj.TextFont = value

    @property
    @ts_interface
    def text_font_source(self) -> FontSource:
        return FontSource(self._com_obj.TextFontSource)

    @text_font_source.setter
    @ts_interface
    def text_font_source(self, value: int | FontSource) -> None:
        self._com_obj.TextFontSource = int(value)

    @property
    @ts_interface
    def tooltip_visible(self) -> bool:
        return bool(self._com_obj.ToolTipVisible)

    @tooltip_visible.setter
    @ts_interface
    def tooltip_visible(self, value: bool) -> None:
        self._com_obj.ToolTipVisible = value

    @property
    @ts_interface
    def vert_lines(self) -> bool:
        return bool(self._com_obj.VertLines)

    @vert_lines.setter
    @ts_interface
    def vert_lines(self, value: bool) -> None:
        self._com_obj.VertLines = value

    @ts_interface
    def begin_update(self) -> None:
        self._com_obj.BeginUpdate()

    @ts_interface
    def edit_label(self) -> None:
        self._com_obj.EditLabel()

    @ts_interface
    def end_update(self) -> None:
        self._com_obj.EndUpdate()

    @ts_interface
    def hit_test(self, x: int, y: int) -> tuple[int, int, int]:
        return self._com_obj.HitTest(x, y, 0, 0, 0)

    @ts_interface
    def item_index_to_step(self, item_index: int) -> tuple[bool, int, int]:
        return self._com_obj.ItemIndexToStep(item_index, 0, 0)

    @ts_interface
    def localize(self) -> None:
        self._com_obj.Localize()

    @ts_interface
    def step_to_item_index(self, group: int, step_index: int) -> int:
        return int(self._com_obj.StepToItemIndex(group, step_index))
