from __future__ import annotations

import typing

from py_teststand.property.property_object import PropertyObject
from py_teststand.sequence.sequence_context import SequenceContext

if typing.TYPE_CHECKING:
    pass


class ResultList:
    """Wrapper class for ResultList property, handling type casting automatically."""

    def __init__(self, obj: typing.Any) -> None:  # noqa: ANN401
        """Initialize with an Execution, SequenceContext, PropertyObject, or raw COM object."""
        self._target = obj

    def _walk(
        self, result_list: PropertyObject, parent_sequence: str = ""
    ) -> typing.Iterator[dict[str, typing.Any]]:
        """Walks a ResultList array and yields each step result as a dict.

        Args:
            result_list: A PropertyObject wrapping the ResultList array.
            parent_sequence: Name of the parent sequence for context.

        Yields:
            One dict per step result with name, type, status, value, limits, etc.
        """
        if not result_list.is_array:
            return

        num_elements = result_list.get_num_elements()
        for i in range(num_elements):
            step_result_object = result_list.get_property_object_by_offset(i, 0)
            if step_result_object is None:
                continue

            with step_result_object as result:
                try:
                    # TS.* standard result properties
                    name = (
                        result.get_val_string("TS.StepName")
                        if result.exists("TS.StepName")
                        else "Unknown"
                    )
                    step_type = (
                        result.get_val_string("TS.StepType") if result.exists("TS.StepType") else ""
                    )
                    status = result.get_val_string("Status") if result.exists("Status") else ""

                    # Error subproperty
                    error_msg = ""
                    error_code = 0
                    if result.exists("Error.Msg"):
                        error_msg = result.get_val_string("Error.Msg")
                    if result.exists("Error.Code"):
                        error_code = int(result.get_val_number("Error.Code"))

                    # Step-type-specific value (Numeric, String, or PassFail)
                    value: typing.Any = None
                    if result.exists("Numeric"):
                        value = result.get_val_number("Numeric")
                    elif result.exists("String"):
                        value = result.get_val_string("String")
                    elif result.exists("PassFail"):
                        value = result.get_val_boolean("PassFail")

                    # Limits subproperty
                    limits: dict[str, typing.Any] = {}
                    limits_path = ""
                    if result.exists("Limits"):
                        limits_path = "Limits"
                    elif result.exists("RawLimits"):
                        limits_path = "RawLimits"

                    if limits_path:
                        limits_object = result.get_property_object(limits_path)
                        if limits_object is not None:
                            with limits_object as limits_properties:
                                if limits_properties.exists("Low"):
                                    limits["low"] = limits_properties.get_val_number("Low")
                                if limits_properties.exists("High"):
                                    limits["high"] = limits_properties.get_val_number("High")
                                if limits_properties.exists("String"):
                                    limits["string"] = limits_properties.get_val_string("String")

                    # Measurement array (MultipleNumericLimitTest)
                    measurements: list[dict[str, typing.Any]] = []
                    if result.exists("Measurement"):
                        measurement_array = result.get_property_object("Measurement")
                        if measurement_array is not None and measurement_array.is_array:
                            for j in range(measurement_array.get_num_elements()):
                                measurement_item = measurement_array.get_property_object_by_offset(
                                    j
                                )
                                if measurement_item is not None:
                                    with measurement_item as measurement_properties:
                                        has_val = measurement_properties.exists("Measurement")
                                        measurement_value = (
                                            measurement_properties.get_val_number("Measurement")
                                            if has_val
                                            else None
                                        )
                                        has_status = measurement_properties.exists("Status")
                                        measurement_status = (
                                            measurement_properties.get_val_string("Status")
                                            if has_status
                                            else ""
                                        )
                                        measurements.append(
                                            {
                                                "value": measurement_value,
                                                "status": measurement_status,
                                            }
                                        )

                    # Nested subsequence ResultList
                    has_nested = False
                    nested_list = None
                    nested_sequence_name = name

                    if result.exists("TS.SequenceCall.ResultList"):
                        has_nested = True
                        nested_list = result.get_property_object("TS.SequenceCall.ResultList")
                        if result.exists("TS.SequenceCall.Sequence"):
                            nested_sequence_name = result.get_val_string("TS.SequenceCall.Sequence")
                    elif result.exists("ResultList"):
                        has_nested = True
                        nested_list = result.get_property_object("ResultList")

                except Exception as e:
                    # Catch COM errors so a single bad element doesn't kill the loop
                    name = "Unknown (Parser Error)"
                    step_type = "Error"
                    status = "Error"
                    value = None
                    limits = {}
                    measurements = []
                    has_nested = False
                    nested_list = None
                    nested_sequence_name = ""
                    error_msg = f"Failed to parse result properties: {e}"
                    error_code = -1

                yield {
                    "name": name,
                    "type": step_type,
                    "status": status,
                    "value": value,
                    "limits": limits if limits else None,
                    "measurements": measurements if measurements else None,
                    "error_msg": error_msg,
                    "error_code": error_code,
                    "parent_sequence": parent_sequence,
                    "is_sequence_call": has_nested,
                }

                if has_nested and nested_list is not None:
                    with nested_list as nested_results:
                        yield from self._walk(nested_results, parent_sequence=nested_sequence_name)

    def parse(self) -> list[dict[str, typing.Any]]:
        """Parses a ResultList from the wrapped object.

        Returns:
            A list of dictionaries representing the parsed step results.
        """
        from py_teststand.execution.execution import Execution
        from py_teststand.property.property_object import PropertyObject

        obj = self._target

        if isinstance(obj, Execution):
            result_object = obj.result_object
            if result_object is None or not result_object.exists("ResultList"):
                return []
            result_list = result_object.get_property_object("ResultList")
            if result_list is None:
                return []
            with result_list as rl:
                return list(self._walk(rl))

        if isinstance(obj, SequenceContext):
            result_list = None
            if obj.locals.exists("ResultList"):
                result_list = obj.locals.get_property_object("ResultList")
            elif obj.parameters.exists("ResultList"):
                result_list = obj.parameters.get_property_object("ResultList")

            if result_list is None:
                return []

            sequence_name = ""
            try:
                if obj.sequence:
                    sequence_name = obj.sequence.name
            except Exception:
                pass

            with result_list as rl:
                return list(self._walk(rl, parent_sequence=sequence_name))

        if isinstance(obj, PropertyObject):
            return list(self._walk(obj))

        # Raw COM objects / Mocks
        com_obj = obj
        is_mock = "mock" in type(com_obj).__name__.lower() or hasattr(com_obj, "_mock_self")
        if not is_mock:
            if hasattr(com_obj, "ResultObject"):
                return ResultList(Execution(com_obj)).parse()
            if hasattr(com_obj, "Locals") and hasattr(com_obj, "Parameters"):
                return ResultList(SequenceContext(com_obj)).parse()

        with PropertyObject(com_obj) as po:
            return list(self._walk(po))
