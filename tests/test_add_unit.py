"""Tests for the add_unit() custom unit registration function."""

import pytest
from unitcalc import convert, list_units, add_unit, UnitCalcError
from unitcalc.core import _registry, _unit_to_category

_TEST_UNITS = ("nautical_mile", "stone", "microkelvin")


class TestAddUnit:
    def setup_method(self) -> None:
        """Remove test units added during previous tests."""
        for category in _registry:
            _registry[category] = {
                name: funcs
                for name, funcs in _registry[category].items()
                if name not in _TEST_UNITS
            }
        for name in _TEST_UNITS:
            _unit_to_category.pop(name, None)

    def test_add_custom_length_unit_and_convert(self) -> None:
        add_unit(
            "length",
            "nautical_mile",
            to_base=lambda x: x * 1852.0,
            from_base=lambda x: x / 1852.0,
        )
        result = convert(1, "nautical_mile", "meter")
        assert result == pytest.approx(1852.0)

    def test_add_custom_unit_appears_in_list(self) -> None:
        add_unit(
            "length",
            "nautical_mile",
            to_base=lambda x: x * 1852.0,
            from_base=lambda x: x / 1852.0,
        )
        units = list_units("length")
        assert "nautical_mile" in units

    def test_add_custom_mass_unit(self) -> None:
        add_unit(
            "mass",
            "stone",
            to_base=lambda x: x * 6.35029,
            from_base=lambda x: x / 6.35029,
        )
        result = convert(1, "stone", "kilogram")
        assert result == pytest.approx(6.35029)

    def test_convert_to_custom_unit(self) -> None:
        add_unit(
            "length",
            "nautical_mile",
            to_base=lambda x: x * 1852.0,
            from_base=lambda x: x / 1852.0,
        )
        result = convert(1852, "meter", "nautical_mile")
        assert result == pytest.approx(1.0)

    def test_convert_between_custom_and_builtin(self) -> None:
        add_unit(
            "length",
            "nautical_mile",
            to_base=lambda x: x * 1852.0,
            from_base=lambda x: x / 1852.0,
        )
        result = convert(1, "nautical_mile", "kilometer")
        assert result == pytest.approx(1.852)
