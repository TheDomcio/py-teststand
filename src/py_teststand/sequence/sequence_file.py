from __future__ import annotations

import functools
import typing
import weakref
from enum import Enum, IntEnum
from typing import TYPE_CHECKING

try:
    import pythoncom
except ImportError:
    pythoncom: typing.Any = None

from py_teststand.core.com_wrapper import ts_interface
from py_teststand.property.property_object_file import PropertyObjectFile
from py_teststand.sequence.sequence import Sequence


class ModelOption(IntEnum):
    UseStationModel = 0
    NoModel = 1
    RequireSpecificModel = 2


class ModuleLoadOption(IntEnum):
    DynamicLoad = 3
    PreloadWhenExecuted = 2
    PreloadWhenOpened = 1
    UseStepLoadOption = 4


class ModuleUnloadOption(IntEnum):
    AfterSequenceExecution = 3
    AfterStepExecution = 2
    OnPreconditionFailure = 1
    UseStepUnloadOption = 5
    WithSequenceFile = 4


class SeqFileBatchSynchronization(IntEnum):
    UseModelSetting = 1
    NoSync = 2
    Serial = 3
    Parallel = 4
    OneThreadOnly = 5


class SeqFileCallback(str, Enum):
    Load = "SequenceFileLoad"
    PostInteractive = "SequenceFilePostInteractive"
    PostResultListEntry = "SequenceFilePostResultListEntry"
    PostResults = "SequenceFilePostResults"
    PostStep = "SequenceFilePostStep"
    PostStepFailure = "SequenceFilePostStepFailure"
    PostStepRuntimeError = "SequenceFilePostStepRuntimeError"
    PreInteractive = "SequenceFilePreInteractive"
    PreStep = "SequenceFilePreStep"
    Unload = "SequenceFileUnload"


class SequenceFileDisplayReason(IntEnum):
    SequenceFileOpened = 1
    UserRequestedOpenWindow = 2


class QueryReloadSequenceFileOption(IntEnum):
    Prompt = 0
    Reload = 1
    Cancel = 2


if TYPE_CHECKING:
    from py_teststand.core.engine import Engine
    from py_teststand.property.property_object import PropertyObject
    from py_teststand.property.property_object_file import PropertyObjectFileType
    from py_teststand.sequence.sequence_context import SequenceContext


class SequenceCollection:
    def __init__(self, sequence_file: SequenceFile):

        self._sequence_file = sequence_file

    def __len__(self) -> int:

        return self._sequence_file.num_sequences

    def __getitem__(self, index: int | str | slice) -> Sequence | list[Sequence]:

        if isinstance(index, str):
            return self._sequence_file.get_sequence_by_name(index)
        if isinstance(index, slice):
            return typing.cast(
                "list[Sequence]", [self[i] for i in range(*index.indices(len(self)))]
            )
        return self._sequence_file.get_sequence(index)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    def __contains__(self, name: str) -> bool:

        try:
            self._sequence_file.get_sequence_by_name(name)
            return True
        except Exception:
            return False


