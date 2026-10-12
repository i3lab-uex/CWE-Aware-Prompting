# -*- coding: utf-8 -*-
"""
Utility module for safely updating vehicle dictionaries.

The function `modify_car_details` updates only the attributes that are explicitly
listed in the global ``ALLOWED_FIELDS`` list.  Any attempt to modify a field
outside this whitelist will raise a ``KeyError``.
"""

from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Allowed fields that can be updated.  Add or remove entries as needed.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "mileage",
    "vin",           # Vehicle Identification Number
    "registration_state",
    "engine_type",
    "transmission",
]

# --------------------------------------------------------------------------- #
def modify_car_details(car: Dict[str, Any], changes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a vehicle dictionary with authorized changes.

    Parameters
    ----------
    car : dict
        Dictionary representing the vehicle.  It must contain at least the keys
        present in ``ALLOWED_FIELDS`` (though other keys are allowed and will be
        left untouched).
    changes : dict
        Dictionary of new values keyed by attribute name.  Only keys that exist in
        ``ALLOWED_FIELDS`` will be applied.

    Returns
    -------
    dict
        The same dictionary instance passed in, updated with the allowed changes.

    Raises
    ------
    TypeError
        If ``car`` or ``changes`` is not a dictionary.
    KeyError
        If any key in ``changes`` is not present in ``ALLOWED_FIELDS``.

    Notes
    -----
    - The function mutates the original ``car`` dictionary in place.
    - No attempt is made to validate data types or value ranges for the
      updated fields; callers should perform such validation if necessary.
    """
    # Defensive type checking
    if not isinstance(car, dict):
        raise TypeError(f"Expected 'car' to be a dict, got {type(car).__name__}")
    if not isinstance(changes, dict):
        raise TypeError(f"Expected 'changes' to be a dict, got {type(changes).__name__}")

    # Validate and apply changes
    for key, value in changes.items():
        if key not in ALLOWED_FIELDS:
            raise KeyError(f"Field '{key}' is not allowed to be modified.")
        car[key] = value

    return car