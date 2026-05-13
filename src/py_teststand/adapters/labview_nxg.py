from __future__ import annotations

import typing
from enum import IntEnum, IntFlag

from py_teststand.adapters.adapter import Adapter, Module
from py_teststand.core.com_wrapper import ts_interface
from py_teststand.property.property_object import PropertyObject
from py_teststand.sequence.expression import EvaluationTypes


class LabVIEWNXGServer(IntEnum):
    ExecServer = 0
    RTEServer = 1


class LabVIEWNXGComponentBuildOutput(IntEnum):
    GLibrary = 0x0
    Source = 0x1
    Executable = 0x2


class LabVIEWNXGNodeOperationMode(IntEnum):
    Default = 0
    Restricted = 1


class LabVIEWNXGParameterDirection(IntEnum):
    In = 0
    Out = 1


class LabVIEWNXGParameterWireRequirement(IntEnum):
    Required = 0
    Recommended = 1
    Optional = 2


class LabVIEWNXGProjectItemType(IntEnum):
    Component = 0x0
    VirtualInstrument = 0x1


class LabVIEWNXGModuleCallOption(IntFlag):
    def __str__(self) -> str:
        return str(self.value)

    BringFrontPaneltoFront = 8
    MakeFrontPanelModal = 4
    NoneValue = 0
    ReserveforExecution = 1
    RunInRuntimeEngine = 2


class LabVIEWNXGNodePropertyDirections(IntEnum):
    def __str__(self) -> str:
        return str(self.value)

    Default = 2
    In = 0
    Out = 1


class LabVIEWNXGParameterCategory(IntEnum):
    def __str__(self) -> str:
        return str(self.value)

    Boolean = 2
    BooleanArray = 52
    Cluster = 3
    ClusterArray = 53
    Complex = 6
    ComplexArray = 55
    Enum = 9
    EnumArray = 58
    Numeric = 0
    NumericArray = 50
    Reference = 4
    ReferenceArray = 54
    String = 1
    StringArray = 51
    Unknown = 8
    Variant = 7
    VariantArray = 56


class LabVIEWNXGParameterType(IntEnum):
    def __str__(self) -> str:
        return str(self.value)

    ActiveXRef = 64
    AnalogWaveform = 23
    DigitalTable = 22
    DigitalWaveform = 24
    ErrorOut = 37
    Ext = 8
    Int16 = 2
    Int32 = 4
    Int64 = 12
    Int8 = 0
    IO = 21
    LVNXGObjectRef = 66
    OtherRef = 67
    PathString = 98
    Real32 = 6
    Real64 = 7
    StandardCluster = 20
    String = 96
    TimestampString = 99
    UInt16 = 3
    UInt32 = 5
    UInt64 = 13
    UInt8 = 1
    Unspecified = 200


