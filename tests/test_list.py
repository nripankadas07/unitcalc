"""Tests for list_units() and list_categories() functions."""

import pytest
from unitcalc import list_units, list_categories


class TestListCategories:
    def test_list_categories_returns_all_four(self) -> None:
        categories = list_categories()
        assert set(categories) == {"length", "mass", "temperature", "time"}

    def test_list_categories_returns_sorted(self) -> None:
        categories = list_categories()
        assert categories == sorted(categories)

    def test_list_categories_returns_list(self) -> None:
        assert isinstance(list_categories(), list)


class TestListUnits:
    def test_list_units_length(self) -> None:
        units = list_units("length")
        assert "meter" in units
        assert "kilometer" in units
        assert "mile" in units
        assert "inch" in units
        assert "foot" in units
        assert "yard" in units
        assert "centimeter" in units
        assert "millimeter" in units

    def test_list_units_mass(self) -> None:
        units = list_units("mass")
        assert "kilogram" in units
        assert "gram" in units
        assert "pound" in units
        assert "ounce" in units
        assert "ton" in units
        assert "milligram" in units

    def test_list_units_temperature(self) -> None:
        units = list_units("temperature")
        assert "celsius" in units
        assert "fahrenheit" in units
        assert "kelvin" in units

    def test_list_units_time(self) -> None:
        units = list_units("time")
        assert "second" in units
        assert "minute" in units
        assert "hour" in units
        assert "day" in units
        assert "week" in units
        assert "millisecond" in units

    def test_list_units_none_returns_all(self) -> None:
        all_units = list_units()
        assert "meter" in all_units
        assert "kilogram" in all_units
        assert "celsius" in all_units
        assert "second" in all_units

    def test_list_units_returns_sorted(self) -> None:
        units = list_units("length")
        assert units == sorted(units)

    def test_list_units_returns_list_of_strings(self) -> None:
        units = list_units("mass")
        assert isinstance(units, list)
        assert all(isinstance(u, str) for u in units)
