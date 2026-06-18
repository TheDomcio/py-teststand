import importlib
import inspect
import pkgutil
import warnings
from enum import Enum

import py_teststand
from py_teststand.core.com_wrapper import COMWrapper


def test_public_api_exports_all_classes() -> None:
    """Ensure that all public COM wrappers and Enums are exported in the root __init__.py."""
    missing_exports: list[str] = []

    package = py_teststand
    prefix = package.__name__ + "."

    for _importer, modname, _ispkg in pkgutil.walk_packages(package.__path__, prefix):
        if "tests" in modname or "conftest" in modname:
            continue

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                module = importlib.import_module(modname)
            except Exception:
                continue

        for name, obj in inspect.getmembers(module):
            if name.startswith("_"):
                continue

            # Only consider classes defined in py_teststand (not imported from outside)
            if inspect.isclass(obj) and getattr(obj, "__module__", "").startswith("py_teststand"):
                if issubclass(obj, (COMWrapper, Enum)):
                    if name not in py_teststand.__all__:
                        missing_exports.append(f"{name} (from {obj.__module__})")

    missing_exports = sorted(set(missing_exports))

    # Exceptions that are purposefully not in __all__
    # (add to this list if there are actual internal classes that shouldn't be exposed)
    allowed_missing = {
        "BaseAdapter (from py_teststand.adapters.adapter)",
        "UIMessageHandler (from py_teststand.ext.events)",
    }

    missing_exports = [m for m in missing_exports if m not in allowed_missing]

    assert not missing_exports, (
        f"Missing exports in py_teststand.__init__.__all__: {missing_exports}"
    )