class LabVIEWNXGAdapter(Adapter):
    @ts_interface
    def as_adapter(self) -> Adapter:
        return Adapter(self._com_obj.AsAdapter(), self._engine_ref)

    @property
    @ts_interface
    def auto_build_component_output(self) -> typing.Any:
        return bool(self._com_obj.AutoBuildComponentOutput)

    @auto_build_component_output.setter
    @ts_interface
    def auto_build_component_output(self, value: bool) -> None:
        self._com_obj.AutoBuildComponentOutput = bool(value)

    @property
    @ts_interface
    def current_server_version(self) -> str:
        return str(self._com_obj.CurrentServerVersion)

    @ts_interface
    def get_classes_for_node_library(self, type_name: str) -> typing.Any:
        res = self._com_obj.GetClassesForNodeLibrary(type_name, None, None)
        if isinstance(res, tuple) and len(res) >= 3:
            return list(res[1]), list(res[2])
        return [], []

    @ts_interface
    def get_cluster_member_is_binary_string(
        self, type_definition: typing.Any, property_lookup_string: str
    ) -> bool:
        com_po = getattr(type_definition, "_com_obj", type_definition)
        return bool(self._com_obj.GetClusterMemberIsBinaryString(com_po, property_lookup_string))

    @ts_interface
    def get_cluster_member_label(
        self, type_definition: typing.Any, property_lookup_string: str
    ) -> typing.Any:
        com_po = getattr(type_definition, "_com_obj", type_definition)
        return str(self._com_obj.GetClusterMemberLabel(com_po, property_lookup_string))

    @ts_interface
    def get_cluster_passing_enabled(self, type_definition: typing.Any) -> typing.Any:
        com_po = getattr(type_definition, "_com_obj", type_definition)
        return bool(self._com_obj.GetClusterPassingEnabled(com_po))

    @ts_interface
    def get_exclude_from_cluster(
        self, type_definition: typing.Any, property_lookup_string: str
    ) -> typing.Any:
        com_po = getattr(type_definition, "_com_obj", type_definition)
        return bool(self._com_obj.GetExcludeFromCluster(com_po, property_lookup_string))

    @ts_interface
    def get_items_in_gll(self, gll_absolute_path: str) -> typing.Any:
        return list(self._com_obj.GetItemsInGLL(gll_absolute_path))

    @ts_interface
    def get_node_libraries(self) -> typing.Any:
        res = self._com_obj.GetNodeLibraries(None, None)
        if isinstance(res, tuple) and len(res) >= 2:
            return list(res[0]), list(res[1])
        return [], []

    @ts_interface
    def get_properties_for_node_class(
        self, type_name: str, class_name: str, options: int = 0
    ) -> tuple[list[str], list[str], list[str], list[str], list[str]]:
        res = self._com_obj.GetPropertiesForNodeClass(
            type_name, class_name, None, None, None, None, None, options
        )
        if isinstance(res, tuple) and len(res) >= 7:
            return list(res[2]), list(res[3]), list(res[4]), list(res[5]), list(res[6])
        return [], [], [], [], []

    @ts_interface
    def get_vi_version(self, project_or_gll_absolute_path: str, qualified_name: str) -> typing.Any:
        return str(self._com_obj.GetVIVersion(project_or_gll_absolute_path, qualified_name))

    @ts_interface
    def initialize(self) -> None:
        self._com_obj.Initialize()

    @ts_interface
    def is_activex_server_connection_valid(self) -> bool:
        return bool(self._com_obj.IsActiveXServerConnectionValid)

    @property
    @ts_interface
    def is_current_server_an_editor(self) -> bool:
        return bool(self._com_obj.IsCurrentServerAnEditor)

    @ts_interface
    def is_labview_nxg_installed(self) -> tuple[bool, str, str, str]:
        res = self._com_obj.IsLabVIEWNXGInstalled("", "", "")
        if isinstance(res, tuple) and len(res) >= 4:
            return bool(res[0]), str(res[1]), str(res[2]), str(res[3])
        return bool(res), "", "", ""

    @ts_interface
    def new_module(self) -> typing.Any:

        return LabVIEWNXGModule(self._com_obj.NewModule(), self._engine_ref)

    @property
    @ts_interface
    def server_info(self) -> typing.Any:

        return LabVIEWNXGServer(self._com_obj.ServerInfo)

    @ts_interface
    def set_cluster_member_is_binary_string(
        self, type_definition: typing.Any, property_lookup_string: str, val: bool
    ) -> None:
        com_po = getattr(type_definition, "_com_obj", type_definition)
        self._com_obj.SetClusterMemberIsBinaryString(com_po, property_lookup_string, val)

    @ts_interface
    def set_cluster_member_label(
        self, type_definition: typing.Any, property_lookup_string: str, label: str
    ) -> None:
        com_po = getattr(type_definition, "_com_obj", type_definition)
        self._com_obj.SetClusterMemberLabel(com_po, property_lookup_string, label)

    @ts_interface
    def set_cluster_passing_enabled(self, type_definition: typing.Any, val: bool) -> typing.Any:
        com_po = getattr(type_definition, "_com_obj", type_definition)
        self._com_obj.SetClusterPassingEnabled(com_po, val)

    @ts_interface
    def set_exclude_from_cluster(
        self, type_definition: typing.Any, property_lookup_string: str, val: bool
    ) -> None:
        com_po = getattr(type_definition, "_com_obj", type_definition)
        self._com_obj.SetExcludeFromCluster(com_po, property_lookup_string, val)

    @property
    @ts_interface
    def validate_gll_path(self) -> bool:
        return bool(self._com_obj.ValidateGLLPath)

    @validate_gll_path.setter
    @ts_interface
    def validate_gll_path(self, value: bool) -> None:
        self._com_obj.ValidateGLLPath = bool(value)


