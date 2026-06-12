"""Contract tests for the LabVIEW adapter wrapper.

Cover the members a caller uses to configure a VI call step: the module's VI and
project paths, its call type, the adapter's module factory and server version, and
a LabVIEW parameter's array-index lookup. Each test pins the exact COM member the
wrapper invokes, the argument conversion, and how the return value is typed, using
a MagicMock for the COM dispatch object so they run with no TestStand or LabVIEW
installed.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from py_teststand.adapters.labview import (
    LabVIEWAdapter,
    LabVIEWCallType,
    LabVIEWModule,
    LabVIEWParameter,
    LabVIEWParameterElement,
    LabVIEWProjectPath,
)


def test_module_vi_path_getter_coerces_to_str():
    com = MagicMock()
    com.VIPath = r"example.lvlibp\measure.vi"
    assert LabVIEWModule(com).vi_path == r"example.lvlibp\measure.vi"


def test_module_vi_path_setter_writes_com_member():
    com = MagicMock()
    LabVIEWModule(com).vi_path = r"other.vi"
    assert com.VIPath == r"other.vi"


def test_module_project_path_getter_and_setter():
    com = MagicMock()
    com.ProjectPath = "Libraries.lvproj"
    module = LabVIEWModule(com)
    assert module.project_path == "Libraries.lvproj"
    module.project_path = "Other.lvproj"
    assert com.ProjectPath == "Other.lvproj"


def test_module_call_type_getter_casts_enum():
    com = MagicMock()
    com.CallType = int(LabVIEWCallType.ClassMemberCall)
    call_type = LabVIEWModule(com).call_type
    assert isinstance(call_type, LabVIEWCallType)
    assert call_type == LabVIEWCallType.ClassMemberCall


def test_module_call_type_setter_writes_int():
    com = MagicMock()
    LabVIEWModule(com).call_type = LabVIEWCallType.PropertyNodeCall
    assert com.CallType == int(LabVIEWCallType.PropertyNodeCall)


def test_adapter_new_module_wraps_com_result():
    com = MagicMock()
    inner = MagicMock()
    com.NewModule.return_value = inner

    module = LabVIEWAdapter(com).new_module()

    com.NewModule.assert_called_once_with()
    assert isinstance(module, LabVIEWModule)
    assert module._com_obj is inner


def test_adapter_current_server_version_coerces_to_str():
    com = MagicMock()
    com.CurrentLabVIEWServerVersion = 2026
    assert LabVIEWAdapter(com).current_labview_server_version == "2026"


def test_parameter_get_array_index_from_offset_calls_getarrayindex():
    com = MagicMock()
    com.GetArrayIndex.return_value = 3
    result = LabVIEWParameter(com).get_array_index_from_offset(2)
    com.GetArrayIndex.assert_called_once_with(2)
    assert result == 3
    assert isinstance(result, int)


def test_module_class_path_getter_and_setter():
    com = MagicMock()
    com.ClassPath = r"libs\Widget.lvclass"
    module = LabVIEWModule(com)
    assert module.class_path == r"libs\Widget.lvclass"
    module.class_path = r"other.lvclass"
    assert com.ClassPath == r"other.lvclass"


def test_module_td_checksum_getter_and_setter():
    com = MagicMock()
    com.TDChecksum = "abc123"
    module = LabVIEWModule(com)
    assert module.td_checksum == "abc123"
    module.td_checksum = "def456"
    assert com.TDChecksum == "def456"


def test_module_get_project_url_paths_for_classes_returns_list():
    com = MagicMock()
    com.GetProjectUrlPathsForClasses.return_value = ("a.lvclass", "b.lvclass")
    result = LabVIEWModule(com).get_project_url_paths_for_classes()
    com.GetProjectUrlPathsForClasses.assert_called_once_with()
    assert result == ["a.lvclass", "b.lvclass"]


def test_module_find_vi_url_using_vi_path_forwards_enum_int():
    com = MagicMock()
    com.FindVIUrlUsingVIPath.return_value = "http://host/measure.vi"
    result = LabVIEWModule(com).find_vi_url_using_vi_path(LabVIEWProjectPath.Remote)
    com.FindVIUrlUsingVIPath.assert_called_once_with(int(LabVIEWProjectPath.Remote))
    assert result == "http://host/measure.vi"


def test_module_load_prototype_inherited_from_module_base():
    # LabVIEWModule.LoadPrototype is obsolete; the base Module.load_prototype is used.
    com = MagicMock()
    com.LoadPrototype.return_value = True
    assert LabVIEWModule(com).load_prototype() is True
    com.LoadPrototype.assert_called_once()


def test_parameter_element_uses_element_members_not_parameter_members():
    com = MagicMock()
    com.ElementName = "[0]"
    com.ElementCaption = "Element 0"
    com.IndexString = "0"
    element = LabVIEWParameterElement(com)
    assert element.element_name == "[0]"
    assert element.element_caption == "Element 0"
    assert element.index_string == "0"


def test_removed_hallucinated_members_are_absent():
    # ClassName was never a LabVIEWModule COM member; ParameterName/Caption belong to
    # LabVIEWParameter, not LabVIEWParameterElement. Guard against re-introduction.
    assert not hasattr(LabVIEWModule, "class_name")
    assert not hasattr(LabVIEWParameterElement, "parameter_name")
    assert not hasattr(LabVIEWParameterElement, "parameter_caption")
