"""Run real pass/fail tests headless and read their numeric results.

The other execution example (execution_run_subsequence.py) runs Action steps that only
report a status. This one runs actual NumericLimitTest steps that produce a
measurement and pass or fail against limits, which is the usual headless goal:
drive a sequence with no UI and read back per-step pass/fail plus the number.

Two things make a test step runnable without a code module:

- Build it with the None adapter (AdapterKeyName.NoneAdapterKeyName). A step built
  with an empty adapter key expects a module and raises "module has not yet been
  specified" when you try to execute it.
- Set the step's DataSource expression, which is where the step reads its
  measurement from. It defaults to "Step.Result.Numeric" (0 with no code module),
  so set it to the expression that yields your measurement. Here a literal stands
  in for what a real instrument read would return.

The step then compares the measured value against Limits.Low / Limits.High and
records Passed or Failed, which we read from each entry in the ResultList.
"""

from __future__ import annotations

from py_teststand import AdapterKeyName, Engine, StepGroup

# (name, measurement expression, low limit, high limit)
TESTS = [
    ("Supply Voltage", "5.0", 4.75, 5.25),
    ("Bias Current", "9.0", 1.0, 8.0),
]


def _add_numeric_limit_test(engine, sequence, name, data_source, low, high):
    """Append a runnable NumericLimitTest to a sequence's Main step group."""
    step = engine.new_step(AdapterKeyName.NoneAdapterKeyName, "NumericLimitTest")
    step.name = name
    step.record_result = True
    step_data = step.as_property_object()
    step_data["DataSource"] = data_source
    step_data["Limits.Low"] = low
    step_data["Limits.High"] = high
    sequence.insert_step(step, sequence.get_num_steps(), StepGroup.Main)


def main() -> None:
    with Engine() as engine:
        sequence_file = engine.new_sequence_file()
        main_sequence = sequence_file.get_sequence_by_name("MainSequence")

        for name, data_source, low, high in TESTS:
            _add_numeric_limit_test(engine, main_sequence, name, data_source, low, high)

        with engine.new_execution(sequence_file, "MainSequence") as execution:
            execution.wait_for_end_ex(-1)

            result_list = execution.result_object.get_property_object("ResultList", 0)
            if result_list is None:
                print("No results recorded.")
                return

            all_passed = True
            with result_list as results:
                for step_result in results:
                    with step_result as result:
                        name = result.get_val_string("TS.StepName", 0)
                        status = result.get_val_string("Status", 0)
                        numeric = result.get_val_number("Numeric", 0)
                        print(f"  {name}: {status} (measured {numeric})")
                        all_passed = all_passed and status == "Passed"

        print(f"\nOverall: {'PASSED' if all_passed else 'FAILED'}")


if __name__ == "__main__":
    main()