class LabVIEWNXGModule(Module):
    @ts_interface
    def as_module(self) -> typing.Any:
        from py_teststand.adapters import Module

        return Module(self._com_obj.AsModule(), self._engine_ref)

    @ts_interface
    def build_component(self, output_type: LabVIEWNXGComponentBuildOutput | int) -> bool:
        return bool(self._com_obj.BuildComponent(int(output_type)))

    @property
    @ts_interface
    def component_name(self) -> typing.Any:
        return str(self._com_obj.ComponentName)

    @component_name.setter
    @ts_interface
    def component_name(self, value: str) -> None:
        self._com_obj.ComponentName = str(value)

    @ts_interface
    def create_project(self, project_path: str) -> bool:
        return bool(self._com_obj.CreateProject(project_path))

    @ts_interface
    def create_property_node_vi(self) -> bool:
        return bool(self._com_obj.CreatePropertyNodeVI())

    @ts_interface
    def edit_project(self) -> bool:
        return bool(self._com_obj.EditProject())

    @ts_interface
    def execute(self, sequence_context: typing.Any, arguments: typing.Any) -> typing.Any:
        com_ctx = getattr(sequence_context, "_com_obj", sequence_context)
        com_args = getattr(arguments, "_com_obj", arguments)
        self._com_obj.Execute(com_ctx, com_args)

    @ts_interface
    def get_project_reference(self) -> typing.Any:

        return LabVIEWNXGProject(self._com_obj.GetProjectReference(), self._engine_ref)

    @ts_interface
    def get_vi_absolute_path(self) -> typing.Any:
        result = self._com_obj.GetVIAbsolutePath("")
        if isinstance(result, tuple):
            return result
        return (bool(result), "")

    @property
    @ts_interface
    def gll_path(self) -> str:
        return str(self._com_obj.GLLPath)

    @gll_path.setter
    @ts_interface
    def gll_path(self, value: str) -> None:
        self._com_obj.GLLPath = str(value)

    @ts_interface
    def have_properties_changed(self, options: int = 0) -> typing.Any:
        result = self._com_obj.HavePropertiesChanged(None, int(options))
        if isinstance(result, tuple) and len(result) >= 2:
            return bool(result[0]), list(result[1])
        return bool(result), []

    @ts_interface
    def is_project_valid(self) -> typing.Any:
        result = self._com_obj.IsProjectValid("")
        if isinstance(result, tuple):
            return result
        return (bool(result), "")

    @ts_interface
    def load_vi_info(self) -> bool:
        return bool(self._com_obj.LoadVIInfo())

    @property
    @ts_interface
    def module_qualified_name(self) -> str:
        return str(self._com_obj.ModuleQualifiedName)

    @module_qualified_name.setter
    @ts_interface
    def module_qualified_name(self, value: str) -> None:
        self._com_obj.ModuleQualifiedName = str(value)

    @property
    @ts_interface
    def node_class_name(self) -> str:
        return str(self._com_obj.NodeClassName)

    @node_class_name.setter
    @ts_interface
    def node_class_name(self, value: str) -> None:
        self._com_obj.NodeClassName = str(value)

    @property
    @ts_interface
    def project_path(self) -> typing.Any:
        return str(self._com_obj.ProjectPath)

    @project_path.setter
    @ts_interface
    def project_path(self, value: str) -> None:
        self._com_obj.ProjectPath = str(value)

    @property
    @ts_interface
    def qualified_name(self) -> str:
        return str(self._com_obj.QualifiedName)

    @qualified_name.setter
    @ts_interface
    def qualified_name(self, value: str) -> None:
        self._com_obj.QualifiedName = str(value)

    @ts_interface
    def update_module_from_step(self, old_step: typing.Any, options: int = 0) -> typing.Any:
        com_step = getattr(old_step, "_com_obj", old_step)
        res = self._com_obj.UpdateModuleFromStep(com_step, int(options), None)
        if isinstance(res, tuple) and len(res) >= 3:
            return list(res[2])
        return []

    @property
    @ts_interface
    def vi_call_options(self) -> int:
        return int(self._com_obj.VICallOptions)

    @vi_call_options.setter
    @ts_interface
    def vi_call_options(self, value: int) -> None:
        self._com_obj.VICallOptions = int(value)

    @property
    @ts_interface
    def vi_description(self) -> str:
        return str(self._com_obj.VIDescription)

    @vi_description.setter
    @ts_interface
    def vi_description(self, value: str) -> None:
        self._com_obj.VIDescription = str(value)

    @property
    @ts_interface
    def vi_target(self) -> typing.Any:
        return str(self._com_obj.VITarget)

    @vi_target.setter
    @ts_interface
    def vi_target(self, value: str) -> None:
        self._com_obj.VITarget = str(value)


