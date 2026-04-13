# unitcalc

Simple, zero-dependency unit conversion library for length, mass, temperature, and time.

## Installation

```bash
pip install unitcalc
```

Or install from source:

```bash
git clone https://github.com/nripankadas07/unitcalc.git
cd unitcalc
pip install .
```

## Usage

```python
from unitcalc import convert, list_units, list_categories, add_unit

# Basic conversions
convert(1000, "meter", "kilometer")       # 1.0
convert(1, "mile", "kilometer")           # 1.609344
convert(100, "celsius", "fahrenheit")     # 212.0
convert(1, "hour", "second")              # 3600.0
convert(2.5, "kilogram", "pound")         # 5.511...

# List available units and categories
list_categories()                          # ['length', 'mass', 'temperature', 'time']
list_units("length")                       # ['centimeter', 'foot', 'inch', ...]
list_units()                               # all units across all categories

# Register a custom unit
add_unit(
    "length",
    "nautical_mile",
    to_base=lambda v: v * 1852.0,       # to meters
    from_base=lambda v: v / 1852.0,     # from meters
)
convert(1, "nautical_mile", "kilometer")  # 1.852
```

## API Reference

### `convert(value, from_unit, to_unit) -> float`

Convert a numeric value between two units in the same category.

**Parameters:**
- `value` (`int | float`) â The value to convert. Must be finite.
- `from_unit` (`str`) â Source unit name (e.g., `"meter"`, `"celsius"`).
- `to_unit` (`str`) â Target unit name.

**Returns:** The converted value as a `float`.

**Raises:** `UnitCalcError` if the value is non-numeric/non-finite, units are unknown, or units belong to different categories.

### `list_units(category=None) -> list[str]`

Return a sorted list of available unit names.

**Parameters:**
- `category` (`str | None`) â If provided, filter to units in that category. If `None`, return all units.

**Returns:** A sorted list of unit name strings.

**Raises:** `UnitCalcError` if the category is unknown.

### `list_categories() -> list[str]`

Return a sorted list of all unit categories: `["length", "mass", "temperature", "time"]`.

### `add_unit(category, name, to_base, from_base) -> None`

Register a custom unit in an existing category.

**Parameters:**
- `category` (`str`) â One of `"length"`, `"mass"`, `"temperature"`, `"time"`.
- `name` (`str`) â The name for the new unit (must be unique across all categories).
- `to_base` (`Callable[[float], float]`) â Converts a value in the new unit to the category's base unit (meter, kilogram, kelvin, or second).
- `from_base` (`Callable[[float], float]`) â Converts a base-unit value back to the new unit.

**Raises:** `UnitCalcError` if the category is unknown, the name already exists, or the callbacks are not callable.

### `UnitCalcError`

Exception class (subclass of `ValueError`) raised for all unitcalc errors: unknown units, incompatible categories, invalid inputs.

## Built-in Units

| Category    | Base Unit  | Units                                                        |
|-------------|------------|--------------------------------------------------------------|
| length      | meter      | meter, kilometer, centimeter, millimeter, mile, yard, foot, inch |
| mass        | kilogram   | kilogram, gram, milligram, pound, ounce, ton                 |
| temperature | kelvin     | kelvin, celsius, fahrenheit                                  |
| time        | second     | second, millisecond, minute, hour, day, week                 |

## Running Tests

```bash
pip install pytest pytest-cov
pytest tests/ -v --cov=unitcalc --cov-report=term-missing
```

## License

MIT
# unitcalc
Simple, zero-dependency unit conversion library forlength, mass, temperature, and time
