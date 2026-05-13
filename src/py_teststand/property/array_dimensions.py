from __future__ import annotations

from py_teststand.core.com_wrapper import COMWrapper, ts_interface


class ArrayDimensions(COMWrapper):
    @property
    @ts_interface
    def num_dimensions(self) -> int:
        return int(self._com_obj.NumDimensions)

    @ts_interface
    def get_lower_bounds(self) -> list[int]:
        return list(self._com_obj.GetLowerBounds())

    @ts_interface
    def get_upper_bounds(self) -> list[int]:
        return list(self._com_obj.GetUpperBounds())

    @ts_interface
    def set_bounds(self, lower_bounds: list[int], upper_bounds: list[int]) -> None:
        self._com_obj.SetBounds(lower_bounds, upper_bounds)

    @ts_interface
    def get_dimensions_sizes(self) -> list[int]:
        return list(self._com_obj.GetDimensionsSizes())

    @ts_interface
    def set_bounds_by_strings(self, lower_bounds: str, upper_bounds: str) -> None:
        self._com_obj.SetBoundsByStrings(lower_bounds, upper_bounds)

    @property
    @ts_interface
    def lower_bounds_string(self) -> str:
        return str(self._com_obj.LowerBoundsString)

    @property
    @ts_interface
    def upper_bounds_string(self) -> str:
        return str(self._com_obj.UpperBoundsString)

    @property
    @ts_interface
    def display_string(self) -> str:
        return str(self._com_obj.DisplayString)
