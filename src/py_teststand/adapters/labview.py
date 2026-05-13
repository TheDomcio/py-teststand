from __future__ import annotations

import typing
from enum import IntEnum, IntFlag

from py_teststand.adapters.adapter import Adapter, AdapterCodeTemplatePolicy, Module
from py_teststand.core.com_wrapper import ts_interface
from py_teststand.property.property_object import PropertyObject
from py_teststand.sequence.expression import EvaluationTypes


class LabVIEWCallType(IntEnum):
    VICall = 0
    ClassMemberCall = 1
    PropertyNodeCall = 2


class LabVIEWDevelopmentEnvironmentBitness(IntEnum):
    Default = 0
    Bit32 = 1
    Bit64 = 2


class LabVIEWModuleCallOption(IntFlag):
    ShowFrontPanel = 0x1
    AutoDetectLVRT = 0x2


class LabVIEWModuleOverrideType(IntEnum):
    Default = 0
    PPL = 1


class LabVIEWNodeOperationMode(IntEnum):
    Default = 0
    Restricted = 1


class LabVIEWNodePropertyDirection(IntEnum):
    def __str__(self) -> str:
        return str(self.value)

    In = 0
    Out = 1
    Default = 2


class LabVIEWProjectPath(IntEnum):
    Local = 0
    Remote = 1


class LabVIEWPropertyOption(IntFlag):
    Read = 0x1
    Write = 0x2
    Default = 0x4


class LabVIEWServer(IntEnum):
    ExecServer = 0x0
    RTEServer = 0x1


class LabVIEWVI(IntEnum):
    Standard = 0
    Express = 1


class LabVIEWParameterCategory(IntEnum):
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
    Ring = 10
    RingArray = 59
    String = 1
    StringArray = 51
    Unknown = 8
    Variant = 7
    VariantArray = 56


class LabVIEWParameterDirection(IntEnum):
    def __str__(self) -> str:
        return str(self.value)

    In = 0
    Out = 1


class LabVIEWParameterType(IntEnum):
    def __str__(self) -> str:
        return str(self.value)

    ActiveXRef = 64
    AnalogWaveform = 23
    Complex128 = 10
    Complex64 = 9
    ComplexExt = 11
    DigitalData = 22
    DigitalWaveform = 24
    DotNetRef = 65
    DynamicData = 25
    EnumUInt16 = 15
    EnumUInt32 = 16
    EnumUInt8 = 14
    ErrorOut = 34
    Ext = 8
    Int16 = 2
    Int32 = 4
    Int64 = 12
    Int8 = 0
    IO = 21
    LVClass = 68
    LVObjectRef = 66
    OtherRef = 67
    PathString = 98
    Real32 = 6
    Real64 = 7
    StandardCluster = 20
    String = 96
    TestData = 33
    TimestampString = 99
    UInt16 = 3
    UInt32 = 5
    UInt64 = 13
    UInt8 = 1
    Unspecified = 200


class LabVIEWParameterWireRequirement(IntEnum):
    def __str__(self) -> str:
        return str(self.value)

    Optional = 2
    Recommended = 1
    Required = 0


