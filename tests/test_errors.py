"""Tests for error handling and input validation in unitcalc."""

import pytest
from unitcalc import convert, list_units, list_categories, add_unit, UnitCalcError


class TestConvertErrors:
    def test_convert_non_numeric_value_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="must be a number"):
            convert("ten", "meter", "kilometer")  # type: ignore[arg-type]

    def test_convert_none_value_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="must be a number"):
            convert(None, "meter", "kilometer")  # type: ignore[arg-type]

    def test_convert_nan_value_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="must be a finite number"):
            convert(float("nan"), "meter", "kilometer")

    def test_convert_inf_value_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="must be a finite number"):
            convert(float("inf"), "meter", "kilometer")

    def test_convert_negative_inf_value_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="must be a finite number"):
            convert(float("-inf"), "meter", "kilometer")

    def test_convert_unknown_from_unit_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="Unknown unit"):
            convert(1, "fathom", "meter")

    def test_convert_unknown_to_unit_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="Unknown unit"):
            convert(1, "meter", "fathom")

    def test_convert_incompatible_categories_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="incompatible"):
            convert(1, "meter", "kilogram")

    def test_convert_empty_from_unit_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="must be a non-empty string"):
            convert(1, "", "meter")

    def test_convert_empty_to_unit_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="must be a non-empty string"):
            convert(1, "meter", "")

    def test_convert_non_string_from_unit_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="must be a non-empty string"):
            convert(1, 123, "meter")  # type: ignore[arg-type]

    def test_convert_non_string_to_unit_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="must be a non-empty string"):
            convert(1, "meter", 123)  # type: ignore[arg-type]

    def test_convert_none_unit_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="must be a non-empty string"):
            convert(1, None, "meter")  # type: ignore[arg-type]

    def test_convert_length_to_time_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="incompatible"):
            convert(1, "kilometer", "second")

    def test_convert_mass_to_temperature_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="incompatible"):
            convert(1, "kilogram", "celsius")


class TestListUnitsErrors:
    def test_list_units_unknown_category_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="Unknown category"):
            list_units("electricity")

    def test_list_units_non_string_category_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="must be a string"):
            list_units(123)  # type: ignore[arg-type]

    def test_list_units_empty_category_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="must be a non-empty string"):
            list_units("")


class TestAddUnitErrors:
    def test_add_unit_empty_name_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="must be a non-empty string"):
            add_unit("length", "", lambda x: x, lambda x: x)

    def test_add_unit_non_string_name_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="must be a non-empty string"):
            add_unit("length", 123, lambda x: x, lambda x: x)  # type: ignore[arg-type]

    def test_add_unit_unknown_category_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="Unknown category"):
            add_unit("electricity", "volt", lambda x: x, lambda x: x)

    def test_add_unit_non_callable_to_base_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="must be callable"):
            add_unit("length", "newunit", "not_a_func", lambda x: x)  # type: ignore[arg-type]

    def test_add_unit_non_callable_from_base_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="must be callable"):
            add_unit("length", "newunit", lambda x: x, "not_a_func")  # type: ignore[arg-type]

    def test_add_unit_duplicate_name_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="already exists"):
            add_unit("length", "meter", lambda x: x, lambda x: x)

    def test_add_unit_empty_category_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="must be a non-empty string"):
            add_unit("", "newunit", lambda x: x, lambda x: x)

    def test_add_unit_non_string_category_raises(self) -> None:
        with pytest.raises(UnitCalcError, match="must be a non-empty string"):
            add_unit(42, "newunit", lambda x: x, lambda x: x)  # type: ignore[arg-type]
