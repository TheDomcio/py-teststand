from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from py_teststand.analyzer.analysis_message import AnalysisMessage


class Error(Exception):
    __test__ = False

    def __init__(
        self,
        message: str,
        hresult: int | None = None,
        source: str | None = None,
        description: str | None = None,
    ) -> None:
        self.hresult = hresult
        self.source = source
        self.description = description

        if hresult is not None:
            formatted_hr = f"0x{hresult & 0xFFFFFFFF:08X}"
            detail = description or message
            full_msg = f"[{formatted_hr}] {detail}"
            if source:
                full_msg = f"{source}: {full_msg}"
            super().__init__(full_msg)
        else:
            super().__init__(message)


class COMError(Error):
    pass


class LicenseError(Error):
    pass


class SequenceFileLoadError(Error):
    pass


class StepExecutionError(Error):
    pass


class InvalidPropertyError(Error):
    pass


class SystemError(Error):
    pass


class MemoryError(SystemError):
    pass


class IOError(Error, OSError):
    pass


class AccessDeniedError(IOError):
    pass


class FileAlreadyExistsError(IOError):
    pass


class FileNotFoundError(IOError):
    pass


class PathNotFoundError(FileNotFoundError):
    pass


class PropertyError(Error):
    pass


class IndexOutOfRangeError(PropertyError, IndexError):
    pass


class TypeMismatchError(PropertyError, TypeError):
    pass


class ExecutionError(Error):
    pass


class ModuleLoadError(ExecutionError):
    pass


class SequenceAbortedError(ExecutionError):
    pass


class SequenceTerminatedError(ExecutionError):
    pass


class AdapterError(Error):
    pass


class DeploymentError(Error):
    pass


class SequenceValidationError(Error):
    def __init__(
        self,
        message: str,
        analysis_messages: list[AnalysisMessage | None] | None = None,
    ) -> None:
        self.analysis_messages = analysis_messages or []
        super().__init__(message)


TESTSTAND_KNOWN_ERROR_CODES: frozenset = frozenset(
    {
        -19065,
        -19064,
        -19063,
        -19062,
        -19060,
        -19059,
        -19058,
        -19057,
        -19056,
        -19055,
        -19054,
        -19053,
        -19052,
        -19046,
        -19045,
        -19044,
        -19043,
        -19042,
        -19041,
        -19040,
        -19039,
        -19038,
        -19037,
        -19036,
        -19035,
        -19034,
        -19033,
        -19031,
        -19030,
        -19029,
        -19028,
        -19027,
        -19026,
        -19025,
        -19024,
        -19022,
        -19021,
        -19020,
        -19015,
        -19014,
        -19013,
        -19011,
        -19010,
        -19009,
        -19007,
        -19006,
        -19004,
        -19002,
        -19001,
        -19000,
        -18360,
        -17603,
        -17602,
        -17600,
        -17306,
        -17301,
        -17212,
        -17208,
        -17000,
        19200,
        19201,
        19202,
        19203,
        19204,
        19205,
        19206,
        19207,
        19208,
        19209,
        19210,
        19211,
        19212,
        19213,
        19215,
        19216,
        19217,
        19218,
        19219,
        19220,
        19221,
        19222,
        19223,
        19404,
        19405,
        19407,
        19408,
        19409,
        19410,
        19411,
        19412,
        19413,
        19414,
        19415,
        19416,
        19417,
        19418,
        19419,
        19420,
        19421,
        19422,
        19423,
        19424,
        19425,
        19426,
        19427,
        19428,
        19429,
        19430,
        19431,
        19436,
        19437,
        19438,
        19439,
        19440,
        19441,
        19442,
        19443,
        19444,
        19445,
        19446,
        19447,
    },
)


def _generate_error_map():
    emap: dict[int, type[Error]] = {}

    for code in TESTSTAND_KNOWN_ERROR_CODES:
        if -17099 <= code <= -17000:
            emap[code] = SystemError
        elif -17299 <= code <= -17100:
            emap[code] = IOError
        elif -17399 <= code <= -17300:
            emap[code] = PropertyError
        elif -17699 <= code <= -17400:
            emap[code] = ExecutionError
        elif -17799 <= code <= -17700 or -18099 <= code <= -18000:
            emap[code] = AdapterError
        elif -19999 <= code <= -19000:
            emap[code] = DeploymentError
        else:
            emap[code] = Error

    emap[-17000] = MemoryError
    emap[-17500] = ExecutionError
    emap[-17205] = AccessDeniedError
    emap[-17208] = FileNotFoundError
    emap[-17301] = IndexOutOfRangeError
    emap[-17306] = InvalidPropertyError
    emap[-17324] = IndexOutOfRangeError
    emap[-17321] = TypeMismatchError
    emap[-17600] = ModuleLoadError
    emap[-17602] = SequenceAbortedError
    emap[-17603] = SequenceTerminatedError
    emap[-19036] = SequenceFileLoadError

    emap[-18360] = LicenseError

    return emap


ERROR_MAP = _generate_error_map()