class LabVIEWAdapter(Adapter):
    @property
    @ts_interface
    def code_template_policy(self) -> AdapterCodeTemplatePolicy:
        return AdapterCodeTemplatePolicy(self._com_obj.CodeTemplatePolicy)

    @code_template_policy.setter
    @ts_interface
    def code_template_policy(self, value: AdapterCodeTemplatePolicy | int) -> None:
        self._com_obj.CodeTemplatePolicy = int(value)

    @property
    @ts_interface
    def current_labview_server_version(self) -> str:
        return str(self._com_obj.CurrentLabVIEWServerVersion)

    @property
    @ts_interface
    def labview_development_environment_bitness(self) -> LabVIEWDevelopmentEnvironmentBitness:
        return LabVIEWDevelopmentEnvironmentBitness(
            self._com_obj.LabVIEWDevelopmentEnvironmentBitness
        )

    @property
    @ts_interface
    def reserve_loaded_vis_for_exec(self) -> bool:
        return bool(self._com_obj.ReserveLoadedVIsForExec)

    @reserve_loaded_vis_for_exec.setter
    @ts_interface
    def reserve_loaded_vis_for_exec(self, value: bool) -> None:
        self._com_obj.ReserveLoadedVIsForExec = value

    @property
    @ts_interface
    def uut_serial_number_expression(self) -> str:
        return str(self._com_obj.UUTSerialNumberExpression)

    @uut_serial_number_expression.setter
    @ts_interface
    def uut_serial_number_expression(self, value: str) -> None:
        self._com_obj.UUTSerialNumberExpression = value

    @ts_interface
    def get_vi_namespace(self, vi_path: str) -> typing.Any:
        return str(self._com_obj.GetVINamespace(vi_path))

    @ts_interface
    def set_server_info(self, server_name: str, server_port: int) -> typing.Any:
        self._com_obj.SetServerInfo(server_name, server_port)

    @property
    @ts_interface
    def additional_threads_inherit_calling_threads_cpu_affinity(self) -> typing.Any:
        return bool(self._com_obj.AdditionalThreadsInheritCallingThreadsCPUAffinity)

    @additional_threads_inherit_calling_threads_cpu_affinity.setter
    @ts_interface
    def additional_threads_inherit_calling_threads_cpu_affinity(self, value: bool) -> None:
        self._com_obj.AdditionalThreadsInheritCallingThreadsCPUAffinity = bool(value)

    @property
    @ts_interface
    def auto_deploy_shared_variables(self) -> typing.Any:
        return bool(self._com_obj.AutoDeploySharedVariables)

    @auto_deploy_shared_variables.setter
    @ts_interface
    def auto_deploy_shared_variables(self, value: bool) -> None:
        self._com_obj.AutoDeploySharedVariables = bool(value)

    @property
    @ts_interface
    def auto_undeploy_shared_variables(self) -> typing.Any:
        return bool(self._com_obj.AutoUndeploySharedVariables)

    @auto_undeploy_shared_variables.setter
    @ts_interface
    def auto_undeploy_shared_variables(self, value: bool) -> None:
        self._com_obj.AutoUndeploySharedVariables = bool(value)

    @property
    @ts_interface
    def build_and_execute_at_start_of_execution(self) -> bool:
        return bool(self._com_obj.BuildAndExecuteAtStartOfExecution)

    @build_and_execute_at_start_of_execution.setter
    @ts_interface
    def build_and_execute_at_start_of_execution(self, value: bool) -> None:
        self._com_obj.BuildAndExecuteAtStartOfExecution = bool(value)

    @property
    @ts_interface
    def build_ppls_at_start_of_execution(self) -> bool:
        return bool(self._com_obj.BuildPPLsAtStartOfExecution)

    @build_ppls_at_start_of_execution.setter
    @ts_interface
    def build_ppls_at_start_of_execution(self, value: bool) -> None:
        self._com_obj.BuildPPLsAtStartOfExecution = bool(value)

    @ts_interface
    def check_remote_system_status(self, remote_host: str, timeout: float) -> tuple[int, str]:
        result = self._com_obj.CheckRemoteSystemStatus(str(remote_host), int(timeout))
        if isinstance(result, tuple):
            return (int(result[0]), str(result[1]))
        return (int(result), "")

    @ts_interface
    def deploy_project_library(self, library_path: str) -> typing.Any:
        self._com_obj.DeployProjectLibrary(str(library_path))

    @ts_interface
    def display_help_for_node_property(
        self,
        library_name: str,
        generic_type: str,
        class_data_name: str,
        property_data_name: str,
        property_unique_id: str,
    ) -> None:
        self._com_obj.DisplayHelpForNodeProperty(
            str(library_name),
            str(generic_type),
            str(class_data_name),
            str(property_data_name),
            str(property_unique_id),
        )

    @property
    @ts_interface
    def enable_rte_debugging_and_tracing(self) -> typing.Any:
        return bool(self._com_obj.EnableRTEDebuggingAndTracing)

    @enable_rte_debugging_and_tracing.setter
    @ts_interface
    def enable_rte_debugging_and_tracing(self, value: bool) -> None:
        self._com_obj.EnableRTEDebuggingAndTracing = bool(value)

    @property
    @ts_interface
    def enable_version_independent_runtime(self) -> bool:
        return bool(self._com_obj.EnableVersionIndependentRuntime)

    @enable_version_independent_runtime.setter
    @ts_interface
    def enable_version_independent_runtime(self, value: bool) -> None:
        self._com_obj.EnableVersionIndependentRuntime = bool(value)

    @ts_interface
    def file_exists_in_llb(self, llb_path: str, vi_name: str) -> typing.Any:
        return bool(self._com_obj.FileExistsInLLB(str(llb_path), str(vi_name)))

    @ts_interface
    def get_classes_for_node_library(self, library_name: str, generic_type: str) -> typing.Any:
        return list(self._com_obj.GetClassesForNodeLibrary(str(library_name), str(generic_type)))

    @ts_interface
    def get_cluster_member_is_binary_string(
        self, type_name: str, member_name: str, options: int = 0
    ) -> bool:
        return bool(
            self._com_obj.GetClusterMemberIsBinaryString(
                str(type_name), str(member_name), int(options)
            )
        )

    @ts_interface
    def get_cluster_member_label(
        self, type_name: str, member_name: str, options: int = 0
    ) -> typing.Any:
        return str(
            self._com_obj.GetClusterMemberLabel(str(type_name), str(member_name), int(options))
        )

    @ts_interface
    def get_cluster_passing_enabled(self, type_name: str, options: int = 0) -> typing.Any:
        return bool(self._com_obj.GetClusterPassingEnabled(str(type_name), int(options)))

    @ts_interface
    def get_exclude_from_cluster(
        self, type_definition: typing.Any, property_lookup_string: str
    ) -> typing.Any:
        com_po = getattr(type_definition, "_com_obj", type_definition)
        return bool(self._com_obj.GetExcludeFromCluster(com_po, str(property_lookup_string)))

    @ts_interface
    def get_express_vi_menu_structure(self, vi_path: str) -> typing.Any:
        return str(self._com_obj.GetExpressVIMenuStructure(str(vi_path)))

    @ts_interface
    def get_member_names(
        self, library_name: str, generic_type: str, class_data_name: str
    ) -> list[str]:
        return list(
            self._com_obj.GetMemberNames(str(library_name), str(generic_type), str(class_data_name))
        )

    @ts_interface
    def get_node_libraries(self) -> typing.Any:
        return list(self._com_obj.GetNodeLibraries())

    @ts_interface
    def get_properties_for_labview_class(
        self,
        library_name: str,
        generic_type: str,
        project_absolute_path: str,
        class_absolute_path: str,
    ) -> tuple[
        list[str],
        list[str],
        list[str],
        list[str],
        list[str],
        list[str],
        list[str],
        list[str],
    ]:
        result = self._com_obj.GetPropertiesForLabVIEWClass(
            str(library_name),
            str(generic_type),
            str(project_absolute_path),
            str(class_absolute_path),
        )
        return (
            list(result.class_long_name),
            list(result.class_data_name),
            list(result.long_names),
            list(result.short_names),
            list(result.data_names),
            list(result.unique_ids),
            list(result.help_descriptions),
            list(result.options),
        )

    @ts_interface
    def get_properties_for_node_class(
        self, library_name: str, generic_type: str, class_data_name: str
    ) -> list[str]:
        return list(
            self._com_obj.GetPropertiesForNodeClass(
                str(library_name), str(generic_type), str(class_data_name)
            )
        )

    @ts_interface
    def get_server_info(self) -> tuple[int, str]:
        result = self._com_obj.GetServerInfo()
        if isinstance(result, tuple):
            return (int(result[0]), str(result[1]))
        return (int(result), "")

    @ts_interface
    def get_vi_version(self, vi_path: str) -> typing.Any:
        return str(self._com_obj.GetVIVersion(str(vi_path)))

    @ts_interface
    def initialize(self) -> None:
        self._com_obj.Initialize()

    @ts_interface
    def is_build_and_execute_enabled(self, options: int = 0) -> typing.Any:
        result = self._com_obj.IsBuildAndExecuteEnabled(int(options), "")
        if isinstance(result, tuple):
            return result
        return (bool(result), "")

    @property
    @ts_interface
    def is_current_labview_server_an_editor(self) -> bool:
        return bool(self._com_obj.IsCurrentLabVIEWServerAnEditor)

    @ts_interface
    def is_express_vi(self, vi_path: str) -> typing.Any:
        return bool(self._com_obj.IsExpressVI(str(vi_path)))

    @property
    @ts_interface
    def is_labview_activex_server_connection_valid(self) -> bool:
        return bool(self._com_obj.IsLabVIEWActiveXServerConnectionValid)

    @ts_interface
    def is_supported_labview_development_system(
        self, version: str, bitness: int, bitness_matching_policy: int
    ) -> bool:
        return bool(
            self._com_obj.IsSupportedLabVIEWDevelopmentSystem(
                str(version), int(bitness), int(bitness_matching_policy)
            )
        )

    @ts_interface
    def new_module(self) -> LabVIEWModule:
        return LabVIEWModule(self._com_obj.NewModule(), self._engine_ref)

    @property
    @ts_interface
    def number_of_threads_used_when_executing_vis_with_rte(self) -> int:
        return int(self._com_obj.NumberOfThreadsUsedWhenExecutingVIsWithRTE)

    @number_of_threads_used_when_executing_vis_with_rte.setter
    @ts_interface
    def number_of_threads_used_when_executing_vis_with_rte(self, value: int) -> None:
        self._com_obj.NumberOfThreadsUsedWhenExecutingVIsWithRTE = int(value)

    @property
    @ts_interface
    def override_module_options(self) -> LabVIEWModuleOverrideType:
        return LabVIEWModuleOverrideType(self._com_obj.OverrideModuleOptions)

    @override_module_options.setter
    @ts_interface
    def override_module_options(self, value: LabVIEWModuleOverrideType | int) -> None:
        self._com_obj.OverrideModuleOptions = int(value)

    @ts_interface
    def set_cluster_member_is_binary_string(
        self, type_definition: typing.Any, property_lookup_string: str, value: bool
    ) -> None:
        com_po = getattr(type_definition, "_com_obj", type_definition)
        self._com_obj.SetClusterMemberIsBinaryString(
            com_po, str(property_lookup_string), bool(value)
        )

    @ts_interface
    def set_cluster_member_label(
        self, type_definition: typing.Any, property_lookup_string: str, label: str
    ) -> None:
        com_po = getattr(type_definition, "_com_obj", type_definition)
        self._com_obj.SetClusterMemberLabel(com_po, str(property_lookup_string), str(label))

    @ts_interface
    def set_cluster_passing_enabled(self, type_definition: typing.Any, value: bool) -> typing.Any:
        com_po = getattr(type_definition, "_com_obj", type_definition)
        self._com_obj.SetClusterPassingEnabled(com_po, bool(value))

    @ts_interface
    def set_exclude_from_cluster(
        self, type_definition: typing.Any, property_lookup_string: str, value: bool
    ) -> None:
        com_po = getattr(type_definition, "_com_obj", type_definition)
        self._com_obj.SetExcludeFromCluster(com_po, str(property_lookup_string), bool(value))

    @property
    @ts_interface
    def use_multiple_threads_when_executing_vis_with_rte(self) -> bool:
        return bool(self._com_obj.UseMultipleThreadsWhenExecutingVIsWithRTE)

    @use_multiple_threads_when_executing_vis_with_rte.setter
    @ts_interface
    def use_multiple_threads_when_executing_vis_with_rte(self, value: bool) -> None:
        self._com_obj.UseMultipleThreadsWhenExecutingVIsWithRTE = bool(value)

    @property
    @ts_interface
    def uut_iteration_number_expression(self) -> str:
        return str(self._com_obj.UUTIterationNumberExpression)

    @uut_iteration_number_expression.setter
    @ts_interface
    def uut_iteration_number_expression(self, value: str) -> None:
        self._com_obj.UUTIterationNumberExpression = str(value)

    @ts_interface
    def clear_build_and_execute_cache(self) -> typing.Any:
        self._com_obj.ClearBuildAndExecuteCache()

    @ts_interface
    def as_adapter(self) -> Adapter:
        return Adapter(self._com_obj.AsAdapter(), self._engine_ref)


