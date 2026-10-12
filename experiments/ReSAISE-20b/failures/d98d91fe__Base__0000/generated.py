# -*- coding: utf-8 -*-
"""
Vehicle attribute updater.

The module defines a single public function `modify_car_details` that safely
updates only the attributes listed in the global ``ALLOWED_FIELDS`` list.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# List of attribute names that are permitted to be modified.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "engine_type",
    "transmission",
    # Add more fields as needed.
]

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def modify_car_details(car: dict, changes: dict) -> dict:
    """
    Safely update a vehicle dictionary with new values.

    Parameters
    ----------
    car : dict
        The original vehicle data.  It will be updated in place.
    changes : dict
        Mapping of attribute names to new values.

    Returns
    -------
    dict
        The updated vehicle dictionary (the same object as ``car``).

    Raises
    ------
    TypeError
        If ``car`` or ``changes`` is not a dictionary.
    ValueError
        If any key in ``changes`` is not listed in ``ALLOWED_FIELDS``.

    Notes
    -----
    This function guards against CWE-915 by ensuring that only attributes
    explicitly allowed in ``ALLOWED_FIELDS`` can be modified.  All other keys
    are rejected with a clear error message.
    """
    if not isinstance(car, dict):
        raise TypeError(f"Expected 'car' to be a dict; got {type(car).__name__}")
    if not isinstance(changes, dict):
        raise TypeError(f"Expected 'changes' to be a dict; got {type(changes).__name__}")

    allowed_set = set(ALLOWED_FIELDS)
    invalid_keys = [k for k in changes if k not in allowed_set]
    if invalid_keys:
        raise ValueError(
            f"The following fields are not permitted for modification: {', '.join(invalid_keys)}"
        )

    # Perform the updates
    car.update(changes)
    return car

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     vehicle = {"make": "Toyota", "model": "Corolla", "year": 2010}
#     updates = {"color": "red", "year": 2022}
#     print(modify_car_details(vehicle, updates))