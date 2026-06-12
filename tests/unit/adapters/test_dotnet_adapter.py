"""Contract tests for the .NET adapter wrapper.

Cover the module members a caller configures for a .NET call (class name,
constructor index, object creation), the adapter's assembly-info caching, and the
runtime-kind helper that distinguishes .NET Framework from .NET (Core) using the
engine's CLR version - which governs whether GAC assembly locations are usable.
A MagicMock stands in for the COM dispatch object, so these run with no TestStand
installed.
"""

from __future__ import annotations

import logging
from unittest.mock import MagicMock

import pytest

from py_teststand.adapters.dotnet import (
    DotNetAdapter,
    DotNetModule,
    DotNetModuleAssemblyLocation,
    DotNetRuntimeKind,
    parse_dotnet_runtime_kind,
)


@pytest.mark.parametrize(
    ("clr_version", "expected"),
    [
        ("v2.0.50727", DotNetRuntimeKind.Framework),
        ("v4.0.30319", DotNetRuntimeKind.Framework),
        ("4.8.4084.0", DotNetRuntimeKind.Framework),
        ("v5.0.0", DotNetRuntimeKind.Core),
        ("v6.0.16", DotNetRuntimeKind.Core),
        ("v8.0.1", DotNetRuntimeKind.Core),
        ("v9.0.0-preview", DotNetRuntimeKind.Core),
        ("", DotNetRuntimeKind.Unknown),
        ("not-a-version", DotNetRuntimeKind.Unknown),
    ],
)
def test_parse_dotnet_runtime_kind(clr_version, expected):
    assert parse_dotnet_runtime_kind(clr_version) == expected


def test_runtime_kind_core_does_not_support_gac():
    engine = MagicMock()
    engine.dot_net_clr_version = "v6.0.16"
    adapter = DotNetAdapter(MagicMock(), engine)

    assert adapter.runtime_kind == DotNetRuntimeKind.Core
    assert adapter.gac_supported is False


def test_runtime_kind_framework_supports_gac():
    engine = MagicMock()
    engine.dot_net_clr_version = "v4.0.30319"
    adapter = DotNetAdapter(MagicMock(), engine)

    assert adapter.runtime_kind == DotNetRuntimeKind.Framework
    assert adapter.gac_supported is True


def test_module_class_name_getter_and_setter():
    com = MagicMock()
    com.ClassName = "My.Namespace.Widget"
    module = DotNetModule(com)
    assert module.class_name == "My.Namespace.Widget"
    module.class_name = "Other.Type"
    assert com.ClassName == "Other.Type"


def test_module_constructor_index_is_int_and_writable():
    com = MagicMock()
    com.ConstructorIndex = 2
    module = DotNetModule(com)
    assert module.constructor_index == 2
    assert isinstance(module.constructor_index, int)
    module.constructor_index = 5
    assert com.ConstructorIndex == 5


def test_module_create_object_is_bool_and_writable():
    com = MagicMock()
    com.CreateObject = True
    module = DotNetModule(com)
    assert module.create_object is True
    module.create_object = False
    assert com.CreateObject is False


def test_adapter_cache_assembly_info_forwards_location_and_path():
    com = MagicMock()
    DotNetAdapter(com).cache_assembly_info(DotNetModuleAssemblyLocation.File, "lib.dll")
    com.CacheAssemblyInfo.assert_called_once_with(DotNetModuleAssemblyLocation.File, "lib.dll")


def test_cache_assembly_info_warns_for_gac_under_core(caplog):
    engine = MagicMock()
    engine.dot_net_clr_version = "v6.0.0"
    com = MagicMock()
    adapter = DotNetAdapter(com, engine)

    with caplog.at_level(logging.WARNING):
        adapter.cache_assembly_info(DotNetModuleAssemblyLocation.GAC, "lib.dll")

    assert any("GAC" in record.message for record in caplog.records)
    com.CacheAssemblyInfo.assert_called_once_with(DotNetModuleAssemblyLocation.GAC, "lib.dll")
