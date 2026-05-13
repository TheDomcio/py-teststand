from __future__ import annotations

import pytest

from py_teststand.adapters.dotnet import (
    DotNetRuntimeKind,
    parse_dotnet_runtime_kind,
)


@pytest.mark.parametrize(
    "clr_version, expected",
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