class SequenceFile(PropertyObjectFile):
    def __init__(self, com_obj: typing.Any, engine: Engine | typing.Any | None = None) -> None:

        super().__init__(com_obj)
        self._engine_ref = (
            engine
            if isinstance(engine, weakref.ReferenceType) or engine is None
            else weakref.ref(engine)
        )

    def __enter__(self) -> SequenceFile:

        return self

    def __exit__(self, exc_type: typing.Any, exc_val: typing.Any, exc_tb: typing.Any) -> None:

        try:
            if self.engine:
                self.engine.release_sequence_file(self)
        except Exception:
            pass
        self.release()

    def release(self, _force: bool = False) -> None:
        if self._com_obj is not None:
            try:
                if self.engine is not None:
                    self.engine.release_sequence_file(self)
            except Exception:
                pass
        try:
            object.__setattr__(self, "_com_obj", None)
        except Exception:
            pass

    def __del__(self) -> None:

        try:
            if hasattr(self, "_com_obj") and self._com_obj is not None:
                self.release()
        except Exception:
            pass

    @property
    def engine(self) -> Engine | None:

        if self._engine_ref is None:
            return None
        return typing.cast("Engine | None", self._engine_ref())

    @property
    @ts_interface
    def sequence_file_type(self) -> typing.Any:
        return int(self._com_obj.SequenceFileType)

    @sequence_file_type.setter
    @ts_interface
    def sequence_file_type(self, value: int) -> None:
        self._com_obj.SequenceFileType = value

    @property
    @ts_interface
    def model_path(self) -> str:
        return str(self._com_obj.ModelPath)

    @model_path.setter
    @ts_interface
    def model_path(self, value: str) -> None:
        self._com_obj.ModelPath = value

    @property
    @ts_interface
    def file_globals_scope(self) -> typing.Any:
        return int(self._com_obj.FileGlobalsScope)

    @file_globals_scope.setter
    @ts_interface
    def file_globals_scope(self, value: int) -> None:
        self._com_obj.FileGlobalsScope = value

    @property
    @ts_interface
    def file_globals_default_values(self) -> PropertyObject:
        from py_teststand.property.property_object import PropertyObject

        return PropertyObject(self._com_obj.FileGlobalsDefaultValues, self.engine)

    @property
    @ts_interface
    def file_globals(self) -> PropertyObject:
        return self.file_globals_default_values

    @property
    @ts_interface
    def station_globals(self) -> PropertyObject:
        engine = self.engine
        assert engine is not None, "Engine not available"
        return engine.station_globals

    @property
    @ts_interface
    def change_count(self) -> int:
        return int(self._com_obj.ChangeCount)

    @property
    @ts_interface
    def has_model(self) -> bool:
        return bool(self._com_obj.HasModel)

    @functools.cached_property
    @ts_interface
    def id(self) -> int:
        return int(self._com_obj.Id)

    @property
    @ts_interface
    def is_executing(self) -> bool:
        return bool(self._com_obj.IsExecuting)

    @property
    @ts_interface
    def batch_sync_option(self) -> typing.Any:

        return SeqFileBatchSynchronization(self._com_obj.BatchSyncOption)

    @batch_sync_option.setter
    @ts_interface
    def batch_sync_option(self, value: SeqFileBatchSynchronization | int) -> None:
        self._com_obj.BatchSyncOption = int(value)

    @property
    @ts_interface
    def model_option(self) -> typing.Any:

        return ModelOption(self._com_obj.ModelOption)

    @model_option.setter
    @ts_interface
    def model_option(self, value: ModelOption | int) -> None:
        self._com_obj.ModelOption = int(value)

    @property
    @ts_interface
    def model_path(self) -> str:
        return str(self._com_obj.ModelPath)

    @model_path.setter
    @ts_interface
    def model_path(self, value: str) -> None:
        self._com_obj.ModelPath = value

    @property
    @ts_interface
    def model_plugin_description(self) -> PropertyObject | None:
        from py_teststand.property.property_object import PropertyObject

        com_obj = self._com_obj.ModelPluginDescription
        return PropertyObject(com_obj, self.engine) if com_obj else None

    @property
    @ts_interface
    def module_load_option(self) -> typing.Any:

        return ModuleLoadOption(self._com_obj.ModuleLoadOption)

    @module_load_option.setter
    @ts_interface
    def module_load_option(self, value: ModuleLoadOption | int) -> None:
        self._com_obj.ModuleLoadOption = int(value)

    @property
    @ts_interface
    def module_unload_option(self) -> typing.Any:

        return ModuleUnloadOption(self._com_obj.ModuleUnloadOption)

    @module_unload_option.setter
    @ts_interface
    def module_unload_option(self, value: ModuleUnloadOption | int) -> None:
        self._com_obj.ModuleUnloadOption = int(value)

    @property
    @ts_interface
    def sequence_file_type(self) -> PropertyObjectFileType:
        from py_teststand.property.property_object_file import PropertyObjectFileType

        return PropertyObjectFileType(self._com_obj.SequenceFileType)

    @sequence_file_type.setter
    @ts_interface
    def sequence_file_type(self, value: PropertyObjectFileType | int) -> None:
        self._com_obj.SequenceFileType = int(value)

    @property
    @ts_interface
    def unload_callback_enabled(self) -> bool:
        return bool(self._com_obj.UnloadCallbackEnabled)

    @unload_callback_enabled.setter
    @ts_interface
    def unload_callback_enabled(self, value: bool) -> None:
        self._com_obj.UnloadCallbackEnabled = bool(value)

    @property
    @ts_interface
    def can_unload(self) -> bool:
        return bool(self._com_obj.CanUnload)

    @ts_interface
    def save(self, path: str | None = None) -> typing.Any:
        path_val = str(path) if path is not None else self.path
        self._com_obj.Save(path_val)

    @ts_interface
    def add_load_reference(self) -> None:
        self._com_obj.AddLoadReference()

    @ts_interface
    def as_property_object(self) -> PropertyObject:
        from py_teststand.property.property_object import PropertyObject

        return PropertyObject(self._com_obj.AsPropertyObject(), self.engine)

    @ts_interface
    def as_property_object_file(self) -> PropertyObjectFile:
        return PropertyObjectFile(self._com_obj.AsPropertyObjectFile())

    @ts_interface
    def delete_sequence(self, index: int) -> None:
        self._com_obj.DeleteSequence(index)

    @ts_interface
    def remove_sequence(self, index: int) -> Sequence:
        return Sequence(self._com_obj.RemoveSequence(index), engine=self.engine)

    @ts_interface
    def insert_sequence(self, sequence: Sequence) -> None:
        self._com_obj.InsertSequence(sequence._com_obj)

    @ts_interface
    def insert_sequence_ex(self, index: int, sequence: Sequence) -> None:
        self._com_obj.InsertSequenceEx(index, sequence._com_obj)

    @ts_interface
    def create_callback_override_sequence(
        self,
        callback_name: str,
        allow_copy_default_steps: bool,
    ) -> Sequence:
        return Sequence(
            self._com_obj.CreateCallbackOverrideSequence(
                str(callback_name),
                bool(allow_copy_default_steps),
            ),
            engine=self.engine,
        )

    @ts_interface
    def load_modules(self, options: int = 0, context: typing.Any | None = None) -> typing.Any:
        ctx_com = getattr(context, "_com_obj", context)
        return bool(self._com_obj.LoadModules(int(options), ctx_com))

    @ts_interface
    def unload_modules(self) -> bool:
        return bool(self._com_obj.UnloadModules())

    @property
    @ts_interface
    def num_sequences(self) -> int:
        return int(self._com_obj.NumSequences)

    @ts_interface
    def get_model_absolute_path(self) -> tuple[str, bool]:
        model_exists = False
        result = self._com_obj.GetModelAbsolutePath(model_exists)
        if isinstance(result, tuple) and len(result) >= 2:
            return str(result[0]), bool(result[1])
        return str(result), bool(model_exists)

    @ts_interface
    def get_model_callback_names(self) -> list[str]:
        return list(self._com_obj.GetModelCallbackNames())

    @ts_interface
    def get_model_sequence_file(self) -> tuple[typing.Any, str]:
        model_description = ""
        result = self._com_obj.GetModelSequenceFile(model_description)
        if isinstance(result, tuple) and len(result) >= 2:
            com_file = result[0]
            desc = str(result[1])
        else:
            com_file = result
            desc = model_description

        sf = SequenceFile(com_file, engine=self.engine) if com_file else None
        return sf, desc

    @ts_interface
    def get_reserved_callback_names(self) -> list[str]:
        return list(self._com_obj.GetReservedCallbackNames())

    @ts_interface
    def get_sequence(self, index: int) -> Sequence:
        return Sequence(self._com_obj.GetSequence(index), engine=self.engine)

    @ts_interface
    def get_sequences(self) -> list[Sequence]:
        return [self.get_sequence(i) for i in range(self.num_sequences)]

    @ts_interface
    def get_sequence_by_name(self, name: str) -> Sequence:
        return Sequence(self._com_obj.GetSequenceByName(name), engine=self.engine)

    @ts_interface
    def get_sequence_index(self, name: str) -> int:
        return int(self._com_obj.GetSequenceIndex(name))

    @ts_interface
    def inc_change_count(self) -> None:
        self._com_obj.IncChangeCount()

    @ts_interface
    def new_sequence(self, name: str) -> Sequence:
        engine = self.engine
        assert engine is not None, "Engine not available"
        com_seq = engine._engine.NewSequence()
        com_seq.Name = name
        self._com_obj.InsertSequenceEx(0, com_seq)
        return Sequence(com_seq, engine=self.engine)

    @ts_interface
    def sequence_name_exists(self, name: str) -> bool:
        return bool(self._com_obj.SequenceNameExists(name))

    @ts_interface
    def new_edit_context(self) -> SequenceContext:
        from py_teststand.sequence.sequence_context import SequenceContext

        return SequenceContext(self._com_obj.NewEditContext(), self.engine)

    @property
    @ts_interface
    def path(self) -> typing.Any:

        return self._com_obj.Path

    @path.setter
    @ts_interface
    def path(self, value: typing.Any) -> None:
        self._com_obj.Path = value
