"""COM contract tests: pin each wrapper to the exact COM member it must call.

These are self-contained (no TestStand installation needed) and never touch a
live engine: every wrapper is built around a plain MagicMock standing in for the
COM dispatch object. Unlike a permissive mock that returns something for any
attribute, each test asserts the *specific* COM member name, the argument order
and conversions, and the return-value wrapping. That makes them fail if a member
is renamed, hallucinated, reordered, or loses an int()/float() coercion, which
is the regression class this project most needs to guard against.

A wrapper reaches its dispatch through one of three handles depending on the
class (_com_obj, _engine, or the PropertyObject _property_object property). For a
Mock, the PropertyObject._property_object property returns the mock unchanged, so
asserting on the mock works for all three.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from py_teststand.property.property_object import PropertyObject, PropertyOption
from py_teststand.sequence.sequence import Sequence
from py_teststand.sequence.sequence_file import SequenceFile
from py_teststand.sequence.step import Step
from py_teststand.sequence.step_group import StepGroup


def test_sequence_get_step_calls_getstep_with_group_int_and_wraps_result():
    com = MagicMock()
    inner = MagicMock()
    com.GetStep.return_value = inner

    sequence = Sequence(com)
    step = sequence.get_step(4, StepGroup.Cleanup)

    com.GetStep.assert_called_once_with(4, 2)
    assert isinstance(step, Step)
    assert step._com_obj is inner


def test_sequence_get_num_steps_passes_group_and_coerces_to_int():
    com = MagicMock()
    com.GetNumSteps.return_value = 3

    sequence = Sequence(com)
    count = sequence.get_num_steps(StepGroup.Setup)

    com.GetNumSteps.assert_called_once_with(0)
    assert count == 3
    assert isinstance(count, int)


def test_sequence_insert_step_forwards_raw_com_and_group_int():
    com = MagicMock()
    sequence = Sequence(com)
    step = Step(MagicMock())

    sequence.insert_step(step, 1, StepGroup.Main)

    com.InsertStep.assert_called_once_with(step._com_obj, 1, 1)


def test_sequence_file_get_sequence_by_name_uses_exact_member():
    com = MagicMock()
    inner = MagicMock()
    com.GetSequenceByName.return_value = inner

    sequence_file = SequenceFile(com)
    sequence = sequence_file.get_sequence_by_name("MainSequence")

    com.GetSequenceByName.assert_called_once_with("MainSequence")
    assert isinstance(sequence, Sequence)
    assert sequence._com_obj is inner


def test_step_create_new_unique_step_id_calls_member():
    com = MagicMock()
    Step(com).create_new_unique_step_id()
    com.CreateNewUniqueStepId.assert_called_once_with()


def test_property_object_clone_passes_lookup_and_options_int():
    com = MagicMock()
    cloned = MagicMock()
    com.Clone.return_value = cloned

    result = PropertyObject(com).clone("Locals.X", PropertyOption.NotOwning)

    com.Clone.assert_called_once_with("Locals.X", int(PropertyOption.NotOwning))
    assert isinstance(result, PropertyObject)
    assert result._com_obj is cloned


def test_property_object_get_by_offset_returns_none_when_com_returns_falsy():
    com = MagicMock()
    com.GetPropertyObjectByOffset.return_value = None

    result = PropertyObject(com).get_property_object_by_offset(2)

    com.GetPropertyObjectByOffset.assert_called_once_with(2, 0)
    assert result is None


def test_property_object_get_val_number_coerces_to_float():
    com = MagicMock()
    com.GetValNumber.return_value = 6  # COM may hand back an int

    value = PropertyObject(com).get_val_number("Resolution", 0)

    com.GetValNumber.assert_called_once_with("Resolution", 0)
    assert value == 6.0
    assert isinstance(value, float)


def test_property_object_set_val_string_forwards_arguments_in_order():
    com = MagicMock()

    PropertyObject(com).set_val_string("Mode", int(PropertyOption.InsertIfMissing), "Voltage")

    com.SetValString.assert_called_once_with("Mode", 1, "Voltage")


def test_property_object_set_val_number_forwards_arguments_in_order():
    com = MagicMock()

    PropertyObject(com).set_val_number("Resolution", 0, 6.5)

    com.SetValNumber.assert_called_once_with("Resolution", 0, 6.5)


def test_step_name_getter_coerces_to_str():
    com = MagicMock()
    com.Name = 12345  # COM could hand back a non-string

    assert Step(com).name == "12345"


def test_step_name_setter_writes_name_member():
    com = MagicMock()

    Step(com).name = "Measure"

    assert com.Name == "Measure"


def test_sequence_file_save_forwards_explicit_path():
    com = MagicMock()

    SequenceFile(com).save("C:/tmp/out.seq")

    com.Save.assert_called_once_with("C:/tmp/out.seq")
