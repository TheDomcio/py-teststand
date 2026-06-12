"""Contract tests for the ActiveX/COM adapter wrapper.

Cover the adapter settings a caller toggles (late binding), the module members
used to specify a COM call (member name, member type, create option), the
member-info load call, the parameters collection, and the UpdateAutomationIDs
result mapping. Each test pins the exact COM member invoked, the argument
conversion, and how results are typed, using a MagicMock for the COM dispatch
object so they run with no TestStand installed.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from py_teststand.adapters.activex import (
    ActiveXAdapter,
    ActiveXModule,
    ActiveXModuleCreate,
    ActiveXModuleMemberType,
    ActiveXParameters,
)


@pytest.fixture
def mock_engine():
    return MagicMock()


def test_update_automation_ids_maps_result_tuple(mock_engine):
    com = MagicMock()
    com.UpdateAutomationIDs.return_value = (10, 2, "Some error")
    adapter = ActiveXAdapter(com, mock_engine)

    sequence_file = MagicMock()
    sequence_file._com_obj = "seq_file_com"
    result = adapter.update_automation_ids(sequence_file)

    com.UpdateAutomationIDs.assert_called_once_with("seq_file_com")
    assert result.num_steps_modified == 10
    assert result.num_step_updates_failed == 2
    assert result.error_description == "Some error"


def test_adapter_use_late_binding_getter_and_setter(mock_engine):
    com = MagicMock()
    com.UseLateBinding = True
    adapter = ActiveXAdapter(com, mock_engine)

    assert adapter.use_late_binding is True
    adapter.use_late_binding = False
    assert com.UseLateBinding is False


def test_module_member_name_getter_and_setter(mock_engine):
    com = MagicMock()
    com.MemberName = "Open"
    module = ActiveXModule(com, mock_engine)

    assert module.member_name == "Open"
    module.member_name = "Close"
    assert com.MemberName == "Close"


def test_module_member_type_casts_enum_and_setter_writes_int(mock_engine):
    com = MagicMock()
    com.MemberType = int(ActiveXModuleMemberType.GetProperty)
    module = ActiveXModule(com, mock_engine)

    assert module.member_type == ActiveXModuleMemberType.GetProperty
    module.member_type = ActiveXModuleMemberType.CallMethod
    assert com.MemberType == int(ActiveXModuleMemberType.CallMethod)


def test_module_create_option_casts_enum(mock_engine):
    com = MagicMock()
    com.CreateOption = int(ActiveXModuleCreate.AttachToActive)
    module = ActiveXModule(com, mock_engine)

    create_option = module.create_option
    assert isinstance(create_option, ActiveXModuleCreate)
    assert create_option == ActiveXModuleCreate.AttachToActive


def test_module_load_member_info_forwards_flag_and_returns_bool(mock_engine):
    com = MagicMock()
    com.LoadMemberInfo.return_value = True
    module = ActiveXModule(com, mock_engine)

    result = module.load_member_info(discard_parameter_values=True)

    com.LoadMemberInfo.assert_called_once_with(True)
    assert result is True


def test_module_parameters_wraps_collection(mock_engine):
    com = MagicMock()
    inner = MagicMock()
    com.Parameters = inner
    module = ActiveXModule(com, mock_engine)

    parameters = module.parameters

    assert isinstance(parameters, ActiveXParameters)
    assert parameters._com_obj is inner
