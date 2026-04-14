"""Custom exception types for unitcalc."""


class UnitCalcError(ValueError):
    """Raised when a unit conversion cannot be performed.

    Covers unknown units, incompatible categories, and invalid input values.
    """
