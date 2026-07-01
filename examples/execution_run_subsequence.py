"""Build and run a sequence end-to-end using only built-in TestStand step types.

Creates a fresh in-memory sequence file, appends three Action steps to
MainSequence using the None adapter (no external code module), starts an
execution, waits for it to finish, and walks the resulting ResultList to
print the recorded step name and status for each step.

The example focuses on the execution + result reporting surface — no code
modules, no LabVIEW/DLL adapters — so it can be exercised on any TestStand
engine without external dependencies.
"""

from __future__ import annotations

from py_teststand import AdapterKeyName, Engine, ResultList, StepGroup


def main() -> None:
    with Engine() as engine:
        sequence_file = engine.new_sequence_file()
        main_sequence = sequence_file.get_sequence_by_name("MainSequence")

        for name in ("Initialize", "Run Test", "Cleanup"):
            step = engine.new_step(AdapterKeyName.NoneAdapterKeyName, "Action")
            step.name = name
            step.record_result = True
            main_sequence.insert_step(step, main_sequence.get_num_steps(), StepGroup.Main)

        with engine.new_execution(sequence_file, "MainSequence") as execution:
            execution.wait_for_end_ex(-1)

            results = execution.result_object
            if results is None:
                return

            with results as res:
                if not res.exists("ResultList", 0):
                    print("No results recorded.")
                    return

                result_list_obj = res.get_property_object("ResultList", 0)
                if result_list_obj is None:
                    return

                parsed_results = ResultList(result_list_obj._com_obj).parse()
                for result in parsed_results:
                    print(f"{result['name']}: {result['status']}")


if __name__ == "__main__":
    main()
