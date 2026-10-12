#!/usr/bin/env python3
"""
Safe vehicle information updater.

This module defines a single function, `update_vehicle_info`, which updates
a dictionary representing a vehicle with new values provided in an
`updates` mapping. Only attributes listed in the global `ALLOWED_FIELDS`
are permitted to be changed, protecting against CWE‑915: Improperly
Controlled Modification of Dynamically-Determined Object Attributes.
"""

from __future__ import annotations

from typing import Dict, Any, Iterable


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

#: Attributes that may be updated.  Add or remove fields as required.
ALLOWED_FIELDS: Iterable[str] = (
    "make",
    "model",
    "year",
    "owner",
    "registration",
)


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def update_vehicle_info(
    vehicle: Dict[str, Any], updates: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a vehicle dictionary with new values.

    Parameters
    ----------
    vehicle:
        The original vehicle data.  This dictionary will be modified in place.
    updates:
        Mapping of attribute names to new values.

    Returns
    -------
    dict
        The updated vehicle dictionary (the same object as ``vehicle``).

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If ``updates`` contains keys that are not in :data:`ALLOWED_FIELDS`.
    """
    # Basic type checks
    if not isinstance(vehicle, dict):
        raise TypeError(f"'vehicle' must be a dict; got {type(vehicle).__name__}")
    if not isinstance(updates, dict):
        raise TypeError(f"'updates' must be a dict; got {type(updates).__name__}")

    # Ensure no disallowed fields are being updated
    allowed_set = set(ALLOWED_FIELDS)
    for key in updates:
        if key not in allowed_set:
            raise ValueError(
                f"Attempt to update disallowed field '{key}'. "
                "Allowed fields are: "
                f"{', '.join(sorted(allowed_set))}"
            )

    # Apply updates
    vehicle.update(updates)
    return vehicle


# --------------------------------------------------------------------------- #
# Example usage (for testing only; remove or guard under __main__ in real use)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Sample vehicle
    car = {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2018,
        "owner": "Alice",
        "registration": "ABC123",
    }

    # Valid update
    try:
        updated_car = update_vehicle_info(car, {"year": 2020, "owner": "Bob"})
        print("Updated vehicle:", updated_car)
    except Exception as exc:
        print(f"Error: {exc}")

    # Attempt to modify a disallowed field
    try:
        update_vehicle_info(car, {"vin": "1HGCM82633A004352"})
    except Exception as exc:
        print(f"Error: {exc}")