class LabVIEWNXGProject(PropertyObject):
    def __init__(self, com_obj: typing.Any, engine: typing.Any = None) -> None:

        super().__init__(com_obj, engine)

    @ts_interface
    def get_project_items(self) -> LabVIEWNXGProjectItems:
        return LabVIEWNXGProjectItems(self._com_obj.GetProjectItems(), self._engine_ref)

    @property
    @ts_interface
    def name(self) -> str:
        return str(self._com_obj.Name)


class LabVIEWNXGProjectItems(PropertyObject):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index: typing.Any) -> typing.Any:
        return LabVIEWNXGProjectItemObject(self._com_obj.Item(index), self._engine_ref)

    def __len__(self) -> int:

        return self.count

    def __getitem__(self, index: typing.Any) -> LabVIEWNXGProjectItemObject:

        return self.item(index)


class LabVIEWNXGProjectItemObject(PropertyObject):
    @property
    @ts_interface
    def component_name(self) -> str:
        return str(self._com_obj.ComponentName)

    @property
    @ts_interface
    def help_description(self) -> str:
        return str(self._com_obj.HelpDescription)

    @property
    @ts_interface
    def module_qualified_name(self) -> str:
        return str(self._com_obj.ModuleQualifiedName)

    @property
    @ts_interface
    def path(self) -> str:
        return str(self._com_obj.Path)

    @property
    @ts_interface
    def target_name(self) -> typing.Any:
        return str(self._com_obj.TargetName)

    @property
    @ts_interface
    def type(self) -> typing.Any:
        return int(self._com_obj.Type)

    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index: typing.Any) -> LabVIEWNXGArgument:
        return LabVIEWNXGArgument(self._com_obj.Item(index), self._engine_ref)

    def __len__(self) -> int:

        return self.count

    def __getitem__(self, index: typing.Any) -> LabVIEWNXGArgument:

        return self.item(index)


class LabVIEWNXGArgument(PropertyObject):
    @property
    @ts_interface
    def complex_imaginary_part(self) -> LabVIEWNXGArgument:
        return LabVIEWNXGArgument(self._com_obj.ComplexImaginaryPart, self._engine_ref)

    @property
    @ts_interface
    def complex_real_part(self) -> LabVIEWNXGArgument:
        return LabVIEWNXGArgument(self._com_obj.ComplexRealPart, self._engine_ref)

    @property
    @ts_interface
    def elements(self) -> PropertyObject:
        return PropertyObject(self._com_obj.Elements, self._engine_ref)

    @property
    @ts_interface
    def parameter_name(self) -> str:
        return str(self._com_obj.ParameterName)

    @property
    @ts_interface
    def value(self) -> PropertyObject:
        return PropertyObject(self._com_obj.Value, self._engine_ref)

    @value.setter
    @ts_interface
    def value(self, value: PropertyObject | typing.Any) -> None:
        val_com = getattr(value, "_com_obj", value)
        self._com_obj.Value = val_com


class LabVIEWNXGNodeProperties(PropertyObject):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def clear(self) -> None:
        self._com_obj.Clear()

    @ts_interface
    def delete(self, index: typing.Any) -> typing.Any:
        self._com_obj.Delete(index)

    @ts_interface
    def item(self, index: typing.Any) -> typing.Any:
        return LabVIEWNXGNodeProperty(self._com_obj.Item(index), self._engine_ref)

    @ts_interface
    def new(
        self, index: typing.Any, long_name: str, data_name: str, unique_id: str, direction: int
    ) -> None:
        self._com_obj.New(index, long_name, data_name, unique_id, direction)

    def __len__(self) -> int:

        return self.count

    def __getitem__(self, index: typing.Any) -> LabVIEWNXGNodeProperty:

        return self.item(index)