class LabVIEWModule(Module):
    @property
    @ts_interface
    def vi_path(self) -> str:
        return str(self._com_obj.VIPath)

    @vi_path.setter
    @ts_interface
    def vi_path(self, value: str) -> None:
        self._com_obj.VIPath = value

    @property
    @ts_interface
    def project_path(self) -> str:
        return str(self._com_obj.ProjectPath)

    @project_path.setter
    @ts_interface
    def project_path(self, value: str) -> None:
        self._com_obj.ProjectPath = value

    @property
    @ts_interface
    def build_specification_name(self) -> str:
        return str(self._com_obj.BuildSpecificationName)

    @build_specification_name.setter
    @ts_interface
    def build_specification_name(self, value: str) -> None:
        self._com_obj.BuildSpecificationName = str(value)

    @property
    @ts_interface
    def call_name(self) -> str:
        return str(self._com_obj.CallName)

    @call_name.setter
    @ts_interface
    def call_name(self, value: str) -> None:
        self._com_obj.CallName = str(value)

    @property
    @ts_interface
    def call_type(self) -> typing.Any:

        return LabVIEWCallType(self._com_obj.CallType)

    @call_type.setter
    @ts_interface
    def call_type(self, value: LabVIEWCallType | int) -> None:
        self._com_obj.CallType = int(value)

    @property
    @ts_interface
    def class_name(self) -> str:
        return str(self._com_obj.ClassName)

    @class_name.setter
    @ts_interface
    def class_name(self, value: str) -> None:
        self._com_obj.ClassName = value

    @property
    @ts_interface
    def class_path(self) -> str:
        return str(self._com_obj.ClassPath)

    @class_path.setter
    @ts_interface
    def class_path(self, value: str) -> None:
        self._com_obj.ClassPath = str(value)

    @ts_interface
    def convert_to_standard_vi(self) -> bool:
        return bool(self._com_obj.ConvertToStandardVI())

    @ts_interface
    def create_project(self, project_path: str) -> bool:
        return bool(self._com_obj.CreateProject(str(project_path)))

    @ts_interface
    def display_parameter_mapping_dialog(self) -> typing.Any:
        return bool(self._com_obj.DisplayParameterMappingDialog())

    @ts_interface
    def display_select_class_from_project_dialog_ex(
        self, reserved: int = 0, property_value: int = 0
    ) -> bool:
        return bool(
            self._com_obj.DisplaySelectClassFromProjectDialogEx(int(reserved), int(property_value))
        )

    @ts_interface
    def display_select_class_from_project_dialog_ex2(
        self, reserved: int = 0, property_value: int = 0, options: int = 0
    ) -> bool:
        return bool(
            self._com_obj.DisplaySelectClassFromProjectDialogEx2(
                int(reserved), int(property_value), int(options)
            )
        )

    @ts_interface
    def display_select_class_member_from_project_dialog_ex(
        self, reserved: int = 0, property_value: int = 0
    ) -> bool:
        return bool(
            self._com_obj.DisplaySelectClassMemberFromProjectDialogEx(
                int(reserved), int(property_value)
            )
        )

    @ts_interface
    def display_select_member_from_class_dialog_ex(
        self, reserved: int = 0, property_value: int = 0
    ) -> bool:
        return bool(
            self._com_obj.DisplaySelectMemberFromClassDialogEx(int(reserved), int(property_value))
        )

    @ts_interface
    def display_select_vi_from_project_dialog_ex(
        self, reserved: int = 0, property_value: int = 0
    ) -> bool:
        return bool(
            self._com_obj.DisplaySelectVIFromProjectDialogEx(int(reserved), int(property_value))
        )

    @ts_interface
    def display_select_vi_from_project_dialog_ex2(
        self, reserved: int = 0, property_value: int = 0, options: int = 0
    ) -> bool:
        return bool(
            self._com_obj.DisplaySelectVIFromProjectDialogEx2(
                int(reserved), int(property_value), int(options)
            )
        )

    @ts_interface
    def edit_class(self) -> None:
        self._com_obj.EditClass()

    @ts_interface
    def edit_project(self) -> None:
        self._com_obj.EditProject()

    @ts_interface
    def execute(self, sequence_context: typing.Any) -> typing.Any:
        com_ctx = getattr(sequence_context, "_com_obj", sequence_context)
        self._com_obj.Execute(com_ctx)

    @ts_interface
    def export_vi(self, vi_path: str) -> None:
        self._com_obj.ExportVI(str(vi_path))

    @ts_interface
    def get_vi_absolute_path(self) -> typing.Any:
        result = self._com_obj.GetVIAbsolutePath("")
        if isinstance(result, tuple):
            return result
        return (bool(result), "")

    @ts_interface
    def get_vi_absolute_path_ex(self, options: int = 0) -> typing.Any:
        result = self._com_obj.GetVIAbsolutePathEx("", int(options))
        if isinstance(result, tuple):
            return result
        return (bool(result), "")

    @property
    @ts_interface
    def help_context(self) -> int:
        return int(self._com_obj.HelpContext)

    @help_context.setter
    @ts_interface
    def help_context(self, value: int) -> None:
        self._com_obj.HelpContext = int(value)

    @property
    @ts_interface
    def help_file_path(self) -> str:
        return str(self._com_obj.HelpFilePath)

    @help_file_path.setter
    @ts_interface
    def help_file_path(self, value: str) -> None:
        self._com_obj.HelpFilePath = str(value)

    @property
    @ts_interface
    def help_picture(self) -> typing.Any:
        return self._com_obj.HelpPicture

    @property
    @ts_interface
    def help_picture_rects(self) -> typing.Any:
        return self._com_obj.HelpPictureRects

    @ts_interface
    def import_vi(self, vi_path: str) -> bool:
        return bool(self._com_obj.ImportVI(str(vi_path)))

    @property
    @ts_interface
    def is_project_valid(self) -> typing.Any:
        return bool(self._com_obj.IsProjectValid)

    @ts_interface
    def load_prototype(self, options: int = 0) -> typing.Any:
        return bool(self._com_obj.LoadPrototype(bool(options)))

    @ts_interface
    def load_prototype_ex(self, discard_parameter_values: bool = False) -> typing.Any:
        return bool(self._com_obj.LoadPrototype(discard_parameter_values))

    @ts_interface
    def get_parameters(self) -> typing.Iterator[typing.Any]:
        from py_teststand.property.property_object import PropertyObject

        params = self._com_obj.Parameters
        count = params.GetNumElements()
        for i in range(count):
            yield PropertyObject(params.GetPropertyObjectByOffset(i), self._engine_ref)

    @ts_interface
    def load_vi_info(self) -> None:
        self._com_obj.LoadVIInfo()

    @ts_interface
    def build_binary(self) -> bool:
        return bool(self._com_obj.BuildBinary())

    @property
    @ts_interface
    def remote_vi_path(self) -> str:
        return str(self._com_obj.RemoteVIPath)

    @remote_vi_path.setter
    @ts_interface
    def remote_vi_path(self, value: str) -> None:
        self._com_obj.RemoteVIPath = str(value)

    @property
    @ts_interface
    def specify_host_by_expression(self) -> bool:
        return bool(self._com_obj.SpecifyHostByExpression)

    @specify_host_by_expression.setter
    @ts_interface
    def specify_host_by_expression(self, value: bool) -> None:
        self._com_obj.SpecifyHostByExpression = bool(value)

    @ts_interface
    def validate_override_settings(self) -> typing.Any:
        return bool(self._com_obj.ValidateOverrideSettings())

    @property
    @ts_interface
    def vi_attached(self) -> bool:
        return bool(self._com_obj.VIAttached)

    @property
    @ts_interface
    def vi_call_options(self) -> LabVIEWModuleCallOption:

        return LabVIEWModuleCallOption(self._com_obj.VICallOptions)

    @vi_call_options.setter
    @ts_interface
    def vi_call_options(self, value: LabVIEWModuleCallOption | int) -> None:
        self._com_obj.VICallOptions = int(value)

    @property
    @ts_interface
    def vi_description(self) -> str:
        return str(self._com_obj.VIDescription)

    @property
    @ts_interface
    def vi_type(self) -> int:
        return int(self._com_obj.VIType)

    @property
    @ts_interface
    def override_binary_namespace(self) -> str:
        return str(self._com_obj.OverrideBinaryNamespace)

    @property
    @ts_interface
    def override_binary_project_path(self) -> str:
        return str(self._com_obj.OverrideBinaryProjectPath)

    @property
    @ts_interface
    def override_binary_vi_path(self) -> str:
        return str(self._com_obj.OverrideBinaryVIPath)

    @property
    @ts_interface
    def override_module_options(self) -> LabVIEWModuleOverrideType:
        return LabVIEWModuleOverrideType(self._com_obj.OverrideModuleOptions)

    @override_module_options.setter
    @ts_interface
    def override_module_options(self, value: LabVIEWModuleOverrideType | int) -> None:
        self._com_obj.OverrideModuleOptions = int(value)

    @property
    @ts_interface
    def parameters(self) -> typing.Any:
        return self._com_obj.Parameters

    @property
    @ts_interface
    def remote_connection_timeout(self) -> float:
        return float(self._com_obj.RemoteConnectionTimeout)

    @remote_connection_timeout.setter
    @ts_interface
    def remote_connection_timeout(self, value: float) -> None:
        self._com_obj.RemoteConnectionTimeout = float(value)

    @property
    @ts_interface
    def remote_host(self) -> str:
        return str(self._com_obj.RemoteHost)

    @remote_host.setter
    @ts_interface
    def remote_host(self, value: str) -> None:
        self._com_obj.RemoteHost = str(value)

    @property
    @ts_interface
    def remote_port_number(self) -> int:
        return int(self._com_obj.RemotePortNumber)

    @remote_port_number.setter
    @ts_interface
    def remote_port_number(self, value: int) -> None:
        self._com_obj.RemotePortNumber = int(value)

    @property
    @ts_interface
    def remote_project_path(self) -> str:
        return str(self._com_obj.RemoteProjectPath)

    @remote_project_path.setter
    @ts_interface
    def remote_project_path(self, value: str) -> None:
        self._com_obj.RemoteProjectPath = str(value)

    @property
    @ts_interface
    def match_array_parameters_to_labview_array_dimensions(self) -> bool:
        return bool(self._com_obj.MatchArrayParametersToLabVIEWArrayDimensions)

    @match_array_parameters_to_labview_array_dimensions.setter
    @ts_interface
    def match_array_parameters_to_labview_array_dimensions(self, value: bool) -> None:
        self._com_obj.MatchArrayParametersToLabVIEWArrayDimensions = bool(value)

    @property
    @ts_interface
    def namespace(self) -> str:
        return str(self._com_obj.Namespace)

    @namespace.setter
    @ts_interface
    def namespace(self, value: str) -> None:
        self._com_obj.Namespace = str(value)

    @property
    @ts_interface
    def node_class_data_name(self) -> str:
        return str(self._com_obj.NodeClassDataName)

    @node_class_data_name.setter
    @ts_interface
    def node_class_data_name(self, value: str) -> None:
        self._com_obj.NodeClassDataName = str(value)

    @property
    @ts_interface
    def node_ignores_internal_errors(self) -> bool:
        return bool(self._com_obj.NodeIgnoresInternalErrors)

    @node_ignores_internal_errors.setter
    @ts_interface
    def node_ignores_internal_errors(self, value: bool) -> None:
        self._com_obj.NodeIgnoresInternalErrors = bool(value)

    @property
    @ts_interface
    def node_library_generic_type_name(self) -> str:
        return str(self._com_obj.NodeLibraryGenericTypeName)

    @node_library_generic_type_name.setter
    @ts_interface
    def node_library_generic_type_name(self, value: str) -> None:
        self._com_obj.NodeLibraryGenericTypeName = str(value)

    @property
    @ts_interface
    def node_library_name(self) -> str:
        return str(self._com_obj.NodeLibraryName)

    @node_library_name.setter
    @ts_interface
    def node_library_name(self, value: str) -> None:
        self._com_obj.NodeLibraryName = str(value)

    @property
    @ts_interface
    def node_operation_mode(self) -> typing.Any:
        return int(self._com_obj.NodeOperationMode)

    @node_operation_mode.setter
    @ts_interface
    def node_operation_mode(self, value: int) -> None:
        self._com_obj.NodeOperationMode = int(value)

    @property
    @ts_interface
    def node_properties(self) -> typing.Any:
        return self._com_obj.NodeProperties

    @property
    @ts_interface
    def node_uses_data_value_reference(self) -> typing.Any:
        return bool(self._com_obj.NodeUsesDataValueReference)

    @node_uses_data_value_reference.setter
    @ts_interface
    def node_uses_data_value_reference(self, value: bool) -> None:
        self._com_obj.NodeUsesDataValueReference = bool(value)

    @property
    @ts_interface
    def override_binary_class_path(self) -> str:
        return str(self._com_obj.OverrideBinaryClassPath)

    @override_binary_class_path.setter
    @ts_interface
    def override_binary_class_path(self, value: str) -> None:
        self._com_obj.OverrideBinaryClassPath = str(value)

    @property
    @ts_interface
    def express_vi_name(self) -> str:
        return str(self._com_obj.ExpressVIName)

    @ts_interface
    def find_class_url_using_class_path(self, class_path: str) -> typing.Any:
        return str(self._com_obj.FindClassURLUsingClassPath(str(class_path)))

    @ts_interface
    def find_class_url_using_class_path_ex(self, class_path: str, options: int = 0) -> typing.Any:
        return str(self._com_obj.FindClassURLUsingClassPathEx(str(class_path), int(options)))

    @ts_interface
    def find_vi_url_using_vi_path(self, vi_path: str) -> typing.Any:
        return str(self._com_obj.FindVIURLUsingVIPath(str(vi_path)))

    @ts_interface
    def find_vi_url_using_vi_path_ex(self, vi_path: str, options: int = 0) -> typing.Any:
        return str(self._com_obj.FindVIURLUsingVIPathEx(str(vi_path), int(options)))

    @ts_interface
    def get_binary_build_specifications(self) -> typing.Any:
        return list(self._com_obj.GetBinaryBuildSpecifications())

    @ts_interface
    def get_class_absolute_path(self, class_path: str) -> typing.Any:
        return str(self._com_obj.GetClassAbsolutePath(str(class_path)))

    @ts_interface
    def get_class_absolute_path_ex(self, class_path: str, options: int = 0) -> typing.Any:
        return str(self._com_obj.GetClassAbsolutePathEx(str(class_path), int(options)))

    @ts_interface
    def get_project_url_paths_for_classes(self) -> list[str]:
        return list(self._com_obj.GetProjectURLPathsForClasses())

    @ts_interface
    def get_project_url_paths_for_vis(self) -> list[str]:
        return list(self._com_obj.GetProjectURLPathsForVIs())

    @ts_interface
    def convert_express_vi_to_standard_vi(self, new_vi_path: str) -> typing.Any:
        return bool(self._com_obj.ConvertExpressVIToStandardVI(new_vi_path))

    @ts_interface
    def as_module(self) -> typing.Any:
        from py_teststand.adapters import Module

        return Module(self._com_obj.AsModule(), self._engine_ref)


