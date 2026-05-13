from __future__ import annotations

import typing
from unittest.mock import MagicMock

from py_teststand.adapters.adapter import Module
from py_teststand.sequence.step import Step
from py_teststand.ui.connections import StepProperties


class MockCOM:
    def __init__(self, **kwargs):

        self._calls = []

        self._props = kwargs

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __getattr__(self, name):

        if name in self._props:
            return self._props[name]

        if name in self.__dict__:
            return self.__dict__[name]

        numeric_props = [
            "Index",
            "StepIndex",
            "StepGroup",
            "ModuleLoadOption",
            "ModuleUnloadOption",
            "ResultRecordingOption",
            "NumCalls",
            "MajorVersion",
            "MinorVersion",
            "NumAdapters",
            "NumUIMessages",
        ]

        if name in numeric_props:
            return 0

        bool_props = [
            "CanSpecifyModule",
            "CanCreateCode",
            "CanEditCode",
            "BreakpointsEnabled",
            "OutputMessagesEnabled",
            "Modified",
            "IsModified",
            "IsReadOnly",
        ]

        if name in bool_props:
            return False

        if name == "StepType":
            return MockCOM(Name="MockStepType")

        if name in ["Module", "Adapter", "Result", "NextStep", "PreviousStep"]:
            return MockCOM()

        def method(*args, **kwargs):

            self._calls.append((name, args, kwargs))

            return MockCOM()

        return method

    def __call__(self, *_args, **_kwargs):

        return MockCOM()

    def AsPropertyObject(self):  # noqa: N802

        return self


def test_step_properties():

    mock_step_type = MockCOM(Name="MockStepType")

    mock_com = MockCOM(
        Name="MyStep",
        StepIndex=5,
        StepGroup=1,
        StatusExpression='Step.Result.Status = "Done"',
        PreExpression="None",
        PostExpression="None",
        ModuleLoadOption=1,
        ModuleUnloadOption=2,
        ResultRecordingOption=2,
        ResultStatus=StepProperties.ResultStatus_Passed,
        CanSpecifyModule=True,
        CanCreateCode=False,
        CanEditCode=True,
        AdapterKeyName="CAdapt",
        VersionString="2016",
        StepType=mock_step_type,
    )

    step = Step(mock_com)

    assert step.name == "MyStep"

    assert step.index == 5

    assert step.step_group == 1

    assert step.status_expression == 'Step.Result.Status = "Done"'

    assert step.pre_expression == "None"

    assert step.post_expression == "None"

    assert step.module_load_option == 1

    assert step.module_unload_option == 2

    assert step.result_recording_option == 2

    assert step.result_status == StepProperties.ResultStatus_Passed

    assert step.can_specify_module is True

    assert step.can_create_code is False

    assert step.can_edit_code is True

    assert step.adapter_key_name == "CAdapt"

    assert step.step_type is not None

    assert step.step_type.name == "MockStepType"


def test_step_methods():

    from py_teststand.property.property_object import PropertyOption

    mock_com = MockCOM()

    step = Step(mock_com)

    step.specify_module(PropertyOption.NoneValue)

    assert any(c[0] == "SpecifyModule" for c in mock_com._calls)

    step.load_module()

    assert any(c[0] == "LoadModule" for c in mock_com._calls)

    step.unload_module()

    assert any(c[0] == "UnloadModule" for c in mock_com._calls)


def test_step_module():

    mock_com = MockCOM(Module=MockCOM())

    step = Step(mock_com)

    mod = step.module

    assert isinstance(mod, Module)

    assert mod._com_obj is mock_com.Module


def test_step_expression():

    mock_com = MockCOM(CustomActionExpression="Locals.MyVar = 1")

    step = Step(mock_com)

    assert step.expression == "Locals.MyVar = 1"


def test_step_result():

    mock_com = MockCOM(Result=MockCOM())

    step = Step(mock_com)

    result = step.result

    assert result is not None


def test_step_next_step():

    mock_com = MockCOM(NextStep=MockCOM(Name="Next"))

    step = Step(mock_com)

    result = step.next_step

    assert result is not None


def test_step_previous_step():

    mock_com = MockCOM(PreviousStep=MockCOM(Name="Previous"))

    step = Step(mock_com)

    result = step.previous_step

    assert result is not None


def test_step_result_status_setter():

    mock_com = MockCOM()

    step = Step(mock_com)

    step.result_status = StepProperties.ResultStatus_Failed

    assert mock_com.ResultStatus == StepProperties.ResultStatus_Failed


def test_step_adapter_key_name():

    mock_com = MockCOM(AdapterKeyName="LabVIEW Adapter")

    step = Step(mock_com)

    assert step.adapter_key_name == "LabVIEW Adapter"


def test_step_adapter():

    mock_com = MockCOM(Adapter=MockCOM(KeyName="DLL"))

    step = Step(mock_com)

    result = step.adapter

    assert result is not None


def test_step_create_class_method():

    mock_engine = typing.cast(typing.Any, MagicMock())

    mock_engine._engine = typing.cast(typing.Any, MockCOM())

    mock_engine._engine.NewStep = lambda *_args: MockCOM()

    step = Step.create(mock_engine, "SequenceFile", "PassFail")

    assert step is not None
