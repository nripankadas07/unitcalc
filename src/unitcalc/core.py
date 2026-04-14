"""Core conversion engine for unitcalc.

Each unit is registered as a pair of functions: to_base (converts the unit's
value to the category's base unit) and from_base (converts the base unit's
value to this unit). Temperature uses Kelvin as the base; length uses meter;
mass uses kilogram; time uses second.
"""

from __future__ import annotations

import math
from typing import Callable, Optional

from unitcalc.errors import UnitCalcError

# Type alias for a conversion pair: (to_base, from_base)
_ConvPair = tuple[Callable[[float], float], Callable[[float], float]]

# ââ Registry âââââââââââââââââââââââââââââââââââââââââââââââââââââââ

_registry: dict[str, dict[str, _ConvPair]] = {
    "length": {},
    "mass": {},
    "temperature": {},
    "time": {},
}

# Reverse lookup: unit name â category
_unit_to_category: dict[str, str] = {}


def _register(category: str, name: str, to_base: Callable[[float], float],
              from_base: Callable[[float], float]) -> None:
    """Register a built-in unit at module load time."""
    _registry[category][name] = (to_base, from_base)
    _unit_to_category[name] = category


# ââ Built-in units âââââââââââââââââââââââââââââââââââââââââââââââââ

# Length (base: meter)
_register("length", "meter",      lambda v: v,             lambda v: v)
_register("length", "kilometer",  lambda v: v * 1000.0,    lambda v: v / 1000.0)
_register("length", "centimeter", lambda v: v / 100.0,     lambda v: v * 100.0)
_register("length", "millimeter", lambda v: v / 1000.0,    lambda v: v * 1000.0)
_register("length", "mile",       lambda v: v * 1609.344,  lambda v: v / 1609.344)
_register("length", "yard",       lambda v: v * 0.9144,    lambda v: v / 0.9144)
_register("length", "foot",       lambda v: v * 0.3048,    lambda v: v / 0.3048)
_register("length", "inch",       lambda v: v * 0.0254,    lambda v: v / 0.0254)

# Mass (base: kilogram)
_register("mass", "kilogram",  lambda v: v,                lambda v: v)
_register("mass", "gram",      lambda v: v / 1000.0,       lambda v: v * 1000.0)
_register("mass", "milligram", lambda v: v / 1_000_000.0,  lambda v: v * 1_000_000.0)
_register("mass", "pound",     lambda v: v * 0.45359237,   lambda v: v / 0.45359237)
_register("mass", "ounce",     lambda v: v * 0.028349523125, lambda v: v / 0.028349523125)
_register("mass", "ton",       lambda v: v * 1000.0,       lambda v: v / 1000.0)

# Temperature (base: kelvin)
_register("temperature", "kelvin",     lambda v: v,                        lambda v: v)
_register("temperature", "celsius",    lambda v: v + 273.15,               lambda v: v - 273.15)
_register("temperature", "fahrenheit", lambda v: (v - 32) * 5 / 9 + 273.15,
                                       lambda v: (v - 273.15) * 9 / 5 + 32)

# Time (base: second)
_register("time", "second",      lambda v: v,              lambda v: v)
_register("time", "millisecond", lambda v: v / 1000.0,     lambda v: v * 1000.0)
_register("time", "minute",      lambda v: v * 60.0,       lambda v: v / 60.0)
_register("time", "hour",        lambda v: v * 3600.0,     lambda v: v / 3600.0)
_register("time", "day",         lambda v: v * 86400.0,    lambda v: v / 86400.0)
_register("time", "week",        lambda v: v * 604800.0,   lambda v: v / 604800.0)


# ââ Validation helpers âââââââââââââââââââââââââââââââââââââââââââââ

def _validate_unit_name(name: object, label: str) -> str:
    """Ensure *name* is a non-empty string and return it."""
    if not isinstance(name, str) or not name:
        raise UnitCalcError(f"{label} must be a non-empty string, got {name!r}")
    return name


def _validate_value(value: object) -> float:
    """Ensure *value* is a finite number and return it as float."""
    if not isinstance(value, (int, float)):
        raise UnitCalcError(f"value must be a number, got {type(value).__name__}")
    fval = float(value)
    if math.isnan(fval) or math.isinf(fval):
        raise UnitCalcError("value must be a finite number")
    return fval


def _lookup_unit(name: str) -> tuple[str, _ConvPair]:
    """Return (category, conversion_pair) for a known unit name."""
    category = _unit_to_category.get(name)
    if category is None:
        raise UnitCalcError(f"Unknown unit: {name!r}")
    return category, _registry[category][name]


# ââ Public API âââââââââââââââââââââââââââââââââââââââââââââââââââââ

def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convert *value* from *from_unit* to *to_unit*.

    Both units must belong to the same category (length, mass, temperature,
    or time). Raises ``UnitCalcError`` for invalid inputs.
    """
    fval = _validate_value(value)
    from_name = _validate_unit_name(from_unit, "from_unit")
    to_name = _validate_unit_name(to_unit, "to_unit")

    from_cat, (to_base_fn, _) = _lookup_unit(from_name)
    to_cat, (_, from_base_fn) = _lookup_unit(to_name)

    if from_cat != to_cat:
        raise UnitCalcError(
            f"Cannot convert between incompatible categories: "
            f"{from_cat} and {to_cat}"
        )

    base_value = to_base_fn(fval)
    return from_base_fn(base_value)


def list_units(category: Optional[str] = None) -> list[str]:
    """Return a sorted list of available unit names.

    If *category* is given, only units in that category are returned.
    If *category* is ``None``, all units across all categories are returned.
    """
    if category is None:
        return sorted(_unit_to_category.keys())

    if not isinstance(category, str):
        raise UnitCalcError(f"category must be a string, got {type(category).__name__}")
    if not category:
        raise UnitCalcError("category must be a non-empty string")
    if category not in _registry:
        raise UnitCalcError(f"Unknown category: {category!r}")

    return sorted(_registry[category].keys())


def list_categories() -> list[str]:
    """Return a sorted list of all unit categories."""
    return sorted(_registry.keys())


def add_unit(category: str, name: str,
             to_base: Callable[[float], float],
             from_base: Callable[[float], float]) -> None:
    """Register a custom unit in an existing category.

    *to_base* converts a value in the new unit to the category's base unit.
    *from_base* converts a base-unit value back to the new unit.
    """
    cat = _validate_unit_name(category, "category")
    unit_name = _validate_unit_name(name, "name")

    if cat not in _registry:
        raise UnitCalcError(f"Unknown category: {cat!r}")
    if unit_name in _unit_to_category:
        raise UnitCalcError(f"Unit {unit_name!r} already exists in category {_unit_to_category[unit_name]!r}")
    if not callable(to_base):
        raise UnitCalcError("to_base must be callable")
    if not callable(from_base):
        raise UnitCalcError("from_base must be callable")

    _registry[cat][unit_name] = (to_base, from_base)
    _unit_to_category[unit_name] = cat