class LabVIEWParameter(PropertyObject):
    @property
    @ts_interface
    def array_dimensions(self) -> int:
        return int(self._com_obj.ArrayDimensions)

    @property
    @ts_interface
    def array_element_prototype(self) -> typing.Any:
        return self._com_obj.ArrayElementPrototype

    @ts_interface
    def as_property_object(self) -> PropertyObject:
        return PropertyObject(self._com_obj.AsPropertyObject(), self._engine_ref)

    @property
    @ts_interface
    def category(self) -> typing.Any:
        return int(self._com_obj.Category)

    @property
    @ts_interface
    def complex_imaginary_part_element(self) -> typing.Any:
        return self._com_obj.ComplexImaginaryPartElement

    @property
    @ts_interface
    def complex_real_part_element(self) -> typing.Any:
        return self._com_obj.ComplexRealPartElement

    @ts_interface
    def create_default_array_elements(self) -> None:
        self._com_obj.CreateDefaultArrayElements()

    @property
    @ts_interface
    def default_value(self) -> typing.Any:
        return self._com_obj.DefaultValue

    @ts_interface
    def delete_array_element(self, index: int) -> typing.Any:
        self._com_obj.DeleteArrayElement(int(index))

    @ts_interface
    def delete_array_elements(self, index: int, count: int) -> None:
        self._com_obj.DeleteArrayElements(int(index), int(count))

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
        return self._com_obj.Elements

    @ts_interface
    def expr_cluster_type_mismatch(
        self, sequence_context: typing.Any, expr: str, error_msg: str
    ) -> tuple[bool, str]:
        raw_ctx = getattr(sequence_context, "_com_obj", sequence_context)
        result = self._com_obj.ExprClusterTypeMismatch(raw_ctx, str(expr), str(error_msg))
        if isinstance(result, tuple):
            return result
        return (bool(result), str(error_msg))

    @ts_interface
    def get_nxg_array_index(self, dimension: int) -> typing.Any:
        return int(self._com_obj.GetArrayIndex(int(dimension)))

    @ts_interface
    def get_default_array_dimension_size(self, dimension: int) -> typing.Any:
        return int(self._com_obj.GetDefaultArrayDimensionSize(int(dimension)))

    @ts_interface
    def get_enum_values(self) -> list[str]:
        return list(self._com_obj.GetEnumValues())

    @ts_interface
    def insert_array_element(self, index: int) -> typing.Any:
        self._com_obj.InsertArrayElement(int(index))

    @property
    @ts_interface
    def is_cluster_mapping_invalid(self) -> typing.Any:
        return bool(self._com_obj.IsClusterMappingInvalid)

    @property
    @ts_interface
    def is_node_using_default(self) -> bool:
        return bool(self._com_obj.IsNodeUsingDefault)

    @property
    @ts_interface
    def is_parameter_mapping_valid(self) -> typing.Any:
        return bool(self._com_obj.IsParameterMappingValid)

    @property
    @ts_interface
    def parameter_caption(self) -> str:
        return str(self._com_obj.ParameterCaption)

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
    def update_cluster_mapping(self) -> typing.Any:
        self._com_obj.UpdateClusterMapping()

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
    def user_data(self, value: PropertyObject) -> None:
        self._com_obj.UserData = value._com_obj

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


