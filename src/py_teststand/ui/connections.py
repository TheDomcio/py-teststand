from __future__ import annotations

import typing
from enum import IntEnum, IntFlag
from typing import TYPE_CHECKING

from py_teststand.core.com_wrapper import COMWrapper, ts_interface
from py_teststand.ui.styles import (
    AutoSizingOption,
    CaptionSource,
    ImageSource,
    NumericSource,
    ShortcutModifier,
    StatusBarPaneStyle,
)


class StepProperties:
    Step_ResultProp = "Result"
    Result_NumericProp = "Numeric"
    Result_StringProp = "String"
    Result_PassFailProp = "PassFail"
    Result_StatusProp = "Status"
    ResultStatus_NoStatus = ""
    ResultStatus_Done = "Done"
    ResultStatus_Skipped = "Skipped"
    ResultStatus_Passed = "Passed"
    ResultStatus_Failed = "Failed"
    ResultStatus_Error = "Error"
    ResultStatus_Running = "Running"
    ResultStatus_Looping = "Looping"
    ResultStatus_Terminated = "Terminated"
    ResultStatus_Waiting = "Waiting"
    Step_InBufProp = "InBuf"
    Step_LimitsProp = "Limits"
    Limits_LowProp = "Low"
    Limits_HighProp = "High"
    Limits_NominalValueProp = "Nominal"
    Limits_StringProp = "String"
    Limits_ThresholdTypeProp = "ThresholdType"
    Step_TSInfoProp = "TS"
    TSInfo_StepAdditions = "SData"
    Step_MeasComparisonType = "Comp"
    NumMeasComp_EQ = "EQ"
    NumMeasComp_NE = "NE"
    NumMeasComp_GT = "GT"
    NumMeasComp_LT = "LT"
    NumMeasComp_GE = "GE"
    NumMeasComp_LE = "LE"
    NumMeasComp_GTLT = "GTLT"
    NumMeasComp_GELE = "GELE"
    NumMeasComp_GELT = "GELT"
    NumMeasComp_GTLE = "GTLE"
    NumMeasComp_LOG = "LOG"
    NumMeasRadix = "DisplayRadix"
    StrMeasComp_IgnoreCase = "IgnoreCase"
    StrMeasComp_CaseSensitive = "CaseSensitive"
    NumMeasComp_EQTHRESHOLD = "EQT"
    NumMeasThresholdType_DELTA = "DELTA"
    NumMeasThresholdType_PERCENTAGE = "PERCENTAGE"
    NumMeasThresholdType_PPM = "PPM"
    Step_MeasThresholdType = "ThresholdType"


class CommandConnectionOption(IntFlag):
    NoneValue = 0x0
    EnableImage = 8
    IgnoreCaption = 2
    IgnoreEnable = 4
    IgnoreVisible = 1


class ExpressionEditButtonKind(IntEnum):
    BrowseExpression = 1
    CheckExpression = 2
    CustomBase = 1000


class ExpressionEditButtonStyle(IntEnum):
    System = 1
    Standard = 2
    Flat = 3
    ToolBarButton = 4


class SelectionFlag(IntFlag):
    NoneValue = 0
    SetupStartSelected = 1
    MainStartSelected = 2
    CleanupStartSelected = 4
    SetupEndSelected = 8
    MainEndSelected = 16
    CleanupEndSelected = 32
    SetupCollapsed = 64
    MainCollapsed = 128
    CleanupCollapsed = 256


class SeqViewColumnType(IntEnum):
    Name = 1
    StepIndex = 2
    Description = 3
    StepSettings = 4
    ExecutionFlow = 4
    Status = 5
    Expression = 6
    Comment = 7
    Requirements = 8


class EdgeStyle(IntEnum):
    Flat = 1
    FixedSingle = 2
    ControlEdge = 3
    Raised = 4
    Inset = 5
    UI = 6


class ConnectionActivityType(IntEnum):
    BooleanChange = 3
    ContentChange = 5
    CursorOrSelectionChange = 6
    EnabledChange = 7
    ImageChange = 4
    NumberChange = 2
    TextChange = 1
    VisibleChange = 8


if TYPE_CHECKING:
    from py_teststand.execution.execution import Execution
    from py_teststand.sequence.sequence_file import SequenceFile
    from py_teststand.sequence.step_group import StepGroup
    from py_teststand.ui.application_manager import CommandKind
    from py_teststand.ui.command import ExecutionViewConnectionOption


class AdapterListConnection(COMWrapper):
    pass


