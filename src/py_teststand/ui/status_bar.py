from __future__ import annotations

import typing

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.ui.styles import AlignmentStyle, FontSource, StatusBarPaneStyle


class StatusBarPane(COMWrapper):
    @property
    @ts_interface
    def caption(self) -> str:
        return str(self._com_obj.Caption)

    @caption.setter
    @ts_interface
    def caption(self, value: str) -> None:
        self._com_obj.Caption = value

    @property
    @ts_interface
    def icon_name(self) -> str:
        return str(self._com_obj.IconName)

    @icon_name.setter
    @ts_interface
    def icon_name(self, value: str) -> None:
        self._com_obj.IconName = value

    @property
    @ts_interface
    def index(self) -> int:
        return int(self._com_obj.Index)

    @property
    @ts_interface
    def name(self) -> str:
        return str(self._com_obj.Name)

    @name.setter
    @ts_interface
    def name(self, value: str) -> None:
        self._com_obj.Name = value

    @property
    @ts_interface
    def process_percent(self) -> float:
        return float(self._com_obj.ProcessPercent)

    @process_percent.setter
    @ts_interface
    def process_percent(self, value: float) -> None:
        self._com_obj.ProcessPercent = value

    @property
    @ts_interface
    def style(self) -> StatusBarPaneStyle:
        return StatusBarPaneStyle(self._com_obj.Style)

    @style.setter
    @ts_interface
    def style(self, value: int | StatusBarPaneStyle) -> None:
        self._com_obj.Style = int(value)

    @property
    @ts_interface
    def text_alignment(self) -> AlignmentStyle:
        return AlignmentStyle(self._com_obj.TextAlignment)

    @text_alignment.setter
    @ts_interface
    def text_alignment(self, value: int | AlignmentStyle) -> None:
        self._com_obj.TextAlignment = int(value)

    @property
    @ts_interface
    def tooltip_text(self) -> str:
        return str(self._com_obj.ToolTipText)

    @tooltip_text.setter
    @ts_interface
    def tooltip_text(self, value: str) -> None:
        self._com_obj.ToolTipText = value

    @property
    @ts_interface
    def use_available_space(self) -> bool:
        return bool(self._com_obj.UseAvailableSpace)

    @use_available_space.setter
    @ts_interface
    def use_available_space(self, value: bool) -> None:
        self._com_obj.UseAvailableSpace = value

    @property
    @ts_interface
    def visible(self) -> bool:
        return bool(self._com_obj.Visible)

    @visible.setter
    @ts_interface
    def visible(self, value: bool) -> None:
        self._com_obj.Visible = value

    @property
    @ts_interface
    def width(self) -> int:
        return int(self._com_obj.Width)

    @width.setter
    @ts_interface
    def width(self, value: int) -> None:
        self._com_obj.Width = value


class StatusBarPanes(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index_or_name: typing.Any) -> StatusBarPane:
        return StatusBarPane(self._com_obj.Item(index_or_name), self._engine_ref)

    def __len__(self) -> int:
        return self.count

    def __getitem__(self, key: typing.Any) -> StatusBarPane:
        return self.item(key)

    def __iter__(self) -> typing.Iterator[StatusBarPane]:
        for i in range(self.count):
            yield self.item(i)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def insert(self, pane_name: str, insert_before: int = -1) -> StatusBarPane:
        return StatusBarPane(self._com_obj.Insert(pane_name, insert_before), self._engine_ref)

    @ts_interface
    def remove(self, index: int) -> None:
        self._com_obj.Remove(index)


class StatusBar(COMWrapper):
    @property
    @ts_interface
    def auto_size(self) -> bool:
        return bool(self._com_obj.AutoSize)

    @auto_size.setter
    @ts_interface
    def auto_size(self, value: bool) -> None:
        self._com_obj.AutoSize = value

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
    def panes(self) -> StatusBarPanes:
        return StatusBarPanes(self._com_obj.Panes, self._engine_ref)

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
    def show_resizing_grip(self) -> bool:
        return bool(self._com_obj.ShowResizingGrip)

    @show_resizing_grip.setter
    @ts_interface
    def show_resizing_grip(self, value: bool) -> None:
        self._com_obj.ShowResizingGrip = value

    @property
    @ts_interface
    def show_top_divider(self) -> bool:
        return bool(self._com_obj.ShowTopDivider)

    @show_top_divider.setter
    @ts_interface
    def show_top_divider(self, value: bool) -> None:
        self._com_obj.ShowTopDivider = value

    @ts_interface
    def hit_test(self, x: int, y: int) -> int:
        return int(self._com_obj.HitTest(x, y))

    @ts_interface
    def localize(self) -> None:
        self._com_obj.Localize()

    @ts_interface
    def show_panes(self) -> None:
        self._com_obj.ShowPanes()
