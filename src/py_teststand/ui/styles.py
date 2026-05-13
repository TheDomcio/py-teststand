from __future__ import annotations

from enum import IntEnum, IntFlag

from py_teststand.core.com_wrapper import COMWrapper, ts_interface


class UIStyleFont(IntEnum):
    Proportional = 0
    Monospaced = 1
    SectionHeader = 2
    Subtitle2 = 3


class FontSource(IntEnum):
    UseFontProperty = 0
    UseGUIFont = 1
    UseContainerFont = 2
    UseTitlebarFont = 3
    UseInactiveTitlebarFont = 4
    UseIconFont = 5
    UseMenuFont = 6
    UseMessageBoxFont = 7
    UsePaletteTitleFont = 8
    UseSelectedItemsFont = 9
    UseToolTipFont = 10
    UseSystemFixedWidthFont = 11
    UseUIStyleFont = 12


class MousePointerStyle(IntEnum):
    Default = 0
    Arrow = 1
    Crosshair = 2
    Ibeam = 3
    SizeNESW = 4
    SizeNS = 5
    SizeNWSE = 6
    SizeWE = 7
    UpArrow = 8
    HourGlass = 9
    NoDrop = 10
    ArrowHourGlass = 11
    ArrowQuestion = 12
    SizeAll = 13
    Custom = 99


class ContentAlignmentStyle(IntEnum):
    MiddleLeft = 0
    MiddleRight = 1
    MiddleCenter = 2
    TopLeft = 3
    TopRight = 4
    TopCenter = 5
    BottomLeft = 6
    BottomRight = 7
    BottomCenter = 8


class AlignmentStyle(IntEnum):
    LeftJustify = 0
    RightJustify = 1
    Center = 2


class AutoSizingOption(IntEnum):
    NoneValue = 0
    Proportional = 1


class StatusBarPaneStyle(IntEnum):
    Etched = 1
    Flat = 2
    Raised = 3


class UIStyleColor(IntEnum):
    Background = 0
    Background2 = 1
    Foreground = 2
    GridLine = 3
    HeaderForeground = 4
    SelectedBackground = 5
    SelectedForeground = 6
    MatchedDelimiterBackground = 7


class Color(IntEnum):
    Black = 0x000000
    White = 0xFFFFFF
    Red = 0xFF0000
    Green = 0x00FF00
    Blue = 0x0000FF


class ShortcutKey(IntEnum):
    VK_0 = 48
    VK_1 = 49
    VK_2 = 50
    VK_3 = 51
    VK_4 = 52
    VK_5 = 53
    VK_6 = 54
    VK_7 = 55
    VK_8 = 56
    VK_9 = 57
    VK_A = 65
    VK_ACCEPT = 30
    VK_ADD = 107
    VK_APPS = 93
    VK_B = 66
    VK_BACK = 8
    VK_C = 67
    VK_CANCEL = 3
    VK_CAPITAL = 20
    VK_CLEAR = 12
    VK_CONTROL = 17
    VK_CONVERT = 28
    VK_D = 68
    VK_DECIMAL = 110
    VK_DELETE = 46
    VK_DIVIDE = 111
    VK_DOWN = 40
    VK_E = 69
    VK_END = 35
    VK_ESCAPE = 27
    VK_EXECUTE = 43
    VK_F = 70
    VK_F1 = 112
    VK_F10 = 121
    VK_F11 = 122
    VK_F12 = 123
    VK_F13 = 124
    VK_F14 = 125
    VK_F15 = 126
    VK_F16 = 127
    VK_F17 = 128
    VK_F18 = 129
    VK_F19 = 130
    VK_F2 = 113
    VK_F20 = 131
    VK_F21 = 132
    VK_F22 = 133
    VK_F23 = 134
    VK_F24 = 135
    VK_F3 = 114
    VK_F4 = 115
    VK_F5 = 116
    VK_F6 = 117
    VK_F7 = 118
    VK_F8 = 119
    VK_F9 = 120
    VK_FINAL = 24
    VK_G = 71
    VK_H = 72
    VK_HANGEUL = 21
    VK_HANGUL = 21
    VK_HANJA = 25
    VK_HELP = 47
    VK_HOME = 36
    VK_I = 73
    VK_INSERT = 45
    VK_J = 74
    VK_JUNJA = 23
    VK_K = 75
    VK_KANA = 21
    VK_KANJI = 25
    VK_L = 76
    VK_LEFT = 37
    VK_LWIN = 91
    VK_M = 77
    VK_MENU = 18
    VK_MODECHANGE = 31
    VK_MULTIPLY = 106
    VK_N = 78
    VK_NEXT = 34
    VK_NONCONVERT = 29
    VK_NUMLOCK = 144
    VK_NUMPAD0 = 96
    VK_NUMPAD1 = 97
    VK_NUMPAD2 = 98
    VK_NUMPAD3 = 99
    VK_NUMPAD4 = 100
    VK_NUMPAD5 = 101
    VK_NUMPAD6 = 102
    VK_NUMPAD7 = 103
    VK_NUMPAD8 = 104
    VK_NUMPAD9 = 105
    VK_O = 79
    VK_P = 80
    VK_PAUSE = 19
    VK_PRINT = 42
    VK_PRIOR = 33
    VK_Q = 81
    VK_R = 82
    VK_RETURN = 13
    VK_RIGHT = 39
    VK_RWIN = 92
    VK_S = 83
    VK_SCROLL = 145
    VK_SELECT = 41
    VK_SEPARATOR = 108
    VK_SHIFT = 16
    VK_SNAPSHOT = 44
    VK_SPACE = 32
    VK_SUBTRACT = 109
    VK_T = 84
    VK_TAB = 9
    VK_U = 85
    VK_UP = 38
    VK_V = 86
    VK_W = 87
    VK_X = 88
    VK_Y = 89
    VK_Z = 90