class AdapterListConnections(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> AdapterListConnection:
        return AdapterListConnection(self._com_obj.Item(index), self._engine_ref)

    def __getitem__(self, index: int) -> AdapterListConnection:

        return self.item(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def add(self, ui_obj: typing.Any) -> AdapterListConnection:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        return AdapterListConnection(self._com_obj.Add(raw_ui), self._engine_ref)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def from_control(self, ui_obj: typing.Any) -> AdapterListConnection | None:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        res = self._com_obj.FromControl(raw_ui)
        return AdapterListConnection(res, self._engine_ref) if res else None

    @ts_interface
    def remove(self, index: int) -> None:
        self._com_obj.Remove(index)


class Strings(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> str:
        return str(self._com_obj.Item(int(index)))

    @ts_interface
    def set_item(self, index: int, value: str) -> None:
        self._com_obj.SetItem(int(index), str(value))

    def __getitem__(self, index: int) -> str:

        return self.item(index)

    def __setitem__(self, index: int, value: str) -> None:

        self.set_item(index, value)

    def __iter__(self):

        for i in range(len(self)):
            yield self.item(i)

    @ts_interface
    def add(self, val: str) -> None:
        self._com_obj.Add(val)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def insert(self, index: int, val: str) -> None:
        self._com_obj.Insert(index, val)

    @ts_interface
    def remove(self, index: int) -> None:
        self._com_obj.Remove(index)


class CaptionConnection(COMWrapper):
    @property
    @ts_interface
    def format_expression(self) -> str:
        return str(self._com_obj.FormatExpression)

    @format_expression.setter
    @ts_interface
    def format_expression(self, value: str) -> None:
        self._com_obj.FormatExpression = value

    @property
    @ts_interface
    def long_name(self) -> bool:
        return bool(self._com_obj.LongName)

    @long_name.setter
    @ts_interface
    def long_name(self, value: bool) -> None:
        self._com_obj.LongName = value

    @property
    @ts_interface
    def source(self) -> CaptionSource:
        return CaptionSource(self._com_obj.Source)

    @source.setter
    @ts_interface
    def source(self, value: int | CaptionSource) -> None:
        self._com_obj.Source = int(value)

    @ts_interface
    def refresh(self) -> None:
        self._com_obj.Refresh()


class CaptionConnections(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> CaptionConnection:
        return CaptionConnection(self._com_obj.Item(index), self._engine_ref)

    def __getitem__(self, index: int) -> CaptionConnection:

        return self.item(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def add(self, ui_obj: typing.Any) -> CaptionConnection:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        return CaptionConnection(self._com_obj.Add(raw_ui), self._engine_ref)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def from_control(self, ui_obj: typing.Any) -> CaptionConnection | None:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        res = self._com_obj.FromControl(raw_ui)
        return CaptionConnection(res, self._engine_ref) if res else None

    @ts_interface
    def remove(self, index: int) -> None:
        self._com_obj.Remove(index)


class CommandConnection(COMWrapper):
    @ts_interface
    def freeze_refresh(self, frz: bool) -> None:
        self._com_obj.FreezeRefresh(bool(frz))

    @property
    @ts_interface
    def index(self) -> int:
        return int(self._com_obj.Index)

    @index.setter
    @ts_interface
    def index(self, value: int) -> None:
        self._com_obj.Index = value

    @property
    @ts_interface
    def kind(self) -> CommandKind:
        from py_teststand.ui.application_manager import CommandKind

        return CommandKind(self._com_obj.Kind)

    @kind.setter
    @ts_interface
    def kind(self, value: int | CommandKind) -> None:
        self._com_obj.Kind = int(value)

    @property
    @ts_interface
    def options(self) -> CommandConnectionOption:
        return CommandConnectionOption(self._com_obj.Options)

    @options.setter
    @ts_interface
    def options(self, value: int | CommandConnectionOption) -> None:
        self._com_obj.Options = int(value)

    @ts_interface
    def refresh(self) -> None:
        self._com_obj.Refresh()


class CommandConnections(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> CommandConnection:
        return CommandConnection(self._com_obj.Item(index), self._engine_ref)

    def __getitem__(self, index: int) -> CommandConnection:

        return self.item(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def add(
        self, command_kind: int, ui_obj: typing.Any, index: int = 0, options: int = 0
    ) -> CommandConnection:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        return CommandConnection(
            self._com_obj.Add(command_kind, raw_ui, index, options), self._engine_ref
        )

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def from_control(self, ui_obj: typing.Any) -> CommandConnection | None:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        res = self._com_obj.FromControl(raw_ui)
        return CommandConnection(res, self._engine_ref) if res else None

    @ts_interface
    def remove(self, index: int) -> None:
        self._com_obj.Remove(index)


class CallStackConnection(COMWrapper):
    pass


class CallStackConnections(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> CallStackConnection:
        return CallStackConnection(self._com_obj.Item(index), self._engine_ref)

    def __getitem__(self, index: int) -> CallStackConnection:

        return self.item(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def add(self, ui_obj: typing.Any) -> CallStackConnection:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        return CallStackConnection(self._com_obj.Add(raw_ui), self._engine_ref)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def from_control(self, ui_obj: typing.Any) -> CallStackConnection | None:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        res = self._com_obj.FromControl(raw_ui)
        return CallStackConnection(res, self._engine_ref) if res else None

    @ts_interface
    def remove(self, index: int) -> None:
        self._com_obj.Remove(index)


class ExecutionListConnection(COMWrapper):
    @property
    @ts_interface
    def display_expression(self) -> str:
        return str(self._com_obj.DisplayExpression)

    @display_expression.setter
    @ts_interface
    def display_expression(self, value: str) -> None:
        self._com_obj.DisplayExpression = value

    @property
    @ts_interface
    def show_hidden_executions(self) -> bool:
        return bool(self._com_obj.ShowHiddenExecutions)

    @show_hidden_executions.setter
    @ts_interface
    def show_hidden_executions(self, value: bool) -> None:
        self._com_obj.ShowHiddenExecutions = value


class ExecutionListConnections(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> ExecutionListConnection:
        return ExecutionListConnection(self._com_obj.Item(index), self._engine_ref)

    def __getitem__(self, index: int) -> ExecutionListConnection:

        return self.item(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def add(self, ui_obj: typing.Any) -> ExecutionListConnection:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        return ExecutionListConnection(self._com_obj.Add(raw_ui), self._engine_ref)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def from_control(self, ui_obj: typing.Any) -> ExecutionListConnection | None:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        res = self._com_obj.FromControl(raw_ui)
        return ExecutionListConnection(res, self._engine_ref) if res else None

    @ts_interface
    def remove(self, index: int) -> None:
        self._com_obj.Remove(index)


class Executions(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> Execution:
        from py_teststand.execution.execution import Execution

        return Execution(self._com_obj.Item(int(index)), self._engine_ref)

    def __getitem__(self, index: int) -> Execution:

        return self.item(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @property
    @ts_interface
    def num_incomplete(self) -> int:
        return int(self._com_obj.NumIncomplete)

    @property
    @ts_interface
    def num_paused(self) -> int:
        return int(self._com_obj.NumPaused)

    @property
    @ts_interface
    def num_running(self) -> int:
        return int(self._com_obj.NumRunning)


class ExecutionViewConnection(COMWrapper):
    @property
    @ts_interface
    def color_paused(self) -> int:
        return int(self._com_obj.ColorPaused)

    @color_paused.setter
    @ts_interface
    def color_paused(self, value: int) -> None:
        self._com_obj.ColorPaused = value

    @property
    @ts_interface
    def color_running(self) -> int:
        return int(self._com_obj.ColorRunning)

    @color_running.setter
    @ts_interface
    def color_running(self, value: int) -> None:
        self._com_obj.ColorRunning = value

    @property
    @ts_interface
    def color_stopped(self) -> int:
        return int(self._com_obj.ColorStopped)

    @color_stopped.setter
    @ts_interface
    def color_stopped(self, value: int) -> None:
        self._com_obj.ColorStopped = value

    @property
    @ts_interface
    def options(self) -> ExecutionViewConnectionOption:
        from py_teststand.ui.command import ExecutionViewConnectionOption

        return ExecutionViewConnectionOption(self._com_obj.Options)

    @options.setter
    @ts_interface
    def options(self, value: int | ExecutionViewConnectionOption) -> None:
        self._com_obj.Options = int(value)

    @property
    @ts_interface
    def ui_control(self) -> typing.Any:
        return self._com_obj.UIControl


class ExecutionViewConnections(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> ExecutionViewConnection:
        return ExecutionViewConnection(self._com_obj.Item(index), self._engine_ref)

    def __getitem__(self, index: int) -> ExecutionViewConnection:

        return self.item(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def add(self, ui_obj: typing.Any) -> ExecutionViewConnection:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        return ExecutionViewConnection(self._com_obj.Add(raw_ui), self._engine_ref)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def from_control(self, ui_obj: typing.Any) -> ExecutionViewConnection | None:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        res = self._com_obj.FromControl(raw_ui)
        return ExecutionViewConnection(res, self._engine_ref) if res else None

    @ts_interface
    def remove(self, index: int) -> None:
        self._com_obj.Remove(index)


class ImageConnection(COMWrapper):
    @property
    @ts_interface
    def source(self) -> ImageSource:
        return ImageSource(self._com_obj.Source)

    @source.setter
    @ts_interface
    def source(self, value: int | ImageSource) -> None:
        self._com_obj.Source = int(value)


class ImageConnections(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> ImageConnection:
        return ImageConnection(self._com_obj.Item(index), self._engine_ref)

    def __getitem__(self, index: int) -> ImageConnection:

        return self.item(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def add(self, ui_obj: typing.Any) -> ImageConnection:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        return ImageConnection(self._com_obj.Add(raw_ui), self._engine_ref)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def from_control(self, ui_obj: typing.Any) -> ImageConnection | None:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        res = self._com_obj.FromControl(raw_ui)
        return ImageConnection(res, self._engine_ref) if res else None

    @ts_interface
    def remove(self, index: int) -> None:
        self._com_obj.Remove(index)


class SelectedSteps(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> typing.Any:
        from py_teststand.sequence.step import Step

        return Step(self._com_obj.Item(index), self._engine_ref)

    def __getitem__(self, index: int) -> typing.Any:

        return self.item(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def add_step(self, val: typing.Any) -> None:
        raw_step = getattr(val, "_com_obj", val)
        self._com_obj.AddStep(raw_step)

    @ts_interface
    def add_step_index(self, step_index: int) -> None:
        self._com_obj.AddStepIndex(step_index)

    @ts_interface
    def add_steps(self, val: list[typing.Any]) -> None:
        raw_objs = [getattr(o, "_com_obj", o) for o in val]
        self._com_obj.AddSteps(raw_objs)

    @ts_interface
    def begin_update(self) -> None:
        self._com_obj.BeginUpdate()

    @ts_interface
    def end_update(self) -> None:
        self._com_obj.EndUpdate()

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @property
    @ts_interface
    def end_selected(self) -> bool:
        return bool(self._com_obj.EndSelected)

    @end_selected.setter
    @ts_interface
    def end_selected(self, value: bool) -> None:
        self._com_obj.EndSelected = value

    @ts_interface
    def get_step_group(self, nth_selected_step: int) -> StepGroup:
        from py_teststand.sequence.step_group import StepGroup

        return StepGroup(self._com_obj.GetStepGroup(nth_selected_step))

    @ts_interface
    def get_step_index(self, nth_selected_step: int) -> int:
        return int(self._com_obj.GetStepIndex(nth_selected_step))

    @property
    @ts_interface
    def selection_flags(self) -> SelectionFlag:
        return SelectionFlag(self._com_obj.SelectionFlag)

    @selection_flags.setter
    @ts_interface
    def selection_flags(self, value: int | SelectionFlag) -> None:
        self._com_obj.SelectionFlag = int(value)


class SelectedPropertyObjects(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> typing.Any:
        from py_teststand.property.property_object import PropertyObject

        return PropertyObject(self._com_obj.Item(index), self._engine_ref)

    def __getitem__(self, index: int) -> typing.Any:

        return self.item(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def add_property_object(self, val: typing.Any) -> None:
        raw_po = getattr(val, "_com_obj", val)
        self._com_obj.AddPropertyObject(raw_po)

    @ts_interface
    def add_property_objects(self, val: list[typing.Any]) -> None:
        raw_objs = [getattr(o, "_com_obj", o) for o in val]
        self._com_obj.AddPropertyObjects(raw_objs)

    @ts_interface
    def begin_update(self) -> None:
        self._com_obj.BeginUpdate()

    @ts_interface
    def end_update(self) -> None:
        self._com_obj.EndUpdate()

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()


class SelectedSequences(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> typing.Any:
        from py_teststand.sequence.sequence import Sequence

        return Sequence(self._com_obj.Item(index), self._engine_ref)

    def __getitem__(self, index: int) -> typing.Any:

        return self.item(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def add_sequence(self, val: typing.Any) -> None:
        raw_seq = getattr(val, "_com_obj", val)
        self._com_obj.AddSequence(raw_seq)

    @ts_interface
    def add_sequences(self, val: list[typing.Any]) -> None:
        raw_objs = [getattr(o, "_com_obj", o) for o in val]
        self._com_obj.AddSequences(raw_objs)

    @ts_interface
    def begin_update(self) -> None:
        self._com_obj.BeginUpdate()

    @ts_interface
    def end_update(self) -> None:
        self._com_obj.EndUpdate()

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()


class ExpressionEditButton(COMWrapper):
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
    def context_menu_item_caption(self) -> str:
        return str(self._com_obj.ContextMenuItemCaption)

    @context_menu_item_caption.setter
    @ts_interface
    def context_menu_item_caption(self, value: str) -> None:
        self._com_obj.ContextMenuItemCaption = value

    @ts_interface
    def do_click(self) -> None:
        self._com_obj.DoClick()

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
    def h_wnd(self) -> int:
        return int(self._com_obj.hWnd)

    @property
    @ts_interface
    def icon(self) -> typing.Any:
        return self._com_obj.Icon

    @icon.setter
    @ts_interface
    def icon(self, value: typing.Any) -> None:
        self._com_obj.Icon = value

    @property
    @ts_interface
    def kind(self) -> typing.Any:

        return ExpressionEditButtonKind(self._com_obj.Kind)

    @kind.setter
    @ts_interface
    def kind(self, value: int) -> None:
        self._com_obj.Kind = value

    @property
    @ts_interface
    def shortcut_key(self) -> int:
        return int(self._com_obj.ShortcutKey)

    @shortcut_key.setter
    @ts_interface
    def shortcut_key(self, value: int) -> None:
        self._com_obj.ShortcutKey = value

    @property
    @ts_interface
    def shortcut_modifier(self) -> typing.Any:

        return ShortcutModifier(self._com_obj.ShortcutModifier)

    @shortcut_modifier.setter
    @ts_interface
    def shortcut_modifier(self, value: int) -> None:
        self._com_obj.ShortcutModifier = value

    @property
    @ts_interface
    def style(self) -> typing.Any:

        return ExpressionEditButtonStyle(self._com_obj.Style)

    @style.setter
    @ts_interface
    def style(self, value: int) -> None:
        self._com_obj.Style = value

    @property
    @ts_interface
    def image(self) -> typing.Any:
        return self._com_obj.Image

    @image.setter
    @ts_interface
    def image(self, value: typing.Any) -> None:
        self._com_obj.Image = value

    @property
    @ts_interface
    def name(self) -> str:
        return str(self._com_obj.Name)

    @property
    @ts_interface
    def tooltip_text(self) -> str:
        return str(self._com_obj.TooltipText)

    @tooltip_text.setter
    @ts_interface
    def tooltip_text(self, value: str) -> None:
        self._com_obj.TooltipText = value

    @property
    @ts_interface
    def visible(self) -> bool:
        return bool(self._com_obj.Visible)

    @visible.setter
    @ts_interface
    def visible(self, value: bool) -> None:
        self._com_obj.Visible = value


class ExpressionEditButtons(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index_or_name: typing.Any) -> ExpressionEditButton:
        return ExpressionEditButton(self._com_obj.Item(index_or_name), self._engine_ref)

    def __getitem__(self, index_or_name: typing.Any) -> ExpressionEditButton:

        return self.item(index_or_name)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def insert(self, index: int, kind: int) -> ExpressionEditButton:
        return ExpressionEditButton(self._com_obj.Insert(index, kind), self._engine_ref)

    @ts_interface
    def remove(self, index_or_name: typing.Any) -> None:
        self._com_obj.Remove(index_or_name)


class ExpressionEditComboBoxItem(COMWrapper):
    @property
    @ts_interface
    def display_name(self) -> str:
        return str(self._com_obj.DisplayName)

    @display_name.setter
    @ts_interface
    def display_name(self, value: str) -> None:
        self._com_obj.DisplayName = value

    @property
    @ts_interface
    def expression(self) -> str:
        return str(self._com_obj.Expression)

    @expression.setter
    @ts_interface
    def expression(self, value: str) -> None:
        self._com_obj.Expression = value

    @property
    @ts_interface
    def icon(self) -> typing.Any:
        return self._com_obj.Icon

    @icon.setter
    @ts_interface
    def icon(self, value: typing.Any) -> None:
        self._com_obj.Icon = value

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
    def value(self) -> str:
        return str(self._com_obj.Value)

    @value.setter
    @ts_interface
    def value(self, val: str) -> None:
        self._com_obj.Value = val


class ExpressionEditComboBoxItems(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> ExpressionEditComboBoxItem:
        return ExpressionEditComboBoxItem(self._com_obj.Item(index), self._engine_ref)

    def __getitem__(self, index: int) -> ExpressionEditComboBoxItem:

        return self.item(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def add(self, text: str, expression: str = "") -> ExpressionEditComboBoxItem:
        return ExpressionEditComboBoxItem(self._com_obj.Add(text, expression), self._engine_ref)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def insert(
        self, index: int, val: str, display_name: str = "", icon: typing.Any = None
    ) -> ExpressionEditComboBoxItem:
        return ExpressionEditComboBoxItem(
            self._com_obj.Insert(index, val, display_name, icon), self._engine_ref
        )

    @ts_interface
    def remove(self, index: int) -> None:
        self._com_obj.Remove(index)


class InsertionPalettePage(COMWrapper):
    @property
    @ts_interface
    def caption(self) -> str:
        return str(self._com_obj.Caption)

    @property
    @ts_interface
    def expanded(self) -> bool:
        return bool(self._com_obj.Expanded)

    @expanded.setter
    @ts_interface
    def expanded(self, value: bool) -> None:
        self._com_obj.Expanded = value

    @property
    @ts_interface
    def index(self) -> int:
        return int(self._com_obj.Index)

    @property
    @ts_interface
    def show_subpages(self) -> bool:
        return bool(self._com_obj.ShowSubpages)

    @show_subpages.setter
    @ts_interface
    def show_subpages(self, value: bool) -> None:
        self._com_obj.ShowSubpages = value

    @property
    @ts_interface
    def splitter_ratio(self) -> float:
        return float(self._com_obj.SplitterRatio)

    @splitter_ratio.setter
    @ts_interface
    def splitter_ratio(self, value: float) -> None:
        self._com_obj.SplitterRatio = value

    @property
    @ts_interface
    def visible(self) -> bool:
        return bool(self._com_obj.Visible)

    @visible.setter
    @ts_interface
    def visible(self, value: bool) -> None:
        self._com_obj.Visible = value


class InsertionPalettePages(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index_or_name: typing.Any) -> InsertionPalettePage:
        return InsertionPalettePage(self._com_obj.Item(index_or_name), self._engine_ref)

    def __getitem__(self, index_or_name: typing.Any) -> InsertionPalettePage:

        return self.item(index_or_name)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]


class ListBarPage(COMWrapper):
    @property
    @ts_interface
    def caption(self) -> str:
        return str(self._com_obj.Caption)

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
    def enabled(self) -> bool:
        return bool(self._com_obj.Enabled)

    @enabled.setter
    @ts_interface
    def enabled(self, value: bool) -> None:
        self._com_obj.Enabled = value

    @property
    @ts_interface
    def items(self) -> typing.Any:
        return ListBarPageItems(self._com_obj.Items, self._engine_ref)

    @property
    @ts_interface
    def name(self) -> str:
        return str(self._com_obj.Name)

    @property
    @ts_interface
    def visible(self) -> bool:
        return bool(self._com_obj.Visible)

    @visible.setter
    @ts_interface
    def visible(self, value: bool) -> None:
        self._com_obj.Visible = value


class ListBarPageItem(COMWrapper):
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
    def tooltip_text(self) -> str:
        return str(self._com_obj.TooltipText)

    @tooltip_text.setter
    @ts_interface
    def tooltip_text(self, value: str) -> None:
        self._com_obj.TooltipText = value


class ListBarPageItems(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index_or_name: typing.Any) -> ListBarPageItem:
        return ListBarPageItem(self._com_obj.Item(index_or_name), self._engine_ref)

    def __getitem__(self, index_or_name: typing.Any) -> ListBarPageItem:

        return self.item(index_or_name)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def insert(self, item_caption: str, icon_name: str, insert_before: int = -1) -> ListBarPageItem:
        return ListBarPageItem(
            self._com_obj.Insert(item_caption, icon_name, insert_before), self._engine_ref
        )

    @ts_interface
    def remove(self, index: int) -> None:
        self._com_obj.Remove(index)


class ListBarPages(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index_or_name: typing.Any) -> ListBarPage:
        return ListBarPage(self._com_obj.Item(index_or_name), self._engine_ref)

    def __getitem__(self, index_or_name: typing.Any) -> ListBarPage:

        return self.item(index_or_name)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def insert(self, page_name: str, insert_before: int = -1) -> ListBarPage:
        return ListBarPage(self._com_obj.Insert(page_name, insert_before), self._engine_ref)

    @ts_interface
    def remove(self, index: int) -> None:
        self._com_obj.Remove(index)


class ListBoxColumn(COMWrapper):
    @property
    @ts_interface
    def auto_sizing(self) -> typing.Any:

        return AutoSizingOption(self._com_obj.AutoSizing)

    @auto_sizing.setter
    @ts_interface
    def auto_sizing(self, value: int) -> None:
        self._com_obj.AutoSizing = value

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
    def index(self) -> int:
        return int(self._com_obj.Index)

    @property
    @ts_interface
    def width(self) -> int:
        return int(self._com_obj.Width)

    @width.setter
    @ts_interface
    def width(self, value: int) -> None:
        self._com_obj.Width = value


class ListBoxColumns(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> ListBoxColumn:
        return ListBoxColumn(self._com_obj.Item(index), self._engine_ref)

    def __getitem__(self, index: int) -> ListBoxColumn:

        return self.item(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]


class MRUFiles(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> str:
        return str(self._com_obj.Item(index))

    def __getitem__(self, index: int) -> str:

        return self.item(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self.item(i)

    @ts_interface
    def add(self, file_name_val: str) -> None:
        self._com_obj.Add(file_name_val)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def get_display_name(self, index: int, max_width: int = 200) -> str:
        return str(self._com_obj.GetDisplayName(index, max_width))

    @property
    @ts_interface
    def max(self) -> int:
        return int(self._com_obj.Max)

    @max.setter
    @ts_interface
    def max(self, value: int) -> None:
        self._com_obj.Max = value

    @ts_interface
    def remove(self, index: int) -> None:
        self._com_obj.Remove(index)


class NumericConnection(COMWrapper):
    @property
    @ts_interface
    def source(self) -> NumericSource:

        return NumericSource(self._com_obj.Source)

    @source.setter
    @ts_interface
    def source(self, value: int | NumericSource) -> None:
        self._com_obj.Source = int(value)

    @ts_interface
    def refresh(self) -> None:
        self._com_obj.Refresh()


class NumericConnections(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> NumericConnection:
        return NumericConnection(self._com_obj.Item(index), self._engine_ref)

    def __getitem__(self, index: int) -> NumericConnection:

        return self.item(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def add(self, ui_obj: typing.Any) -> NumericConnection:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        return NumericConnection(self._com_obj.Add(raw_ui), self._engine_ref)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def from_control(self, ui_obj: typing.Any) -> NumericConnection | None:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        res = self._com_obj.FromControl(raw_ui)
        return NumericConnection(res, self._engine_ref) if res else None

    @ts_interface
    def remove(self, index: int) -> None:
        self._com_obj.Remove(index)


class ReportViewConnection(COMWrapper):
    pass


class ReportViewConnections(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> ReportViewConnection:
        return ReportViewConnection(self._com_obj.Item(index), self._engine_ref)

    def __getitem__(self, index: int) -> ReportViewConnection:

        return self.item(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def add(self, ui_obj: typing.Any) -> ReportViewConnection:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        return ReportViewConnection(self._com_obj.Add(raw_ui), self._engine_ref)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def from_control(self, ui_obj: typing.Any) -> ReportViewConnection | None:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        res = self._com_obj.FromControl(raw_ui)
        return ReportViewConnection(res, self._engine_ref) if res else None

    @ts_interface
    def remove(self, index: int) -> None:
        self._com_obj.Remove(index)


class InsertionPaletteConnection(COMWrapper):
    @property
    @ts_interface
    def step_types_page(self) -> InsertionPalettePage:
        return InsertionPalettePage(self._com_obj.StepTypesPage, self._engine_ref)

    @property
    @ts_interface
    def templates_page(self) -> InsertionPalettePage:
        return InsertionPalettePage(self._com_obj.TemplatesPage, self._engine_ref)

    @property
    @ts_interface
    def ui_control(self) -> typing.Any:
        return self._com_obj.UIControl


class InsertionPaletteConnections(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> InsertionPaletteConnection:
        return InsertionPaletteConnection(self._com_obj.Item(index), self._engine_ref)

    def __getitem__(self, index: int) -> InsertionPaletteConnection:

        return self.item(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def add(self, ui_obj: typing.Any) -> InsertionPaletteConnection:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        return InsertionPaletteConnection(self._com_obj.Add(raw_ui), self._engine_ref)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def from_control(self, ui_obj: typing.Any) -> InsertionPaletteConnection | None:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        res = self._com_obj.FromControl(raw_ui)
        return InsertionPaletteConnection(res, self._engine_ref) if res else None

    @ts_interface
    def remove(self, index: int) -> None:
        self._com_obj.Remove(index)


class ApplicationMgrConnections(COMWrapper):
    @property
    @ts_interface
    def adapter_list(self) -> AdapterListConnections:
        return AdapterListConnections(self._com_obj.AdapterList, self._engine_ref)

    @property
    @ts_interface
    def caption(self) -> CaptionConnections:
        return CaptionConnections(self._com_obj.Caption, self._engine_ref)

    @property
    @ts_interface
    def command(self) -> CommandConnections:
        return CommandConnections(self._com_obj.Command, self._engine_ref)


class Borders(COMWrapper):
    @property
    @ts_interface
    def border_dragged_event_enabled(self) -> bool:
        return bool(self._com_obj.BorderDraggedEventEnabled)

    @border_dragged_event_enabled.setter
    @ts_interface
    def border_dragged_event_enabled(self, value: bool) -> None:
        self._com_obj.BorderDraggedEventEnabled = value

    @property
    @ts_interface
    def border_edge_style(self) -> int:
        return int(self._com_obj.BorderEdgeStyle)

    @border_edge_style.setter
    @ts_interface
    def border_edge_style(self, value: int) -> None:
        self._com_obj.BorderEdgeStyle = value

    @property
    @ts_interface
    def border_width(self) -> int:
        return int(self._com_obj.BorderWidth)

    @border_width.setter
    @ts_interface
    def border_width(self, value: int) -> None:
        self._com_obj.BorderWidth = value

    @property
    @ts_interface
    def frame_edge_style(self) -> int:
        return int(self._com_obj.FrameEdgeStyle)

    @frame_edge_style.setter
    @ts_interface
    def frame_edge_style(self, value: int) -> None:
        self._com_obj.FrameEdgeStyle = value

    @property
    @ts_interface
    def frame_edge_ui_style_color(self) -> int:
        return int(self._com_obj.FrameEdgeUIStyleColor)

    @frame_edge_ui_style_color.setter
    @ts_interface
    def frame_edge_ui_style_color(self, value: int) -> None:
        self._com_obj.FrameEdgeUIStyleColor = value

    @property
    @ts_interface
    def frame_inside_borders(self) -> bool:
        return bool(self._com_obj.FrameInsideBorders)

    @frame_inside_borders.setter
    @ts_interface
    def frame_inside_borders(self, value: bool) -> None:
        self._com_obj.FrameInsideBorders = value

    @property
    @ts_interface
    def frame_visible(self) -> bool:
        return bool(self._com_obj.FrameVisible)

    @frame_visible.setter
    @ts_interface
    def frame_visible(self, value: bool) -> None:
        self._com_obj.FrameVisible = value


class ThreadListConnection(COMWrapper):
    pass


class ThreadListConnections(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> ThreadListConnection:
        return ThreadListConnection(self._com_obj.Item(index), self._engine_ref)

    def __getitem__(self, index: int) -> ThreadListConnection:

        return self.item(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def add(self, ui_obj: typing.Any) -> ThreadListConnection:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        return ThreadListConnection(self._com_obj.Add(raw_ui), self._engine_ref)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def from_control(self, ui_obj: typing.Any) -> ThreadListConnection | None:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        res = self._com_obj.FromControl(raw_ui)
        return ThreadListConnection(res, self._engine_ref) if res else None

    @ts_interface
    def remove(self, ui_obj: typing.Any) -> bool:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        return bool(self._com_obj.Remove(raw_ui))


class SequenceViewConnection(COMWrapper):
    @property
    @ts_interface
    def double_click_edits_step_properties(self) -> bool:
        return bool(self._com_obj.DoubleClickEditsStepProperties)

    @double_click_edits_step_properties.setter
    @ts_interface
    def double_click_edits_step_properties(self, value: bool) -> None:
        self._com_obj.DoubleClickEditsStepProperties = value

    @property
    @ts_interface
    def ui_control(self) -> typing.Any:
        return self._com_obj.UIControl


class SequenceViewConnections(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> SequenceViewConnection:
        return SequenceViewConnection(self._com_obj.Item(index), self._engine_ref)

    def __getitem__(self, index: int) -> SequenceViewConnection:

        return self.item(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def add(self, ui_obj: typing.Any) -> SequenceViewConnection:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        return SequenceViewConnection(self._com_obj.Add(raw_ui), self._engine_ref)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def from_control(self, ui_obj: typing.Any) -> SequenceViewConnection | None:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        res = self._com_obj.FromControl(raw_ui)
        return SequenceViewConnection(res, self._engine_ref) if res else None

    @ts_interface
    def remove(self, ui_obj: typing.Any) -> bool:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        return bool(self._com_obj.Remove(raw_ui))


class SeqViewColumn(COMWrapper):
    @property
    @ts_interface
    def auto_sizing(self) -> typing.Any:

        return AutoSizingOption(self._com_obj.AutoSizing)

    @auto_sizing.setter
    @ts_interface
    def auto_sizing(self, value: int) -> None:
        self._com_obj.AutoSizing = value

    @property
    @ts_interface
    def back_color_expression(self) -> str:
        return str(self._com_obj.BackColorExpression)

    @back_color_expression.setter
    @ts_interface
    def back_color_expression(self, value: str) -> None:
        self._com_obj.BackColorExpression = value

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
    def expression(self) -> str:
        return str(self._com_obj.Expression)

    @expression.setter
    @ts_interface
    def expression(self, value: str) -> None:
        self._com_obj.Expression = value

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
        self._com_obj.Name = str(value)

    @property
    @ts_interface
    def text_color_expression(self) -> str:
        return str(self._com_obj.TextColorExpression)

    @text_color_expression.setter
    @ts_interface
    def text_color_expression(self, value: str) -> None:
        self._com_obj.TextColorExpression = str(value)

    @property
    @ts_interface
    def type(self) -> SeqViewColumnType:

        return SeqViewColumnType(self._com_obj.Type)

    @type.setter
    @ts_interface
    def type(self, value: int | SeqViewColumnType) -> None:
        self._com_obj.Type = int(value)

    @property
    @ts_interface
    def visible(self) -> bool:
        return bool(self._com_obj.Visible)

    @visible.setter
    @ts_interface
    def visible(self, value: bool) -> None:
        self._com_obj.Visible = bool(value)

    @property
    @ts_interface
    def width(self) -> int:
        return int(self._com_obj.Width)

    @width.setter
    @ts_interface
    def width(self, value: int) -> None:
        self._com_obj.Width = int(value)


class SeqViewColumns(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index_or_name: typing.Any) -> SeqViewColumn:
        return SeqViewColumn(self._com_obj.Item(index_or_name), self._engine_ref)

    def __getitem__(self, index_or_name: typing.Any) -> SeqViewColumn:

        return self.item(index_or_name)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def insert(self, column_name: str, column_type: int, insert_before: int = -1) -> SeqViewColumn:
        return SeqViewColumn(
            self._com_obj.Insert(column_name, column_type, insert_before), self._engine_ref
        )

    @ts_interface
    def move_left(self, index: int) -> None:
        self._com_obj.MoveLeft(index)

    @ts_interface
    def move_right(self, index: int) -> None:
        self._com_obj.MoveRight(index)

    @ts_interface
    def remove(self, index_or_name: typing.Any) -> None:
        self._com_obj.Remove(index_or_name)


class SequenceListConnection(COMWrapper):
    @property
    @ts_interface
    def show_comment_in_tip(self) -> bool:
        return bool(self._com_obj.ShowCommentInTip)

    @show_comment_in_tip.setter
    @ts_interface
    def show_comment_in_tip(self, value: bool) -> None:
        self._com_obj.ShowCommentInTip = value

    @property
    @ts_interface
    def ui_control(self) -> typing.Any:
        return self._com_obj.UIControl

    @ts_interface
    def get_column_index(self, column: int) -> int:
        return int(self._com_obj.GetColumnIndex(column))

    @ts_interface
    def get_column_visible(self, column: int) -> bool:
        return bool(self._com_obj.GetColumnVisible(column))

    @ts_interface
    def set_column_visible(self, column: int, val: bool) -> None:
        self._com_obj.SetColumnVisible(column, val)


class SequenceListConnections(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> SequenceListConnection:
        return SequenceListConnection(self._com_obj.Item(index), self._engine_ref)

    def __getitem__(self, index: int) -> SequenceListConnection:

        return self.item(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def add(self, ui_obj: typing.Any) -> SequenceListConnection:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        return SequenceListConnection(self._com_obj.Add(raw_ui), self._engine_ref)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def from_control(self, ui_obj: typing.Any) -> SequenceListConnection | None:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        res = self._com_obj.FromControl(raw_ui)
        return SequenceListConnection(res, self._engine_ref) if res else None

    @ts_interface
    def remove(self, ui_obj: typing.Any) -> bool:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        return bool(self._com_obj.Remove(raw_ui))


class SequenceFileListConnection(COMWrapper):
    @property
    @ts_interface
    def show_comment_in_tip(self) -> bool:
        return bool(self._com_obj.ShowCommentInTip)

    @show_comment_in_tip.setter
    @ts_interface
    def show_comment_in_tip(self, value: bool) -> None:
        self._com_obj.ShowCommentInTip = value

    @property
    @ts_interface
    def show_full_path(self) -> bool:
        return bool(self._com_obj.ShowFullPath)

    @show_full_path.setter
    @ts_interface
    def show_full_path(self, value: bool) -> None:
        self._com_obj.ShowFullPath = value


class SequenceFileListConnections(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> SequenceFileListConnection:
        return SequenceFileListConnection(self._com_obj.Item(index), self._engine_ref)

    def __getitem__(self, index: int) -> SequenceFileListConnection:

        return self.item(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def add(self, ui_obj: typing.Any) -> SequenceFileListConnection:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        return SequenceFileListConnection(self._com_obj.Add(raw_ui), self._engine_ref)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def from_control(self, ui_obj: typing.Any) -> SequenceFileListConnection | None:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        res = self._com_obj.FromControl(raw_ui)
        return SequenceFileListConnection(res, self._engine_ref) if res else None

    @ts_interface
    def remove(self, ui_obj: typing.Any) -> bool:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        return bool(self._com_obj.Remove(raw_ui))


class SequenceFiles(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index_or_path: typing.Any) -> SequenceFile:
        from py_teststand.sequence.sequence_file import SequenceFile

        return SequenceFile(self._com_obj.Item(index_or_path), self._engine_ref)

    def __getitem__(self, index_or_path: typing.Any) -> SequenceFile:

        return self.item(index_or_path)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]


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
    def style(self) -> typing.Any:

        return StatusBarPaneStyle(self._com_obj.Style)

    @style.setter
    @ts_interface
    def style(self, value: int) -> None:
        self._com_obj.Style = value

    @property
    @ts_interface
    def text_alignment(self) -> typing.Any:
        from py_teststand.ui.label_ctrl import AlignmentStyle

        return AlignmentStyle(self._com_obj.TextAlignment)

    @text_alignment.setter
    @ts_interface
    def text_alignment(self, value: int) -> None:
        self._com_obj.TextAlignment = value

    @property
    @ts_interface
    def tooltip_text(self) -> str:
        return str(self._com_obj.TooltipText)

    @tooltip_text.setter
    @ts_interface
    def tooltip_text(self, value: str) -> None:
        self._com_obj.TooltipText = value

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

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index_or_name: typing.Any) -> StatusBarPane:
        return StatusBarPane(self._com_obj.Item(index_or_name), self._engine_ref)

    def __getitem__(self, index_or_name: typing.Any) -> StatusBarPane:

        return self.item(index_or_name)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def insert(self, pane_name: str, insert_before: int = -1) -> StatusBarPane:
        return StatusBarPane(self._com_obj.Insert(pane_name, insert_before), self._engine_ref)

    @ts_interface
    def remove(self, index_or_name: typing.Any) -> None:
        self._com_obj.Remove(index_or_name)


class StepGroupListConnection(COMWrapper):
    @property
    @ts_interface
    def ui_control(self) -> typing.Any:
        return self._com_obj.UIControl


class StepGroupListConnections(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> StepGroupListConnection:
        return StepGroupListConnection(self._com_obj.Item(index), self._engine_ref)

    def __getitem__(self, index: int) -> StepGroupListConnection:

        return self.item(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def add(self, ui_obj: typing.Any) -> StepGroupListConnection:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        return StepGroupListConnection(self._com_obj.Add(raw_ui), self._engine_ref)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def from_control(self, ui_obj: typing.Any) -> StepGroupListConnection | None:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        res = self._com_obj.FromControl(raw_ui)
        return StepGroupListConnection(res, self._engine_ref) if res else None

    @ts_interface
    def remove(self, ui_obj: typing.Any) -> bool:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        return bool(self._com_obj.Remove(raw_ui))


class VariablesConnection(COMWrapper):
    @property
    @ts_interface
    def ui_control(self) -> typing.Any:
        return self._com_obj.UIControl


class VariablesConnections(COMWrapper):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    def __len__(self) -> int:

        return self.count

    @ts_interface
    def item(self, index: int) -> VariablesConnection:
        return VariablesConnection(self._com_obj.Item(int(index)), self._engine_ref)

    def __getitem__(self, index: int) -> VariablesConnection:

        return self.item(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    @ts_interface
    def add(self, ui_obj: typing.Any) -> VariablesConnection:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        return VariablesConnection(self._com_obj.Add(raw_ui), self._engine_ref)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def from_control(self, ui_obj: typing.Any) -> VariablesConnection | None:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        res = self._com_obj.FromControl(raw_ui)
        return VariablesConnection(res, self._engine_ref) if res else None

    @ts_interface
    def remove(self, ui_obj: typing.Any) -> bool:
        raw_ui = getattr(ui_obj, "_com_obj", ui_obj)
        return bool(self._com_obj.Remove(raw_ui))


Buttons = ExpressionEditButtons
ComboBoxItems = ExpressionEditComboBoxItems