class LabVIEWParameterElement(PropertyObject):
    @property
    @ts_interface
    def array_dimensions(self) -> int:
        return int(self._com_obj.ArrayDimensions)

    @property
    @ts_interface
    def array_element_prototype(self) -> typing.Any:
        return self._com_obj.ArrayElementPrototype

    @ts_interface
    def as_property_object(self) -> PropertyObject:
        return PropertyObject(self._com_obj.AsPropertyObject(), self._engine_ref)

    @property
    @ts_interface
    def category(self) -> typing.Any:
        return int(self._com_obj.Category)

    @property
    @ts_interface
    def complex_imaginary_part_element(self) -> typing.Any:
        return self._com_obj.ComplexImaginaryPartElement

    @property
    @ts_interface
    def complex_real_part_element(self) -> typing.Any:
        return self._com_obj.ComplexRealPartElement

    @ts_interface
    def create_default_array_elements(self) -> None:
        self._com_obj.CreateDefaultArrayElements()

    @property
    @ts_interface
    def default_value(self) -> typing.Any:
        return self._com_obj.DefaultValue

    @ts_interface
    def delete_array_element(self, index: int) -> typing.Any:
        self._com_obj.DeleteArrayElement(int(index))

    @ts_interface
    def delete_array_elements(self, index: int, count: int) -> None:
        self._com_obj.DeleteArrayElements(int(index), int(count))

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
        return self._com_obj.Elements

    @ts_interface
    def expr_cluster_type_mismatch(
        self, sequence_context: typing.Any, expr: str, error_msg: str
    ) -> tuple[bool, str]:
        raw_ctx = getattr(sequence_context, "_com_obj", sequence_context)
        result = self._com_obj.ExprClusterTypeMismatch(raw_ctx, str(expr), str(error_msg))
        if isinstance(result, tuple):
            return result
        return (bool(result), str(error_msg))

    @ts_interface
    def get_nxg_array_index(self, dimension: int) -> typing.Any:
        return int(self._com_obj.GetArrayIndex(int(dimension)))

    @ts_interface
    def get_default_array_dimension_size(self, dimension: int) -> typing.Any:
        return int(self._com_obj.GetDefaultArrayDimensionSize(int(dimension)))

    @ts_interface
    def get_enum_values(self) -> list[str]:
        return list(self._com_obj.GetEnumValues())

    @ts_interface
    def insert_array_element(self, index: int) -> typing.Any:
        self._com_obj.InsertArrayElement(int(index))

    @property
    @ts_interface
    def is_cluster_mapping_invalid(self) -> typing.Any:
        return bool(self._com_obj.IsClusterMappingInvalid)

    @property
    @ts_interface
    def is_node_using_default(self) -> bool:
        return bool(self._com_obj.IsNodeUsingDefault)

    @property
    @ts_interface
    def is_parameter_mapping_valid(self) -> typing.Any:
        return bool(self._com_obj.IsParameterMappingValid)

    @property
    @ts_interface
    def parameter_caption(self) -> str:
        return str(self._com_obj.ParameterCaption)

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
    def update_cluster_mapping(self) -> typing.Any:
        self._com_obj.UpdateClusterMapping()

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
    def user_data(self, value: PropertyObject) -> None:
        self._com_obj.UserData = value._com_obj

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


