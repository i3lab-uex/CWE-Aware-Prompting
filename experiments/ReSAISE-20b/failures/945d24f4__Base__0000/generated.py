#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A safe helper for updating vehicle details while preventing unauthorized field
modifications (CWE‑915).
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global list of fields that are allowed to be modified. Add or remove
# entries here as the domain evolves.
# --------------------------------------------------------------------------- #
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
]

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def update_car_information(
    car_details: dict[str, any],
    changes: dict[str, any]
) -> dict[str, any]:
    """
    Update specific fields of a vehicle's details.

    Parameters
    ----------
    car_details : dict[str, any]
        The original dictionary containing vehicle information.
    changes : dict[str, any]
        A mapping of field names to new values. Only keys that appear in
        :data:`ALLOWED_FIELDS` are applied.

    Returns
    -------
    dict[str, any]
        A new dictionary containing the updated vehicle information.

    Raises
    ------
    ValueError
        If ``changes`` contains a key that is not in :data:`ALLOWED_FIELDS`.

    Notes
    -----
    * The function returns a **new dictionary**; the original ``car_details``
      is left untouched.
    * This guard protects against CWE‑915 by ensuring that only
      explicitly whitelisted fields may be altered.
    """
    # Validate input types (helps prevent accidental misuse)
    if not isinstance(car_details, dict):
        raise TypeError("car_details must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Ensure no disallowed keys are present
    invalid_keys = set(changes) - set(ALLOWED_FIELDS)
    if invalid_keys:
        raise ValueError(
            f"The following fields are not allowed to be updated: {sorted(invalid_keys)}"
        )

    # Create a shallow copy to avoid mutating the caller's dict
    updated = car_details.copy()

    # Apply allowed changes
    for key, value in changes.items():
        updated[key] = value

    return updated

# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    original = {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2015,
        "color": "red",
        "vin": "123ABC456DEF",
        "mileage": 60000,
    }

    changes = {
        "color": "blue",
        "mileage": 65000,
    }

    try:
        new_details = update_car_information(original, changes)
        print("Updated car details:", new_details)
    except Exception as exc:
        print(f"Error: {exc}")