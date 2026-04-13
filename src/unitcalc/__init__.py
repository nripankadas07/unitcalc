"""unitcalc — Simple unit conversion library for length, mass, temperature, and time."""

from unitcalc.core import convert, list_units, list_categories, add_unit
from unitcalc.errors import UnitCalcError

__all__ = ["convert", "list_units", "list_categories", "add_unit", "UnitCalcError"]
__version__ = "1.0.0"
