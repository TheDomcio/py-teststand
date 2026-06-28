"""Walk and parse execution results into Python dictionaries.

Builds a sequence with test steps, runs it, then shows two ways to
retrieve the parsed ResultList:

1. Object-oriented approach via execution.result_list.
2. Passing a raw COM/PropertyObject ResultList directly to ResultList().
"""

from __future__ import annotations

import json

from py_teststand import (
    AdapterKeyName,
    Engine,
    ResultList,
    StepGroup,
)


def main() -> None:
    with Engine() as engine:
        sequence_file = engine.new_sequence_file()
        main_sequence = sequence_file.get_sequence_by_name("MainSequence")

        # Pass/Fail Test — forces pass
        step1 = engine.new_step(AdapterKeyName.NoneAdapterKeyName, "PassFailTest")
        step1.name = "Verify Power Rail"
        step1.record_result = True
        step1.as_property_object()["DataSource"] = "True"
        main_sequence.insert_step(step1, 0, StepGroup.Main)

        # Numeric Limit Test - forces 1.5 against 1.0-2.0 limits
        step2 = engine.new_step(AdapterKeyName.NoneAdapterKeyName, "NumericLimitTest")
        step2.name = "Verify Current Draw"
        step2.record_result = True
        step_properties = step2.as_property_object()
        step_properties["DataSource"] = "1.5"
        step_properties["Limits.Low"] = 1.0
        step_properties["Limits.High"] = 2.0
        main_sequence.insert_step(step2, 1, StepGroup.Main)

        # Execute the sequence
        print("Running sequence...")
        with engine.new_execution(sequence_file, "MainSequence") as execution:
            execution.wait_for_end_ex(-1)

            # Approach 1: Object-oriented approach (directly on Execution object)
            # The execution.result_list property automatically extracts and parses
            # the ResultList array internally.
            parsed_results = execution.result_list.parse()

            print("\nApproach 1 - execution.result_list:")
            for index, result in enumerate(parsed_results):
                print(
                    f"  [{index}] {result['name']} "
                    f"({result['type']}) -> {result['status']}, "
                    f"Value: {result['value']}"
                )

            # Approach 2: Universal helper class
            # You can also pass an Execution or SequenceContext
            # directly to ResultList().
            result_list = ResultList(execution).parse()

            print("\nApproach 2 - ResultList(execution).parse():")
            for index, result in enumerate(result_list):
                print(f"  [{index}] {result['name']} ({result['type']}) -> {result['status']}")
            print("\nSerialized JSON Report:")
            print(json.dumps(parsed_results, indent=4))


if __name__ == "__main__":
    main()
