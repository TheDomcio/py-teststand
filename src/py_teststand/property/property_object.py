from __future__ import annotations

import datetime
import functools
import typing
from enum import IntEnum, IntFlag
from typing import TYPE_CHECKING

try:
    import pythoncom
    import pywintypes
    import win32com
    import win32com.client
except ImportError:
    pywintypes: typing.Any = None
    pythoncom: typing.Any = None
    win32com: typing.Any = None

from py_teststand.core.com_wrapper import COMWrapper, ts_interface


def _is_2d_list(value: typing.Any) -> bool:
    if not isinstance(value, (list, tuple)) or len(value) == 0:
        return False
    first = value[0]
    return isinstance(first, (list, tuple))


def _make_2d_variant(value: typing.Any) -> typing.Any:
    if win32com is None or pythoncom is None:
        return value
    rows = [list(row) for row in value]
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_VARIANT, rows)


class PropertyOption(IntFlag):
    NoneValue = 0
    InsertIfMissing = 0x1
    DeleteIfExists = 0x2
    DoNothingIfExists = 0x4
    SetOnlyIfDoesNotExist = 0x5
    CoerceBadNumbersToZero = 0x40000
    CoerceFromNumber = 0x8
    CoerceFromString = 0x10
    CoerceFromBoolean = 0x20
    CoerceFromReference = 0x10000
    CoerceToNumber = 0x40
    CoerceToString = 0x80
    CoerceToBoolean = 0x100
    CoerceToReference = 0x20000
    Coerce = 0x301F8
    OverrideNotDeletable = 0x400000
    NotOwning = 0x200
    ReferToAlias = 0x400
    RequireIdenticalStructure = 0x2000
    CaseInsensitive = 0x1000
    DoNotRecurse = 0x4000
    DoNotShareProperties = 0x8000000
    CopyAllFlags = 0x20000000
    DoNotAdoptCurrentName = 0x800
    CoerceFromEnum = 192
    CoerceToEnum = 24


class PropertyFlag(IntFlag):
    NoneValue = 0
    NotEditable = 0x1
    PassByReference = 0x4
    Hidden = 0x8
    HiddenInTypes = 0x10
    IntermediateExprValue = 0x40
    DontTypeCheckParameter = 0x80
    Propagate = 0x100
    PermitPropagation = 0x200
    IsMeasurementValue = 0x400
    DontCopyToResults = 0x800
    IsLimit = 0x1000
    IncludeInReport = 0x2000
    ExcludeFromComparison = 0x10000
    Shared = 0x20000
    SharedAtRunTime = 0x40000
    ExcludeFromCopy = 0x80000
    UnstructuredProperty = 0x200000
    NotDeletable = 0x400000
    CommentNotEditable = 0x1000000
    SerializeAlias = 0x2000000
    NameNotEditable = 0x4000000


class EvaluationOption(IntFlag):
    NoneValue = 0
    DoNotAlterValues = 0x1
    AllowEmptyExpression = 0x2
    AllowIndexingEmptyArrays = 0x4
    CreateNonExistentVariables = 0x8
    ForErrorChecking = 0x10
    IgnoreNoValidationDirective = 0x20
    NoOptions = 0


class PropertyObjectElement(IntEnum):
    NoneValue = 0
    Value = 1
    Name = 2
    Comment = 3
    Flags = 4
    NumericFormat = 5
    Representation = 6
    Attributes = 7


class PropValType(IntEnum):
    Container = 0
    String = 1
    Boolean = 2
    Number = 3
    NamedType = 4
    Reference = 5
    Array = 6
    Enum = 7


class XMLOption(IntFlag):
    NoneValue = 0
    ExcludeComments = 1
    ExcludeFlags = 2
    ExcludeVersionInfo = 4
    ExcludeEmptyObjects = 8
    UseValueFormatIfDefined = 16
    NoIndentation = 32
    NoCRLF = 64
    UseCRLFInsteadOfLF = 128
    ExcludeAliasObjects = 256
    ExcludeArrayPrototypes = 512
    ExcludeAttributes = 3072
    AllowInvalidObjects = 4096


class CopyLocation(IntEnum):
    ShallowCopy = 1
    DeepCopy = 2


class TypeCategory(IntEnum):
    NoneValue = 0
    StepTypes = 1
    CustomDataTypes = 2
    BuiltinDataTypes = 3


class NamedPropertyType:
    CommonResults = "CommonResults"
    Error = "Error"
    FCParam = "FCParameter"
    Path = "Path"


class PropertyDialogOption(IntFlag):
    NoneValue = 0
    NoOptions = 0
    ShowViewContentsButton = 2
    DisableAdvancedButton = 4
    DisableNumericFormatButton = 8
    UseVariablesViewDialog = 16
    ModalToAppMainWind = 65536
    ReadOnly = 131072


class PropertyDialogOutput(IntFlag):
    AppliedToAllInstances = 1
    AppliedChanges = 2
    ViewContents = 4
    ModifiedObject = 8
    ModifiedFile = 16


