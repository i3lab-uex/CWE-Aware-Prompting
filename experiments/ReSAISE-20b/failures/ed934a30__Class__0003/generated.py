#!/usr/bin/env python3
"""
Vehicle attribute updater.

The function ``alter_vehicle_info`` updates a vehicle's attributes only if the
attribute names are present in the global ``ALLOWED_FIELDS`` list.  The update
is performed on a copy of the input dictionary so that the caller's data is
not mutated.  A ``ValueError`` is raised if any key in *modifications* is not
allowed.

This implementation follows the CWE‑913 guidance by explicitly limiting
which keys may be modified, preventing arbitrary code or data from being
altered.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global configuration – fields that may be changed by ``alter_vehicle_info``.
# The list can be extended or modified as needed; only these keys will be
# accepted for update.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
]

# --------------------------------------------------------------------------- #
def alter_vehicle_info(details: dict, modifications: dict) -> dict:
    """
    Update vehicle attributes in *details* with values from *modifications*
    but only for keys that are present in ``ALLOWED_FIELDS``.

    Parameters
    ----------
    details : dict
        Current vehicle attributes.
    modifications : dict
        Proposed updates to the vehicle.

    Returns
    -------
    dict
        A new dictionary containing the updated attributes.

    Raises
    ------
    TypeError
        If either *details* or *modifications* is not a dictionary.
    ValueError
        If any key in *modifications* is not permitted by ``ALLOWED_FIELDS``.
    """
    if not isinstance(details, dict):
        raise TypeError(f"Expected 'details' to be a dict, got {type(details).__name__}")
    if not isinstance(modifications, dict):
        raise TypeError(f"Expected 'modifications' to be a dict, got {type(modifications).__name__}")

    # Detect disallowed keys early
    disallowed = [k for k in modifications if k not in ALLOWED_FIELDS]
    if disallowed:
        raise ValueError(f"Attempted to modify disallowed fields: {', '.join(disallowed)}")

    # Work on a shallow copy to avoid mutating the caller's data
    updated = details.copy()
    updated.update(modifications)
    return updated

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Simple demonstration
    vehicle = {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2018,
        "color": "red",
        "vin": "1NXBR32E73Z123456",
        "mileage": 45000,
    }

    changes = {"color": "blue", "year": 2019}
    try:
        new_vehicle = alter_vehicle_info(vehicle, changes)
        print("Updated vehicle:", new_vehicle)
    except Exception as exc:
        print(f"Error: {exc}")