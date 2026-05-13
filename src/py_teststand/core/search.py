from __future__ import annotations

from enum import IntFlag

from py_teststand.core.com_wrapper import COMWrapper, ts_interface


class SearchOption(IntFlag):
    def __str__(self) -> str:
        return str(self.value)

    MatchCase = 0x1
    WholeWordOnly = 0x2
    RegExpr = 0x4
    IncludeSubsequenceFiles = 0x8


Search = SearchOption


class SearchFilterOption(IntFlag):
    def __str__(self) -> str:
        return str(self.value)

    Locals = 0x1
    Parameters = 0x2
    FileGlobals = 0x4
    Steps = 0x8
    CustomStepProps = 0x10
    BuiltinStepProps = 0x20
    ModuleStepProps = 0x40
    StepTypes = 0x80
    CustomDataTypes = 0x100
    StandardDataTypes = 0x200
    BuiltinSeqAndSeqFileProps = 0x400
    All = 0x00FFFFFF
    TypesOnly = 0x01000000


SearchFilter = SearchFilterOption


class SearchElement(IntFlag):
    def __str__(self) -> str:
        return str(self.value)

    Name = 0x1
    Comment = 0x2
    StringValue = 0x4
    NumericValue = 0x8
    BooleanValue = 0x10
    Attributes = 0x20
    TypeName = 0x40
    Enumerators = 0x80
    AllValues = 0x1C
    All = -1


class SearchMatch(COMWrapper):
    @property
    @ts_interface
    def file_display_name(self) -> str:
        return str(self._com_obj.FileDisplayName)

    @property
    @ts_interface
    def file_id(self) -> int:
        return int(self._com_obj.FileId)

    @property
    @ts_interface
    def file_path(self) -> str:
        return str(self._com_obj.FilePath)

    @ts_interface
    def get_location(self) -> tuple[int, int, int]:
        return self._com_obj.GetLocation()

    @ts_interface
    def get_property_path(self, use_names_for_indices: bool = False) -> str:
        return str(self._com_obj.GetPropertyPath(bool(use_names_for_indices)))

    @property
    @ts_interface
    def matched_text(self) -> str:
        return str(self._com_obj.MatchedText)

    @property
    @ts_interface
    def match_is_valid(self) -> bool:
        return bool(self._com_obj.MatchIsValid)

    @property
    @ts_interface
    def property_value_as_string(self) -> str:
        return str(self._com_obj.PropertyValueAsString)

    @property
    @ts_interface
    def property_value_type(self) -> int:
        return int(self._com_obj.PropertyValueType)

    @property
    @ts_interface
    def type_category_of_match(self) -> int:
        return int(self._com_obj.TypeCategoryOfMatch)

    @ts_interface
    def update_for_replace(self, replacement_string: str) -> None:
        self._com_obj.UpdateForReplace(str(replacement_string))

    @ts_interface
    def update_for_replace_value(self, new_value: str) -> None:
        self._com_obj.UpdateForReplaceValue(str(new_value))

    @property
    @ts_interface
    def user_data(self) -> int:
        return int(self._com_obj.UserData)

    @user_data.setter
    @ts_interface
    def user_data(self, value: int) -> None:
        self._com_obj.UserData = int(value)


class SearchResults(COMWrapper):
    @property
    @ts_interface
    def num_matches(self) -> int:
        return int(self._com_obj.NumMatches)

    @property
    @ts_interface
    def num_warnings(self) -> int:
        return int(self._com_obj.NumWarnings)

    @property
    @ts_interface
    def status_message(self) -> str:
        return str(self._com_obj.StatusMessage)

    @ts_interface
    def get_match(self, index: int) -> SearchMatch:
        return SearchMatch(self._com_obj.GetMatch(int(index)), self._engine_ref)

    @ts_interface
    def get_warning(self, index: int) -> str:
        return str(self._com_obj.GetWarning(int(index)))

    @ts_interface
    def cancel(
        self,
        wait_for_complete: bool = False,
        process_windows_msgs_while_waiting: bool = True,
    ) -> None:
        self._com_obj.Cancel(bool(wait_for_complete), bool(process_windows_msgs_while_waiting))

    @ts_interface
    def is_complete(
        self,
        wait_for_complete: bool = False,
        process_windows_msgs_while_waiting: bool = True,
    ) -> bool:
        return bool(
            self._com_obj.IsComplete(
                bool(wait_for_complete), bool(process_windows_msgs_while_waiting)
            )
        )
