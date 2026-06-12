"""Lifecycle and reference-hardening tests for the COM wrapper layer.

The wrapper's most important safety property is that every COM object it holds
has a clear release path and that releasing actually drops the reference, so a
caller cannot leak (or keep using) a COM proxy after it is done with it. These
tests pin that contract using a plain MagicMock for the COM dispatch object, so
they run anywhere with no TestStand installed and never touch a live engine.

Real-COM leak detection (interface counts) lives in the teststand_engine tests in
tests/integration/test_memory_leaks.py.
"""

from __future__ import annotations

import gc
import weakref
from unittest.mock import MagicMock

import pytest

from py_teststand.core.com_wrapper import COMWrapper
from py_teststand.core.engine import Engine
from py_teststand.core.exceptions import Error
from py_teststand.property.property_object import PropertyObject
from py_teststand.sequence.sequence_file import SequenceFile


def test_release_drops_com_reference():
    com = MagicMock()
    wrapper = COMWrapper(com)
    assert wrapper._com_obj is com
    wrapper.release()
    assert wrapper._com_obj is None


def test_access_after_release_raises():
    wrapper = COMWrapper(MagicMock())
    wrapper.release()
    with pytest.raises(Error):
        wrapper._com()


def test_attribute_forwarding_then_fails_after_release():
    com = MagicMock()
    com.SomeMember = 7
    wrapper = COMWrapper(com)
    assert wrapper.SomeMember == 7
    wrapper.release()
    with pytest.raises(Error):
        _ = wrapper.SomeMember


def test_double_release_is_idempotent():
    wrapper = COMWrapper(MagicMock())
    wrapper.release()
    wrapper.release()
    assert wrapper._com_obj is None


def test_context_manager_releases_on_exit():
    com = MagicMock()
    with COMWrapper(com) as wrapper:
        assert wrapper._com_obj is com
    assert wrapper._com_obj is None


def test_del_releases_reference():
    com = MagicMock()
    wrapper = COMWrapper(com)
    wrapper.__del__()
    assert wrapper._com_obj is None


def test_engine_reference_is_weak_not_strong():
    # A child wrapper must not keep the owning engine alive; it holds a weakref.
    engine_stand_in = MagicMock()
    wrapper = COMWrapper(MagicMock(), engine_stand_in)
    assert wrapper.engine is engine_stand_in

    engine_ref = weakref.ref(engine_stand_in)
    del engine_stand_in
    gc.collect()

    assert engine_ref() is None
    assert wrapper.engine is None


def test_property_object_release_drops_reference():
    com = MagicMock()
    property_object = PropertyObject(com)
    assert property_object._property_object is com
    property_object.release()
    assert property_object._com_obj is None


def test_engine_release_sequence_file_releases_wrapper():
    # Hardening: release_sequence_file must hand the file to the engine AND drop
    # the wrapper's COM reference, so no released proxy is left dangling.
    engine = object.__new__(Engine)
    engine._engine = MagicMock()
    sequence_file = SequenceFile(MagicMock())
    inner = sequence_file._com_obj

    engine.release_sequence_file(sequence_file)

    engine._engine.ReleaseSequenceFile.assert_called_once_with(inner)
    assert sequence_file._com_obj is None


def test_engine_release_sequence_file_ex_releases_wrapper():
    engine = object.__new__(Engine)
    engine._engine = MagicMock()
    engine._engine.ReleaseSequenceFileEx.return_value = True
    sequence_file = SequenceFile(MagicMock())
    inner = sequence_file._com_obj

    result = engine.release_sequence_file_ex(sequence_file)

    engine._engine.ReleaseSequenceFileEx.assert_called_once_with(inner, 0)
    assert result is True
    assert sequence_file._com_obj is None


def test_engine_release_sequence_file_ex_keeps_wrapper_when_still_referenced():
    # Per NI docs, ReleaseSequenceFileEx returns False when the file remains in the
    # cache (other load references). The COM reference must NOT be released then.
    engine = object.__new__(Engine)
    engine._engine = MagicMock()
    engine._engine.ReleaseSequenceFileEx.return_value = False
    sequence_file = SequenceFile(MagicMock())

    result = engine.release_sequence_file_ex(sequence_file)

    assert result is False
    assert sequence_file._com_obj is not None


def test_engine_release_sequence_file_tolerates_already_released_wrapper():
    # Calling release twice (or on an already-released wrapper) must not call the
    # engine with a None pointer.
    engine = object.__new__(Engine)
    engine._engine = MagicMock()
    sequence_file = SequenceFile(MagicMock())

    engine.release_sequence_file(sequence_file)
    engine.release_sequence_file(sequence_file)

    engine._engine.ReleaseSequenceFile.assert_called_once()
