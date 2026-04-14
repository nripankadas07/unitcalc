"""Tests for the convert() function â happy paths and core behavior."""

import math
import pytest
from unitcalc import convert, UnitCalcError


# ââ Length conversions ââââââââââââââââââââââââââââââââââââââââââââââ

class TestLengthConversions:
    def test_convert_meter_to_kilometer(self) -> None:
        assert convert(1000, "meter", "kilometer") == pytest.approx(1.0)

    def test_convert_kilometer_to_meter(self) -> None:
        assert convert(1, "kilometer", "meter") == pytest.approx(1000.0)

    def test_convert_mile_to_kilometer(self) -> None:
        assert convert(1, "mile", "kilometer") == pytest.approx(1.609344)

    def test_convert_inch_to_centimeter(self) -> None:
        assert convert(1, "inch", "centimeter") == pytest.approx(2.54)

    def test_convert_foot_to_meter(self) -> None:
        assert convert(1, "foot", "meter") == pytest.approx(0.3048)

    def test_convert_yard_to_meter(self) -> None:
        assert convert(1, "yard", "meter") == pytest.approx(0.9144)

    def test_convert_millimeter_to_meter(self) -> None:
        assert convert(1000, "millimeter", "meter") == pytest.approx(1.0)


# ââ Mass conversions âââââââââââââââââââââââââââââââââââââââââââââââ

class TestMassConversions:
    def test_convert_kilogram_to_gram(self) -> None:
        assert convert(1, "kilogram", "gram") == pytest.approx(1000.0)

    def test_convert_pound_to_kilogram(self) -> None:
        assert convert(1, "pound", "kilogram") == pytest.approx(0.45359237)

    def test_convert_ounce_to_gram(self) -> None:
        assert convert(1, "ounce", "gram") == pytest.approx(28.349523125)

    def test_convert_ton_to_kilogram(self) -> None:
        assert convert(1, "ton", "kilogram") == pytest.approx(1000.0)

    def test_convert_milligram_to_gram(self) -> None:
        assert convert(1000, "milligram", "gram") == pytest.approx(1.0)


# ââ Temperature conversions ââââââââââââââââââââââââââââââââââââââââ

class TestTemperatureConversions:
    def test_convert_celsius_to_fahrenheit_freezing(self) -> None:
        assert convert(0, "celsius", "fahrenheit") == pytest.approx(32.0)

    def test_convert_celsius_to_fahrenheit_boiling(self) -> None:
        assert convert(100, "celsius", "fahrenheit") == pytest.approx(212.0)

    def test_convert_fahrenheit_to_celsius(self) -> None:
        assert convert(32, "fahrenheit", "celsius") == pytest.approx(0.0)

    def test_convert_celsius_to_kelvin(self) -> None:
        assert convert(0, "celsius", "kelvin") == pytest.approx(273.15)

    def test_convert_kelvin_to_celsius(self) -> None:
        assert convert(273.15, "kelvin", "celsius") == pytest.approx(0.0)

    def test_convert_fahrenheit_to_kelvin(self) -> None:
        assert convert(32, "fahrenheit", "kelvin") == pytest.approx(273.15)

    def test_convert_kelvin_to_fahrenheit(self) -> None:
        assert convert(273.15, "kelvin", "fahrenheit") == pytest.approx(32.0)

    def test_convert_negative_celsius(self) -> None:
        assert convert(-40, "celsius", "fahrenheit") == pytest.approx(-40.0)


# ââ Time conversions ââââââââââââââââââââââââââââââââââââââââââââââ

class TestTimeConversions:
    def test_convert_hour_to_minute(self) -> None:
        assert convert(1, "hour", "minute") == pytest.approx(60.0)

    def test_convert_minute_to_second(self) -> None:
        assert convert(1, "minute", "second") == pytest.approx(60.0)

    def test_convert_day_to_hour(self) -> None:
        assert convert(1, "day", "hour") == pytest.approx(24.0)

    def test_convert_week_to_day(self) -> None:
        assert convert(1, "week", "day") == pytest.approx(7.0)

    def test_convert_hour_to_second(self) -> None:
        assert convert(1, "hour", "second") == pytest.approx(3600.0)

    def test_convert_millisecond_to_second(self) -> None:
        assert convert(1000, "millisecond", "second") == pytest.approx(1.0)


# ââ Same-unit identity ââââââââââââââââââââââââââââââââââââââââââââ

class TestSameUnitConversion:
    def test_convert_same_unit_returns_same_value(self) -> None:
        assert convert(42.5, "meter", "meter") == pytest.approx(42.5)

    def test_convert_same_unit_celsius(self) -> None:
        assert convert(100, "celsius", "celsius") == pytest.approx(100.0)

    def test_convert_zero_value(self) -> None:
        assert convert(0, "kilogram", "gram") == pytest.approx(0.0)

    def test_convert_negative_value(self) -> None:
        assert convert(-5, "meter", "kilometer") == pytest.approx(-0.005)

    def test_convert_very_large_value(self) -> None:
        result = convert(1e15, "millimeter", "kilometer")
        assert result == pytest.approx(1e9)

    def test_convert_very_small_value(self) -> None:
        result = convert(1e-10, "kilometer", "millimeter")
        assert result == pytest.approx(1e-4)