class PropertyObjectFileContentType:
    AdaptersConfigFile = "AdaptersConfigFile"
    ConfigFile = "TEConfigFile"
    CustomConfigFile = "CustomConfigFile"
    GeneralEngineConfigFile = "GeneralEngineConfigFile"
    ProjectFile = "TSProjectFile"
    PropertyObjectFile = "PropertyObjectFile"
    SearchDirectoriesConfigFile = "SearchDirectoriesConfigFile"
    SequenceFile = "SequenceFile"
    StationGlobalsFile = "Globals"
    TypePaletteFile = "Types"
    TypePalettesConfigFile = "TypePalettesConfigFile"
    UsersFile = "UserListFile"
    WorkspaceFile = "TSWorkspaceFile"


class ReadWriteOption(IntFlag):
    NoneValue = 0
    NoOptions = 0
    ValuesOnly = 1
    EraseExistingObject = 2
    EraseAll = 4
    DoNotWriteTypes = 8


class TypeEqualOption(IntFlag):
    NoneValue = 0
    NoOptions = 0
    DoNotCompareDimensions = 1
    DoNotCompareIsObject = 2


if TYPE_CHECKING:
    from py_teststand.execution.report import ReportSection


class PropertyObject(COMWrapper):
    @property
    def _property_object(self) -> typing.Any:

        if "Mock" in str(type(self._com_obj)):
            return self._com_obj

        if hasattr(self._com_obj, "GetValVariant"):
            return self._com_obj

        try:
            return self._com_obj.AsPropertyObject()
        except Exception:
            pass

        try:
            from win32com.client import CastTo

            return CastTo(self._com_obj, "IPropertyObject")
        except Exception:
            pass

        try:
            if hasattr(self._com_obj, "_oleobj_"):
                import win32com.client.dynamic

                return win32com.client.dynamic.Dispatch(self._com_obj._oleobj_)
        except Exception:
            pass

        return self._com_obj

    def __getitem__(self, index: typing.Any) -> typing.Any:

        lookup_string = index
        if isinstance(lookup_string, int):
            if lookup_string < 0:
                lookup_string = self.get_num_elements() + lookup_string
            lookup_string = f"[{lookup_string}]"

        if not isinstance(lookup_string, str):
            raise TypeError(f"PropertyObject lookup must be a string, got {type(lookup_string)}")

        if "Mock" in str(type(self._com_obj)):
            return self.get_val_variant(lookup_string, PropertyOption.NoneValue)

        try:
            type_info = self._property_object.GetType(lookup_string, 0)
            try:
                category = int(type_info[0])
                is_array = bool(type_info[2])
                if is_array or category in (0, 5, 6, 8):
                    return self.get_property_object(lookup_string)
            except (ValueError, TypeError, IndexError):
                pass
        except Exception:
            pass
        return self.get_val_variant(lookup_string, PropertyOption.NoneValue)

    def __setitem__(self, lookup_string: str, value: typing.Any) -> None:

        if isinstance(value, COMWrapper):
            self._property_object.SetValVariant(
                lookup_string,
                PropertyOption.NoneValue,
                value._com_obj,
            )
        else:
            self.set_val_variant(lookup_string, PropertyOption.NoneValue, value)

    def __getattr__(self, name: str) -> typing.Any:

        if name.startswith("_") or name in self.__dict__:
            return object.__getattribute__(self, name)

        if "Mock" in str(type(self._com_obj)):
            return super().__getattr__(name)

        try:
            property_object = self._property_object
            if property_object.Exists(name, 0):
                ti = property_object.GetType(name, 0)
                try:
                    category = int(ti[0])
                    is_array = bool(ti[2])
                    if is_array or category in (0, 5, 6, 8):
                        com_sub = property_object.GetPropertyObject(name, 0)
                        return PropertyObject(com_sub, self._engine_ref) if com_sub else None
                except (ValueError, TypeError, IndexError):
                    pass

                return property_object.GetValVariant(name, 0)
        except Exception:
            pass

        try:
            return super().__getattr__(name)
        except Exception as e:
            raise AttributeError(f"Property '{name}' not found on {self!r}") from e

    def __setattr__(self, name: str, value: typing.Any) -> None:

        if name.startswith("_") or name in self.__dict__:
            object.__setattr__(self, name, value)
            return

        cls_attr = getattr(self.__class__, name, None)
        if cls_attr is not None and hasattr(cls_attr, "__set__"):
            cls_attr.__set__(self, value)
            return

        if "Mock" in str(type(self._com_obj)):
            super().__setattr__(name, value)
            return

        try:
            property_object = self._property_object
            if property_object.Exists(name, 0):
                val_com = getattr(value, "_com_obj", value) if value is not None else None
                property_object.SetValVariant(name, 0, val_com)
                return
        except Exception:
            pass

        try:
            super().__setattr__(name, value)
        except Exception as e:
            raise AttributeError(f"Could not set '{name}' on {self!r}") from e

    def __len__(self) -> int:

        try:
            if self.is_array:
                return self.get_num_elements()
            return self.get_num_sub_properties()
        except Exception:
            return 0

    def __iter__(self) -> typing.Iterator[typing.Any]:
        if self.is_array:
            for i in range(self.get_num_elements()):
                yield self.get_property_object_by_offset(i, 0)
        else:
            for i in range(self.get_num_sub_properties()):
                yield self.get_nth_sub_property("", i)

    @ts_interface
    def get_val_variant(self, lookup_string: str = "", options: int = 0) -> typing.Any:
        return self._property_object.GetValVariant(lookup_string, options)

    @ts_interface
    def set_val_variant(
        self,
        lookup_string: str = "",
        options: int = 0,
        value: typing.Any = None,
    ) -> typing.Any:
        if pythoncom is not None and win32com is not None:
            if isinstance(value, bool):
                try:
                    value = win32com.client.VARIANT(pythoncom.VT_BOOL, -1 if value else 0)
                except Exception:
                    pass
            elif _is_2d_list(value):
                try:
                    value = _make_2d_variant(value)
                except Exception:
                    pass
            elif isinstance(value, (list, tuple)):
                try:
                    value = win32com.client.VARIANT(
                        pythoncom.VT_ARRAY | pythoncom.VT_VARIANT,
                        list(value),
                    )
                except Exception:
                    value = tuple(typing.cast("typing.Any", value))
        elif isinstance(value, datetime.datetime) and pywintypes is not None:
            value = pywintypes.Time(value)
        self._property_object.SetValVariant(lookup_string, options, value)

    @ts_interface
    def get_val_string(self, lookup_string: str = "", options: int = 0) -> typing.Any:
        return str(self._property_object.GetValString(lookup_string, options))

    @ts_interface
    def set_val_string(
        self,
        lookup_string: str = "",
        options: int = 0,
        value: str = "",
    ) -> typing.Any:
        self._property_object.SetValString(lookup_string, options, value)

    @ts_interface
    def get_val_number(self, lookup_string: str = "", options: int = 0) -> typing.Any:
        return float(self._property_object.GetValNumber(lookup_string, options))

    @ts_interface
    def set_val_number(
        self,
        lookup_string: str = "",
        options: int = 0,
        value: float = 0.0,
    ) -> typing.Any:
        self._property_object.SetValNumber(lookup_string, options, value)

    @ts_interface
    def get_val_boolean(self, lookup_string: str = "", options: int = 0) -> typing.Any:
        return bool(self._property_object.GetValBoolean(lookup_string, options))

    @ts_interface
    def set_val_boolean(
        self,
        lookup_string: str = "",
        options: int = 0,
        value: bool = False,
    ) -> None:
        self._property_object.SetValBoolean(lookup_string, options, value)

    @ts_interface
    def new_sub_property(
        self,
        lookup_string: str,
        value_type: PropValType,
        as_array: bool,
        type_name: str,
        options: int = 0,
    ) -> None:
        self._property_object.NewSubProperty(
            lookup_string,
            int(value_type),
            as_array,
            type_name,
            int(options),
        )

    @ts_interface
    def insert_sub_property(
        self,
        lookup_string: str,
        value_type: PropValType,
        as_array: bool,
        sub_property: PropertyObject,
    ) -> None:
        raw_sub = getattr(sub_property, "_com_obj", sub_property)
        self._property_object.InsertSubProperty(lookup_string, int(value_type), as_array, raw_sub)

    @ts_interface
    def evaluate(self, expression: str) -> typing.Any:
        return PropertyObject(self._property_object.Evaluate(expression), self._engine_ref)

    @ts_interface
    def evaluate_ex(
        self,
        expression: str,
        options: EvaluationOption = EvaluationOption.NoneValue,
    ) -> PropertyObject | None:
        res_com = self._property_object.EvaluateEx(expression, int(options))
        return PropertyObject(res_com, self._engine_ref) if res_com else None

    @ts_interface
    def clone(
        self,
        lookup_string: str = "",
        options: PropertyOption = PropertyOption.NoneValue,
    ) -> PropertyObject:
        return PropertyObject(
            self._property_object.Clone(lookup_string, int(options)),
            self._engine_ref,
        )

    @ts_interface
    def search(
        self,
        lookup_string: str = "",
        search_string: str = "",
        search_options: int = 0,
        filter_options: int = 0,
        elements_to_search: int = 0,
        limit_to_adapters: list[str] | None = None,
        limit_to_named_props: list[str] | None = None,
        limit_to_props_of_named_types: list[str] | None = None,
        subprop_lookup_strings_to_exclude: list[str] | None = None,
    ) -> typing.Any:
        return self._property_object.Search(
            lookup_string,
            search_string,
            search_options,
            filter_options,
            elements_to_search,
            limit_to_adapters or [],
            limit_to_named_props or [],
            limit_to_props_of_named_types or [],
            subprop_lookup_strings_to_exclude or [],
        )

    @ts_interface
    def set_flags(
        self,
        lookup_string: str,
        options: PropertyOption | int,
        flags: PropertyFlag | int,
    ) -> None:
        self._property_object.SetFlags(lookup_string, int(options), int(flags))

    @ts_interface
    def get_property_object(
        self,
        lookup_string: str,
        options: PropertyOption | int = 0,
    ) -> PropertyObject | None:
        com_obj = self._property_object.GetPropertyObject(lookup_string, int(options))
        return PropertyObject(com_obj, self._engine_ref) if com_obj else None

    @ts_interface
    def get_sub_property(self, lookup_string: str, options: int = 0) -> PropertyObject | None:
        return self.get_property_object(lookup_string, options)

    @ts_interface
    def exists(self, lookup_string: str, options: int = 0) -> typing.Any:
        return bool(self._property_object.Exists(lookup_string, options))

    @ts_interface
    def validate_new_name(self, new_name: str, allow_duplicates: bool = False) -> typing.Any:
        res = self._property_object.ValidateNewName(new_name, allow_duplicates)
        if isinstance(res, tuple) and len(res) >= 2:
            return bool(res[1]), str(res[0])
        return bool(res), ""

    @ts_interface
    def validate_new_sub_property_name(
        self,
        name: str,
        allow_duplicates: bool = False,
    ) -> tuple[bool, str]:
        res = self._property_object.ValidateNewSubPropertyName(name, allow_duplicates)
        if isinstance(res, tuple) and len(res) >= 2:
            return bool(res[1]), str(res[0])
        return bool(res), ""

    @property
    @ts_interface
    def name(self) -> str:
        return str(getattr(self._com_obj, "Name", ""))

    @name.setter
    @ts_interface
    def name(self, value: str) -> None:
        if hasattr(self._com_obj, "Name"):
            self._com_obj.Name = value

    @functools.cached_property
    @ts_interface
    def type_name(self) -> str:
        return str(getattr(self._com_obj, "TypeName", ""))

    @property
    @ts_interface
    def type_obj(self) -> typing.Any:
        return self._property_object.Type

    def get_type_name(self, lookup_string: str = "", options: PropertyOption | int = 0) -> str:
        return self.get_type(lookup_string, options)[3]

    @ts_interface
    def get_type(
        self,
        lookup_string: str = "",
        options: PropertyOption | int = 0,
    ) -> tuple[PropValType, bool, bool, str]:

        res = self._property_object.GetType(lookup_string, int(options), False, False, "")
        if isinstance(res, tuple) and len(res) >= 4:
            return PropValType(res[0]), bool(res[1]), bool(res[2]), str(res[3])
        return PropValType.Container, False, False, ""

    @property
    @ts_interface
    def is_array(self) -> bool:
        res = self.get_type("", 0)
        return bool(res[2])

    @property
    @ts_interface
    def can_add_sub_property(self) -> bool:
        return bool(self._property_object.CanAddSubProperty)

    @property
    @ts_interface
    def comment(self) -> str:
        return str(self._property_object.Comment)

    @comment.setter
    @ts_interface
    def comment(self, value: str) -> None:
        self._property_object.Comment = value

    @property
    @ts_interface
    def attributes(self) -> PropertyObject:
        return PropertyObject(self._property_object.Attributes, self._engine_ref)

    @property
    @ts_interface
    def numeric_format(self) -> str:
        return str(self._property_object.NumericFormat)

    @numeric_format.setter
    @ts_interface
    def numeric_format(self, value: str) -> None:
        self._property_object.NumericFormat = value

    def to_list(self) -> list[typing.Any]:

        if not self.is_array:
            raise ValueError(f"PropertyObject '{self.name}' is not an array.")

        try:
            res = self.get_val_variant("", PropertyOption.NoneValue)
            if isinstance(res, (list, tuple)):
                return list(res)
        except Exception:
            pass

        num_elements = self.get_num_elements()
        return [self.get_val_variant(f"[{i}]") for i in range(num_elements)]

    @property
    @ts_interface
    def type_version(self) -> str:
        return str(self._com_obj.TypeVersion)

    @property
    @ts_interface
    def type_last_modified(self) -> str:
        return str(self._property_object.TypeLastModified)

    @property
    @ts_interface
    def type_minimum_teststand_version(self) -> str:
        return str(self._property_object.TypeMinimumTestStandVersion)

    @type_minimum_teststand_version.setter
    @ts_interface
    def type_minimum_teststand_version(self, value: str) -> None:
        self._property_object.TypeMinimumTestStandVersion = value

    @property
    @ts_interface
    def is_type_definition(self) -> bool:
        return bool(self._property_object.IsTypeDefinition)

    @property
    @ts_interface
    def is_root_type_definition(self) -> bool:
        return bool(self._property_object.IsRootTypeDefinition)

    @property
    @ts_interface
    def is_modified_type(self) -> bool:
        return bool(self._property_object.IsModifiedType)

    @is_modified_type.setter
    @ts_interface
    def is_modified_type(self, value: bool) -> None:
        self._property_object.IsModifiedType = value

    @ts_interface
    def delete_sub_property(self, lookup_string: str, options: int = 0) -> typing.Any:
        self._property_object.DeleteSubProperty(lookup_string, options)

    @ts_interface
    def delete_nth_sub_property(
        self,
        lookup_string: str,
        index: int,
        options: int = 0,
    ) -> typing.Any:
        self._property_object.DeleteNthSubProperty(lookup_string, index, options)

    @ts_interface
    def get_num_elements(self) -> int:
        return int(self._property_object.GetNumElements())

    @ts_interface
    def set_num_elements(self, num_elements: int, options: int = 0) -> typing.Any:
        self._property_object.SetNumElements(num_elements, options)

    @ts_interface
    def get_num_sub_properties(self, lookup_string: str = "") -> typing.Any:
        return int(self._property_object.GetNumSubProperties(lookup_string))

    @ts_interface
    def get_nth_sub_property_name(
        self,
        lookup_string: str = "",
        index: int = 0,
        options: int = 0,
    ) -> str:
        return str(self._property_object.GetNthSubPropertyName(lookup_string, index, options))

    @ts_interface
    def get_nth_sub_property(
        self,
        lookup_string: str = "",
        index: int = 0,
        options: int = 0,
    ) -> PropertyObject | None:
        com_obj = self._property_object.GetNthSubProperty(lookup_string, index, options)
        return PropertyObject(com_obj, self._engine_ref) if com_obj else None

    @ts_interface
    def get_flags(self, lookup_string: str = "", options: PropertyOption | int = 0) -> PropertyFlag:

        return PropertyFlag(int(self._property_object.GetFlags(lookup_string, int(options))))

    @ts_interface
    def get_type_definition(self, lookup_string: str = "", options: int = 0) -> typing.Any:
        com_obj = self._property_object.GetTypeDefinition(lookup_string, options)
        return PropertyObject(com_obj, self._engine_ref) if com_obj else None

    @ts_interface
    def get_type_display_string(self, lookup_string: str = "", options: int = 0) -> typing.Any:
        return str(self._property_object.GetTypeDisplayString(lookup_string, options))

    @ts_interface
    def get_type_flags(self, lookup_string: str = "", options: int = 0) -> typing.Any:
        return int(self._property_object.GetTypeFlags(lookup_string, options))

    @ts_interface
    def get_formatted_value(
        self,
        lookup_string: str = "",
        options: int = 0,
        format_string: str = "",
        use_value_format_if_defined: bool = False,
        separator: str = "",
    ) -> str:
        return str(
            self._property_object.GetFormattedValue(
                lookup_string,
                options,
                format_string,
                use_value_format_if_defined,
                separator,
            ),
        )

    @ts_interface
    def get_property_object_by_offset(
        self,
        array_offset: int,
        options: int = 0,
    ) -> PropertyObject | None:
        com_obj = self._property_object.GetPropertyObjectByOffset(array_offset, options)
        return PropertyObject(com_obj, self._engine_ref) if com_obj else None

    @ts_interface
    def get_val_boolean_by_offset(self, array_offset: int, options: int = 0) -> typing.Any:
        return bool(self._property_object.GetValBooleanByOffset(array_offset, options))

    @ts_interface
    def get_val_number_by_offset(self, array_offset: int, options: int = 0) -> typing.Any:
        return float(self._property_object.GetValNumberByOffset(array_offset, options))

    @ts_interface
    def get_val_string_by_offset(self, array_offset: int, options: int = 0) -> typing.Any:
        return str(self._property_object.GetValStringByOffset(array_offset, options))

    @ts_interface
    def get_val_variant_by_offset(self, array_offset: int, options: int = 0) -> typing.Any:
        return self._property_object.GetValVariantByOffset(array_offset, options)

    @ts_interface
    def set_val_boolean_by_offset(
        self,
        array_offset: int,
        options: int = 0,
        value: bool = False,
    ) -> None:
        self._property_object.SetValBooleanByOffset(array_offset, options, value)

    @ts_interface
    def set_val_number_by_offset(
        self,
        array_offset: int,
        options: int = 0,
        value: float = 0.0,
    ) -> None:
        self._property_object.SetValNumberByOffset(array_offset, options, value)

    @ts_interface
    def set_val_string_by_offset(
        self,
        array_offset: int,
        options: int = 0,
        value: str = "",
    ) -> None:
        self._property_object.SetValStringByOffset(array_offset, options, value)

    @ts_interface
    def set_val_variant_by_offset(
        self,
        array_offset: int,
        options: int = 0,
        value: typing.Any = None,
    ) -> None:
        if pythoncom is not None and win32com is not None:
            if isinstance(value, bool):
                try:
                    value = win32com.client.VARIANT(pythoncom.VT_BOOL, -1 if value else 0)
                except Exception:
                    pass
            elif _is_2d_list(value):
                try:
                    value = _make_2d_variant(value)
                except Exception:
                    pass
            elif isinstance(value, (list, tuple)):
                try:
                    value = win32com.client.VARIANT(
                        pythoncom.VT_ARRAY | pythoncom.VT_VARIANT,
                        list(value),
                    )
                except Exception:
                    value = value
        elif isinstance(value, datetime.datetime) and pywintypes is not None:
            value = pywintypes.Time(value)
        self._property_object.SetValVariantByOffset(array_offset, options, value)

    @ts_interface
    def get_val_integer64(self, lookup_string: str = "", options: int = 0) -> typing.Any:
        return int(self._property_object.GetValInteger64(lookup_string, options))

    @ts_interface
    def set_val_integer64(
        self,
        lookup_string: str = "",
        options: int = 0,
        value: int = 0,
    ) -> typing.Any:
        self._property_object.SetValInteger64(lookup_string, options, value)

    @ts_interface
    def get_val_unsigned_integer64(self, lookup_string: str = "", options: int = 0) -> typing.Any:
        return int(self._property_object.GetValUnsignedInteger64(lookup_string, options))

    @ts_interface
    def set_val_unsigned_integer64(
        self,
        lookup_string: str = "",
        options: int = 0,
        value: int = 0,
    ) -> None:
        self._property_object.SetValUnsignedInteger64(lookup_string, options, value)

    @ts_interface
    def get_handle(self, lookup_string: str = "", options: int = 0) -> int:
        engine = self.engine
        if engine is not None and bool(engine.is_64bit):
            try:
                return self.get_val_integer64(lookup_string, options)
            except Exception:
                return int(self.get_val_number(lookup_string, options))
        return int(self.get_val_number(lookup_string, options))

    @ts_interface
    def set_handle(self, lookup_string: str = "", options: int = 0, value: int = 0) -> None:
        engine = self.engine
        if engine is not None and bool(engine.is_64bit):
            try:
                self.set_val_integer64(lookup_string, options, value)
                return
            except Exception:
                pass
        self.set_val_number(lookup_string, options, float(value))

    @ts_interface
    def get_val_binary(self, lookup_string: str = "", options: int = 0) -> typing.Any:
        return bytes(self._property_object.GetValBinary(lookup_string, options))

    @ts_interface
    def set_val_binary(self, lookup_string: str, options: int, value: bytes) -> typing.Any:
        self._property_object.SetValBinary(lookup_string, options, value)

    @ts_interface
    def get_val_interface(self, lookup_string: str = "", options: int = 0) -> typing.Any:
        com_obj = self._property_object.GetValInterface(lookup_string, options)
        return PropertyObject(com_obj, self._engine_ref) if com_obj else None

    @ts_interface
    def set_val_interface(
        self,
        lookup_string: str = "",
        options: int = 0,
        value: typing.Any = None,
    ) -> None:
        val_com = getattr(value, "_com_obj", value) if value else None
        self._property_object.SetValInterface(lookup_string, options, val_com)

    @ts_interface
    def insert_elements(self, array_offset: int, num_elements: int, options: int = 0) -> typing.Any:
        self._property_object.InsertElements(array_offset, num_elements, options)

    @ts_interface
    def delete_elements(self, array_offset: int, num_elements: int, options: int = 0) -> typing.Any:
        self._property_object.DeleteElements(array_offset, num_elements, options)

    @ts_interface
    def set_property_object(
        self,
        lookup_string: str,
        options: int,
        value: typing.Any,
    ) -> typing.Any:
        val_com = getattr(value, "_com_obj", value) if value else None
        self._property_object.SetPropertyObject(lookup_string, options, val_com)

    @ts_interface
    def set_property_object_by_offset(
        self,
        array_offset: int,
        options: int,
        value: typing.Any,
    ) -> typing.Any:
        val_com = getattr(value, "_com_obj", value) if value else None
        self._property_object.SetPropertyObjectByOffset(array_offset, options, val_com)

    @ts_interface
    def is_alias_object(self, lookup_string: str = "", options: int = 0) -> typing.Any:
        return bool(self._property_object.IsAliasObject(lookup_string, options))

    @ts_interface
    def is_equal_to(self, object_to_compare: typing.Any, options: int = 0) -> bool:
        obj_com = getattr(object_to_compare, "_com_obj", object_to_compare)
        return bool(self._property_object.IsEqualTo(obj_com, options))

    @ts_interface
    def get_xml(
        self,
        generation_options: XMLOption | int = 0,
        initial_indentation: int = 0,
        default_name: str = "",
        format_string: str = "",
    ) -> tuple[str, typing.Any, typing.Any]:
        result = self._property_object.GetXML(
            int(generation_options),
            int(initial_indentation),
            default_name,
            format_string,
        )
        if isinstance(result, tuple):
            xml_string = str(result[0]) if len(result) > 0 else ""
            conflict_objects = list(result[1]) if len(result) > 1 and result[1] else []
            conflict_strings = list(result[2]) if len(result) > 2 and result[2] else []
            return (xml_string, conflict_objects, conflict_strings)
        return (str(result), [], [])

    @ts_interface
    def set_xml(
        self,
        xml_string: str,
        options: int = 0,
        initial_indentation: int = 0,
    ) -> typing.Any:
        self._property_object.SetXML(str(xml_string), int(options), int(initial_indentation))

    @ts_interface
    def contains_type_instance(
        self,
        lookup_string: str = "",
        options: int = 0,
        type_name: str = "",
    ) -> bool:
        return bool(self._property_object.ContainsTypeInstance(lookup_string, options, type_name))

    @ts_interface
    def get_array_index(
        self,
        lookup_string: str = "",
        options: int = 0,
        array_offset: int = 0,
    ) -> str:
        return str(self._property_object.GetArrayIndex(lookup_string, options, array_offset))

    @ts_interface
    def get_array_offset(
        self,
        lookup_string: str = "",
        options: int = 0,
        array_index: str = "",
    ) -> int:
        return int(self._property_object.GetArrayOffset(lookup_string, options, array_index))

    @ts_interface
    def get_sub_property_index(
        self,
        lookup_string: str,
        options: int,
        prop_name: str,
    ) -> typing.Any:
        return int(self._property_object.GetSubPropertyIndex(lookup_string, options, prop_name))

    @ts_interface
    def get_structure_change_count(self, lookup_string: str = "", options: int = 0) -> typing.Any:
        return int(self._property_object.GetStructureChangeCount(lookup_string, options))

    @ts_interface
    def set_nth_sub_property_name(
        self,
        lookup_string: str = "",
        index: int = 0,
        options: int = 0,
        new_value: str = "",
    ) -> None:
        self._property_object.SetNthSubPropertyName(lookup_string, index, options, new_value)

    @ts_interface
    def get_location(self, top_object: typing.Any = None) -> typing.Any:
        top_com = getattr(top_object, "_com_obj", top_object) if top_object else None
        return str(self._property_object.GetLocation(top_com))

    @ts_interface
    def get_instance_default_flags(self, lookup_string: str = "", options: int = 0) -> typing.Any:
        return int(self._property_object.GetInstanceDefaultFlags(lookup_string, options))

    @ts_interface
    def set_instance_default_flags(
        self,
        lookup_string: str = "",
        options: int = 0,
        flags: int = 0,
    ) -> None:
        self._property_object.SetInstanceDefaultFlags(lookup_string, options, flags)

    @ts_interface
    def get_instance_override_flags(self, lookup_string: str = "", options: int = 0) -> typing.Any:
        return int(self._property_object.GetInstanceOverrideFlags(lookup_string, options))

    @ts_interface
    def set_instance_override_flags(
        self,
        lookup_string: str = "",
        options: int = 0,
        flags: int = 0,
    ) -> None:
        self._property_object.SetInstanceOverrideFlags(lookup_string, options, flags)

    @ts_interface
    def lock_type_definition(self) -> None:
        self._property_object.LockTypeDefinition()

    @ts_interface
    def unlock_type_definition(self, password_string: str) -> None:
        self._property_object.UnlockTypeDefinition(str(password_string))

    @ts_interface
    def get_type_definition_protection(self) -> int:
        return int(self._property_object.GetTypeDefinitionProtection())

    @ts_interface
    def set_type_definition_protection(
        self,
        new_value: int,
        password_string: str = "",
    ) -> typing.Any:
        self._property_object.SetTypeDefinitionProtection(new_value, password_string)

    @ts_interface
    def clear_type_definition_password_history(self) -> None:
        self._property_object.ClearTypeDefinitionPasswordHistory()

    @ts_interface
    def read(self, path_string: str, object_name: str = "", rw_options: int = 0) -> typing.Any:
        self._property_object.Read(path_string, object_name, rw_options)

    @ts_interface
    def write(self, path_string: str, object_name: str = "", rw_options: int = 0) -> typing.Any:
        self._property_object.Write(path_string, object_name, rw_options)

    @ts_interface
    def read_ex(
        self,
        path_string: str,
        object_name: str = "",
        rw_options: int = 0,
        handler_type: int = 1,
    ) -> None:
        self._property_object.ReadEx(path_string, object_name, rw_options, handler_type)

    @ts_interface
    def serialize(self, stream: str = "", object_name: str = "", rw_options: int = 0) -> typing.Any:
        return str(self._property_object.Serialize(stream, object_name, rw_options))

    @ts_interface
    def unserialize(self, stream: str, rw_options: int = 0) -> typing.Any:
        self._property_object.Unserialize(stream, rw_options)

    @ts_interface
    def get_property_object_elements(
        self,
        lookup_string: str,
        options: int = 0,
    ) -> list[PropertyObject]:
        elements_com = self._property_object.GetPropertyObjectElements(lookup_string, options)
        return [PropertyObject(el, self._engine_ref) for el in elements_com]

    @ts_interface
    def create_report_section(
        self,
        generation_options: int = 0,
        initial_indentation: int = 0,
        default_name: str = "",
        format_string: str = "",
        format: str = "",
    ) -> ReportSection | None:
        from py_teststand.execution.report import ReportSection

        com_obj = self._property_object.CreateReportSection(
            generation_options,
            initial_indentation,
            default_name,
            format_string,
            format,
        )
        return ReportSection(com_obj, self._engine_ref) if com_obj else None

    @ts_interface
    def set_val_idispatch(
        self,
        lookup_string: str = "",
        options: int = 0,
        value: typing.Any = None,
    ) -> None:
        val_com = getattr(value, "_com_obj", value) if value else None
        self._property_object.SetValIDispatch(lookup_string, options, val_com)

    @ts_interface
    def set_val_idispatch_by_offset(
        self,
        array_offset: int = 0,
        options: int = 0,
        value: typing.Any = None,
    ) -> None:
        val_com = getattr(value, "_com_obj", value) if value else None
        self._property_object.SetValIDispatchByOffset(array_offset, options, val_com)

    @ts_interface
    def set_val_integer64_by_offset(
        self,
        array_offset: int = 0,
        options: int = 0,
        value: int = 0,
    ) -> None:
        self._property_object.SetValInteger64ByOffset(array_offset, options, value)

    @ts_interface
    def set_val_interface_by_offset(
        self,
        array_offset: int = 0,
        options: int = 0,
        value: typing.Any = None,
    ) -> None:
        val_com = getattr(value, "_com_obj", value) if value else None
        self._property_object.SetValInterfaceByOffset(array_offset, options, val_com)

    @ts_interface
    def set_val_unsigned_integer64_by_offset(
        self,
        array_offset: int = 0,
        options: int = 0,
        value: int = 0,
    ) -> None:
        self._property_object.SetValUnsignedInteger64ByOffset(array_offset, options, value)

    @ts_interface
    def display_array_bounds_dialog(self, dlg_title: str = "", dlg_options: int = 0) -> bool:
        return bool(self._com_obj.DisplayArrayBoundsDialog(dlg_title, int(dlg_options)))

    @ts_interface
    def display_attributes_dialog(
        self,
        dlg_title: str = "",
        file: typing.Any = None,
        dlg_options: int = 0,
    ) -> bool:
        file_com = getattr(file, "_com_obj", file) if file is not None else None
        return bool(self._com_obj.DisplayAttributesDialog(dlg_title, file_com, int(dlg_options)))

    @ts_interface
    def display_edit_numeric_format_dialog(
        self,
        dlg_title: str,
        dlg_options: int = 0,
    ) -> tuple[bool, str]:
        res = self._com_obj.DisplayEditNumericFormatDialog(dlg_title, "", int(dlg_options))
        if isinstance(res, tuple) and len(res) >= 2:
            return bool(res[0]), str(res[1])
        return bool(res), ""

    @ts_interface
    def display_flags_dialog(self, dlg_title: str = "", dlg_options: int = 0) -> int:
        return int(self._com_obj.DisplayFlagsDialog(dlg_title, int(dlg_options)))

    @ts_interface
    def display_properties_dialog(
        self,
        dlg_title: str = "",
        file: typing.Any = None,
        dlg_options: int = 0,
    ) -> int:
        file_com = getattr(file, "_com_obj", file) if file is not None else None
        return int(self._com_obj.DisplayPropertiesDialog(dlg_title, file_com, int(dlg_options)))

    @ts_interface
    def enum_is_valid(self) -> bool:
        return bool(self._com_obj.EnumIsValid())

    @ts_interface
    def get_display_names(self, lookup_string: str = "", options: int = 0) -> tuple[str, str]:
        res = self._com_obj.GetDisplayNames(lookup_string, int(options), "", "")
        if isinstance(res, tuple) and len(res) >= 2:
            return str(res[0]), str(res[1])
        return "", ""

    @ts_interface
    def get_sub_properties(self, lookup_string: str = "", options: int = 0) -> list[PropertyObject]:
        elements = self._com_obj.GetSubProperties(lookup_string, int(options))
        return [PropertyObject(el, self._engine_ref) for el in elements]

    @ts_interface
    def get_value_display_name(self, lookup_string: str = "", options: int = 0) -> str:
        return str(self._com_obj.GetValueDisplayName(lookup_string, int(options)))

    @ts_interface
    def set_type_flags(self, lookup_string: str, options: int, flags: PropertyFlag | int) -> None:
        self._com_obj.SetTypeFlags(lookup_string, int(options), int(flags))

    @ts_interface
    def unserialize_ex(
        self,
        stream: str,
        object_name: str = "",
        rw_options: int = 0,
        handler_type: int = 1,
    ) -> None:
        self._com_obj.UnserializeEx(stream, object_name, int(rw_options), int(handler_type))

    @ts_interface
    def update_enumerators(self, new_values: PropertyObject) -> bool:
        return bool(self._com_obj.UpdateEnumerators(new_values._com_obj))

    @ts_interface
    def validate_new_element_name(
        self,
        new_name: str,
        allow_duplicates: bool = False,
    ) -> tuple[bool, str]:
        res = self._com_obj.ValidateNewElementName(new_name, bool(allow_duplicates))
        if isinstance(res, tuple) and len(res) >= 2:
            return bool(res[1]), str(res[0])
        return bool(res), ""

    @property
    @ts_interface
    def array_element_prototype(self) -> PropertyObject | None:
        com = self._com_obj.ArrayElementPrototype
        return PropertyObject(com, self._engine_ref) if com else None

    @array_element_prototype.setter
    @ts_interface
    def array_element_prototype(self, value: PropertyObject) -> None:
        self._com_obj.ArrayElementPrototype = value._com_obj

    @property
    @ts_interface
    def enumerators(self) -> PropertyObject | None:
        com = self._com_obj.Enumerators
        return PropertyObject(com, self._engine_ref) if com else None

    @property
    @ts_interface
    def has_attributes(self) -> bool:
        return bool(self._com_obj.HasAttributes)

    @property
    @ts_interface
    def has_type_attributes(self) -> bool:
        return bool(self._com_obj.HasTypeAttributes)

    @property
    @ts_interface
    def parent(self) -> PropertyObject | None:
        com = self._com_obj.Parent
        return PropertyObject(com, self._engine_ref) if com else None

    @property
    @ts_interface
    def type_attributes(self) -> PropertyObject | None:
        com = self._com_obj.TypeAttributes
        return PropertyObject(com, self._engine_ref) if com else None

    @property
    @ts_interface
    def type_category(self) -> int:
        return int(self._com_obj.TypeCategory)

    @property
    @ts_interface
    def type_definition_locked(self) -> bool:
        return bool(self._com_obj.TypeDefinitionLocked)

    @type_version.setter
    @ts_interface
    def type_version(self, value: str) -> None:
        self._com_obj.TypeVersion = str(value)