class KeyModifier(IntEnum):
    Alt = 4
    Control = 2
    NoneValue = 0
    Shift = 1


class MouseButton(IntEnum):
    Left = 1
    Middle = 4
    Right = 2


class WhichBorder(IntEnum):
    Bottom = 2
    Left = 4
    NoneValue = 0
    Right = 8
    Top = 1


class CaptionSource(IntEnum):
    NotASource = 0
    MacroExpression = 1
    UUTSerialNumber = 2
    UUTStatus = 3
    BatchSerialNumber = 4
    BatchStatus = 5
    BatchState = 6
    ModelState = 7
    UserName = 8
    ProgressText = 9
    ProgressPercent = 10
    CurrentSequenceFile = 11
    CurrentSequenceFileComment = 12
    CurrentSequence = 13
    CurrentSequenceComment = 14
    CurrentStepGroup = 15
    CurrentStep = 16
    CurrentStepComment = 17
    ZeroBased = 18
    OneBased = 19
    SelectedSteps_ZeroBased = 20
    SelectedTests_OneBased = 21
    NumberOfSteps = 22
    NumberOfTests = 23
    CurrentExecution = 24
    CurrentThread = 25
    CurrentCallStackEntry = 26
    CurrentProcessModelFile = 27
    ReportLocation = 28
    TestSocketIndex = 29
    Time = 30
    Date = 31
    WithoutFileState = 32
    FileStateOnly = 33
    EngineEnvironment = 34


class ImageSource(IntEnum):
    NotASource = 0
    UUTStatus = 3
    BatchStatus = 5
    BatchState = 6
    ModelState = 7
    CurrentSequenceFile = 11
    CurrentSequence = 12
    CurrentStepGroup = 13
    CurrentStep = 14
    CurrentExecution = 21
    CurrentThread = 22
    CurrentCallStackEntry = 23
    CurrentProcessModelFile = 24
    CurrentAdapter = 25


class NumericSource(IntEnum):
    NotASource = 0
    ProgressPercent = 10


class ShortcutModifier(IntFlag):
    NoneValue = 0
    Shift = 1
    Control = 2
    Alt = 4
    NotAModifier = 0


class UIStyle(COMWrapper):
    @property
    @ts_interface
    def background_color(self) -> int:
        return int(self._com_obj.BackgroundColor)

    @property
    @ts_interface
    def font_name(self) -> str:
        return str(self._com_obj.FontName)

    @property
    @ts_interface
    def font_size(self) -> float:
        return float(self._com_obj.FontSize)

    @property
    @ts_interface
    def foreground_color(self) -> int:
        return int(self._com_obj.ForegroundColor)

    @property
    @ts_interface
    def grid_line_color(self) -> int:
        return int(self._com_obj.GridLineColor)

    @property
    @ts_interface
    def header_foreground_color(self) -> int:
        return int(self._com_obj.HeaderForegroundColor)

    @property
    @ts_interface
    def section_header_font_name(self) -> str:
        return str(self._com_obj.SectionHeaderFontName)

    @property
    @ts_interface
    def section_header_font_size(self) -> float:
        return float(self._com_obj.SectionHeaderFontSize)

    @property
    @ts_interface
    def selected_background_color(self) -> int:
        return int(self._com_obj.SelectedBackgroundColor)

    @property
    @ts_interface
    def selected_foreground_color(self) -> int:
        return int(self._com_obj.SelectedForegroundColor)

    @ts_interface
    def get_color(self, color_index: int) -> int:
        return int(self._com_obj.GetColor(int(color_index)))

    @ts_interface
    def get_font_type_name(self, font_index: int) -> str:
        return str(self._com_obj.GetFontTypeName(int(font_index)))

    @ts_interface
    def get_font_type_size(self, font_index: int) -> float:
        return float(self._com_obj.GetFontTypeSize(int(font_index)))

    @ts_interface
    def set_style(self, style_string: str) -> None:
        self._com_obj.SetStyle(str(style_string))
