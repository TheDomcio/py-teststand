import sys
from unittest.mock import MagicMock, patch

import pytest

HAS_REAL_ENGINE = False


try:
    import pythoncom
    import win32com.client

    pythoncom.CoInitialize()

    win32com.client.Dispatch("TestStand.Engine")

    HAS_REAL_ENGINE = True

    pythoncom.CoUninitialize()


except Exception:

    class com_error(Exception):  # noqa: N818
        def __init__(self, hresult, message, *_args):

            self.hresult = hresult

            super().__init__(message)

    pythoncom_mock = MagicMock(name="pythoncom_mock")

    pythoncom_mock.com_error = com_error

    sys.modules["pythoncom"] = pythoncom_mock

    win32com_mock = MagicMock(name="win32com_mock")

    sys.modules["win32com"] = win32com_mock

    sys.modules["win32com.client"] = win32com_mock.client

    sys.modules["win32com.client.gencache"] = win32com_mock.client.gencache

    import pythoncom
    import win32com.client


@pytest.fixture(autouse=True, scope="session")
def mock_win32com_environment():

    if HAS_REAL_ENGINE:
        yield None

        return

    mock_engine = MagicMock(name="MockTestStandEngine")

    mock_engine.VersionString = "23.0.0"

    with patch("win32com.client.Dispatch", return_value=mock_engine), patch(
        "win32com.client.gencache.EnsureDispatch", return_value=mock_engine
    ), patch("win32com.client.DispatchEx", return_value=mock_engine):
        yield mock_engine


@pytest.fixture(scope="session")
def engine():

    from py_teststand import Engine

    eng = Engine()

    yield eng

    try:
        eng.shutdown()

    except Exception:
        pass


def pytest_addoption(parser):

    parser.addoption(
        "--run-live-com",
        action="store_true",
        default=False,
        help="run tests that require a live TestStand COM installation",
    )


def pytest_configure(config):

    config.addinivalue_line("markers", "network: requires outbound HTTPS")

    config.addinivalue_line("markers", "integration: tests requiring a live TestStand Engine")

    config.addinivalue_line("markers", "no_cover: disable coverage tracer")

    config.addinivalue_line(
        "markers", "live_com: mark test as requiring live TestStand COM instance"
    )


def pytest_collection_modifyitems(config, items):

    if config.getoption("--run-live-com"):
        return

    skip_live = pytest.mark.skip(reason="need --run-live-com option to run")

    for item in items:
        if "live_com" in item.keywords or "integration" in item.keywords:
            item.add_marker(skip_live)
