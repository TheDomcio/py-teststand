"""Integration tests for result_list parsing using the live engine."""

from __future__ import annotations

from py_teststand import AdapterKeyName, Engine, ResultList, StepGroup


def test_result_list_parser_on_live_engine() -> None:
    """Creates a sequence with all three major step types, runs it, and parses results."""
    with Engine() as engine:
        sequence_file = engine.new_sequence_file()
        main_sequence = sequence_file.get_sequence_by_name("MainSequence")

        # Step 1: Pass/Fail Test
        step1 = engine.new_step(AdapterKeyName.NoneAdapterKeyName, "PassFailTest")
        step1.name = "Verify Power Rail"
        step1.record_result = True
        step1.as_property_object()["DataSource"] = "True"
        main_sequence.insert_step(step1, 0, StepGroup.Main)

        # Step 2: Numeric Limit Test
        step2 = engine.new_step(AdapterKeyName.NoneAdapterKeyName, "NumericLimitTest")
        step2.name = "Verify Current Draw"
        step2.record_result = True
        step2_props = step2.as_property_object()
        step2_props["DataSource"] = "1.5"
        step2_props["Limits.Low"] = 1.0
        step2_props["Limits.High"] = 2.0
        main_sequence.insert_step(step2, 1, StepGroup.Main)

        # Step 3: String Value Test
        step3 = engine.new_step(AdapterKeyName.NoneAdapterKeyName, "StringValueTest")
        step3.name = "Verify Serial Number"
        step3.record_result = True
        step3_props = step3.as_property_object()
        step3_props["DataSource"] = '"SN-12345"'
        step3_props["Limits.String"] = "SN-12345"
        step3_props["Comp"] = "IgnoreCase"
        main_sequence.insert_step(step3, 2, StepGroup.Main)

        with engine.new_execution(sequence_file, "MainSequence") as execution:
            execution.wait_for_end_ex(-1)

            results_obj = execution.result_object
            assert results_obj is not None
            assert results_obj.exists("ResultList", 0)

            result_list_prop = results_obj.get_property_object("ResultList", 0)
            assert result_list_prop is not None

            # Parse results
            parsed_results = ResultList(result_list_prop._com_obj).parse()

            # Assert we got 3 steps
            assert len(parsed_results) == 3

            # Check Pass/Fail Test
            assert parsed_results[0]["name"] == "Verify Power Rail"
            assert parsed_results[0]["type"] == "PassFailTest"
            assert parsed_results[0]["status"] == "Passed"
            assert parsed_results[0]["value"] is True

            # Check Numeric Limit Test
            assert parsed_results[1]["name"] == "Verify Current Draw"
            assert parsed_results[1]["type"] == "NumericLimitTest"
            assert parsed_results[1]["status"] == "Passed"
            assert parsed_results[1]["value"] == 1.5
            assert parsed_results[1]["limits"]["low"] == 1.0
            assert parsed_results[1]["limits"]["high"] == 2.0

            # Check String Value Test
            assert parsed_results[2]["name"] == "Verify Serial Number"
            assert parsed_results[2]["type"] == "StringValueTest"
            assert parsed_results[2]["status"] == "Passed"
            assert parsed_results[2]["value"] == "SN-12345"
            assert parsed_results[2]["limits"] is None