class LabVIEWArguments(PropertyObject):
    @property
    @ts_interface
    def count(self) -> int:
        return int(self._com_obj.Count)

    @ts_interface
    def item(self, index: typing.Any) -> typing.Any:
        return LabVIEWArgument(self._com_obj.Item(index), self._engine_ref)

    def __len__(self) -> int:

        return self.count

    def __getitem__(self, index: typing.Any) -> LabVIEWArgument:

        return self.item(index)


class LabVIEWArgument(PropertyObject):
    @property
    @ts_interface
    def complex_imaginary_part(self) -> LabVIEWArgument:
        return LabVIEWArgument(self._com_obj.ComplexImaginaryPart, self._engine_ref)

    @property
    @ts_interface
    def complex_real_part(self) -> LabVIEWArgument:
        return LabVIEWArgument(self._com_obj.ComplexRealPart, self._engine_ref)

    @property
    @ts_interface
    def elements(self) -> LabVIEWArguments:
        return LabVIEWArguments(self._com_obj.Elements, self._engine_ref)

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


class LabVIEWNodeProperties(PropertyObject):
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
        return LabVIEWNodeProperty(self._com_obj.Item(index), self._engine_ref)

    @ts_interface
    def new(
        self,
        index: typing.Any,
        long_name: str,
        data_name: str,
        unique_id: str,
        direction: LabVIEWNodePropertyDirection | int,
    ) -> None:
        self._com_obj.New(index, long_name, data_name, unique_id, int(direction))

    def __len__(self) -> int:

        return self.count

    def __getitem__(self, index: typing.Any) -> LabVIEWNodeProperty:

        return self.item(index)


class LabVIEWNodeProperty(PropertyObject):
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

        return LabVIEWNodePropertyDirection(self._com_obj.Direction)

    @direction.setter
    @ts_interface
    def direction(self, value: LabVIEWNodePropertyDirection | int) -> None:
        self._com_obj.Direction = int(value)

    @property
    @ts_interface
    def long_name(self) -> str:
        return str(self._com_obj.LongName)

    @property
    @ts_interface
    def unique_id(self) -> str:
        return str(self._com_obj.UniqueID)
