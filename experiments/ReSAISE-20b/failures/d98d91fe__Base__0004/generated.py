# -*- coding: utf-8 -*-

"""
Utility module for safely updating vehicle dictionaries.
"""

from typing import Dict, Any

# Global list of fields that are permitted to be modified
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "mileage",
    "engine_type",
    "transmission",
]

class FieldNotAllowedError(ValueError):
    """Raised when an attempt is made to modify a disallowed field."""
    pass

def modify_car_details(car: Dict[str, Any], changes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update only the attributes of a vehicle that are explicitly allowed.

    Parameters
    ----------
    car : dict
        Dictionary representing the vehicle. The dictionary is modified in-place.
    changes : dict
        Mapping of attribute names to their new values.

    Returns
    -------
    dict
        The same dictionary object, now updated with the allowed changes.

    Raises
    ------
    TypeError
        If either ``car`` or ``changes`` is not a dictionary.
    FieldNotAllowedError
        If any key in ``changes`` is not present in :data:`ALLOWED_FIELDS`.
    """
    if not isinstance(car, dict):
        raise TypeError(f"'car' must be a dictionary; got {type(car).__name__}")
    if not isinstance(changes, dict):
        raise TypeError(f"'changes' must be a dictionary; got {type(changes).__name__}")

    disallowed = set(changes) - set(ALLOWED_FIELDS)
    if disallowed:
        raise FieldNotAllowedError(
            f"The following fields are not allowed to be modified: {sorted(disallowed)}"
        )

    for key, value in changes.items():
        car[key] = value

    return car