class LabVIEWNXGNodeProperty(PropertyObject):
    @ts_interface
    def as_property_object(self) -> PropertyObject:
        return PropertyObject(self._com_obj.AsPropertyObject(), self._engine_ref)

    @property
    @ts_interface
    def data_name(self) -> str:
        return str(self._com_obj.DataName)

    @property
    @ts_interface
    def direction(self) -> typing.Any:
        return int(self._com_obj.Direction)

    @direction.setter
    @ts_interface
    def direction(self, value: int) -> None:
        self._com_obj.Direction = int(value)

    @property
    @ts_interface
    def long_name(self) -> str:
        return str(self._com_obj.LongName)

    @property
    @ts_interface
    def unique_id(self) -> str:
        return str(self._com_obj.UniqueID)


class LabVIEWNXGParameter(PropertyObject):
    @property
    @ts_interface
    def array_dimensions(self) -> int:
        return int(self._com_obj.ArrayDimensions)

    @property
    @ts_interface
    def array_element_prototype(self) -> LabVIEWNXGParameter:
        return LabVIEWNXGParameter(self._com_obj.ArrayElementPrototype, self._engine_ref)

    @ts_interface
    def as_property_object(self) -> PropertyObject:
        return PropertyObject(self._com_obj.AsPropertyObject(), self._engine_ref)

    @property
    @ts_interface
    def category(self) -> typing.Any:
        return int(self._com_obj.Category)

    @property
    @ts_interface
    def complex_imaginary_part_element(self) -> LabVIEWNXGParameter:
        return LabVIEWNXGParameter(self._com_obj.ComplexImaginaryPartElement, self._engine_ref)

    @property
    @ts_interface
    def complex_real_part_element(self) -> LabVIEWNXGParameter:
        return LabVIEWNXGParameter(self._com_obj.ComplexRealPartElement, self._engine_ref)

    @ts_interface
    def create_default_array_elements(self) -> bool:
        return bool(self._com_obj.CreateDefaultArrayElements())

    @property
    @ts_interface
    def default_value(self) -> str:
        return str(self._com_obj.DefaultValue)

    @ts_interface
    def delete_array_element(self, index: int) -> typing.Any:
        self._com_obj.DeleteArrayElement(int(index))

    @ts_interface
    def delete_array_elements(self) -> bool:
        return bool(self._com_obj.DeleteArrayElements())

    @property
    @ts_interface
    def description(self) -> str:
        return str(self._com_obj.Description)

    @property
    @ts_interface
    def direction(self) -> typing.Any:
        return int(self._com_obj.Direction)

    @ts_interface
    def display_create_custom_data_type_dialog(self, sequence_context: typing.Any) -> typing.Any:
        raw_ctx = getattr(sequence_context, "_com_obj", sequence_context)
        return bool(self._com_obj.DisplayCreateCustomDataTypeDialog(raw_ctx))

    @property
    @ts_interface
    def display_type(self) -> str:
        return str(self._com_obj.DisplayType)

    @property
    @ts_interface
    def elements(self) -> typing.Any:

        return LabVIEWNXGParameters(self._com_obj.Elements, self._engine_ref)

    @ts_interface
    def expr_cluster_type_mismatch(self, sequence_context: typing.Any) -> typing.Any:
        raw_ctx = getattr(sequence_context, "_com_obj", sequence_context)
        return bool(self._com_obj.ExprClusterTypeMismatch(raw_ctx))

    @property
    @ts_interface
    def get_array_element_index(self) -> str:
        return str(self._com_obj.GetArrayElementIndex)

    @ts_interface
    def get_nxg_array_index(self, offset: int) -> typing.Any:
        return str(self._com_obj.GetArrayIndex(int(offset)))

    @ts_interface
    def get_default_array_dimension_size(self, dimension: int) -> typing.Any:
        return int(self._com_obj.GetDefaultArrayDimensionSize(int(dimension)))

    @ts_interface
    def get_enum_values(self) -> list[typing.Any]:
        return list(self._com_obj.GetEnumValues())

    @ts_interface
    def insert_array_element(self, index: int) -> typing.Any:
        self._com_obj.InsertArrayElement(int(index))

    @ts_interface
    def is_cluster_mapping_invalid(self) -> typing.Any:
        result = self._com_obj.IsClusterMappingInvalid("")
        if isinstance(result, tuple):
            return result
        return (bool(result), "")

    @ts_interface
    def is_parameter_mapping_valid(self) -> typing.Any:
        result = self._com_obj.IsParameterMappingValid("")
        if isinstance(result, tuple):
            return result
        return (bool(result), "")

    @property
    @ts_interface
    def node_uses_default_value(self) -> bool:
        return bool(self._com_obj.NodeUsesDefaultValue)

    @property
    @ts_interface
    def parameter_name(self) -> str:
        return str(self._com_obj.ParameterName)

    @property
    @ts_interface
    def partially_specified(self) -> bool:
        return bool(self._com_obj.PartiallySpecified)

    @property
    @ts_interface
    def pass_as_binary_string(self) -> bool:
        return bool(self._com_obj.PassAsBinaryString)

    @pass_as_binary_string.setter
    @ts_interface
    def pass_as_binary_string(self, value: bool) -> None:
        self._com_obj.PassAsBinaryString = bool(value)

    @property
    @ts_interface
    def type(self) -> int:
        return int(self._com_obj.Type)

    @property
    @ts_interface
    def type_display_string(self) -> str:
        return str(self._com_obj.TypeDisplayString)

    @ts_interface
    def update_cluster_mapping(self, sequence_context: typing.Any) -> typing.Any:
        raw_ctx = getattr(sequence_context, "_com_obj", sequence_context)
        return bool(self._com_obj.UpdateClusterMapping(raw_ctx))

    @property
    @ts_interface
    def use_default_value(self) -> bool:
        return bool(self._com_obj.UseDefaultValue)

    @use_default_value.setter
    @ts_interface
    def use_default_value(self, value: bool) -> None:
        self._com_obj.UseDefaultValue = bool(value)

    @property
    @ts_interface
    def user_data(self) -> PropertyObject:
        return PropertyObject(self._com_obj.UserData, self._engine_ref)

    @user_data.setter
    @ts_interface
    def user_data(self, value: PropertyObject | typing.Any) -> None:
        val_com = getattr(value, "_com_obj", value)
        self._com_obj.UserData = val_com

    @property
    @ts_interface
    def valid_evaluation_types(self) -> EvaluationTypes:
        from py_teststand.sequence.expression import EvaluationTypes

        return EvaluationTypes(self._com_obj.ValidEvaluationTypes, self._engine_ref)

    @property
    @ts_interface
    def value_expr(self) -> str:
        return str(self._com_obj.ValueExpr)

    @value_expr.setter
    @ts_interface
    def value_expr(self, value: str) -> None:
        self._com_obj.ValueExpr = str(value)

    @property
    @ts_interface
    def value_expr_is_ignored(self) -> bool:
        return bool(self._com_obj.ValueExprIsIgnored)

    @value_expr_is_ignored.setter
    @ts_interface
    def value_expr_is_ignored(self, value: bool) -> None:
        self._com_obj.ValueExprIsIgnored = bool(value)

    @property
    @ts_interface
    def value_expr_is_optional(self) -> bool:
        return bool(self._com_obj.ValueExprIsOptional)

    @property
    @ts_interface
    def wire_requirement(self) -> typing.Any:
        return int(self._com_obj.WireRequirement)


class LabVIEWNXGParameters(PropertyObject):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index: typing.Any) -> typing.Any:
        return LabVIEWNXGParameter(self._com_obj.Item(index), self._engine_ref)

    def __len__(self) -> int:

        return self.count

    def __getitem__(self, index: typing.Any) -> LabVIEWNXGParameter:

        return self.item(index)

    @ts_interface
    def new_arguments(self) -> typing.Any:

        return PropertyObject(self._com_obj.NewArguments(), self._engine_ref)
