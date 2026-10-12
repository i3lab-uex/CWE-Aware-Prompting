# -*- coding: utf-8 -*-
"""
Vehicle data modification utility.

The module defines a single public function `modify_vehicle_data` that safely updates
attributes of a vehicle dictionary. Only attributes listed in the global
`ALLOWED_FIELDS` constant may be modified; attempts to modify any other field raise a
`ValueError`.

This implementation guards against the CWE‑915 vulnerability (improperly controlled
modification of dynamically‑determined object attributes) by performing explicit
whitelisting of mutable keys and rejecting any other modification requests.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global whitelist of fields that are permitted to be modified.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "engine_type",
    "transmission",
    # Add additional allowed fields here as needed.
]

# --------------------------------------------------------------------------- #
def modify_vehicle_data(vehicle_info: dict, modifications: dict) -> dict:
    """
    Safely update a vehicle dictionary with provided modifications.

    Parameters
    ----------
    vehicle_info : dict
        The original vehicle data.  Keys should be strings and values can be any JSON‑serializable
        type.
    modifications : dict
        Mapping of attribute names to new values that should be applied to `vehicle_info`.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle data.  The original `vehicle_info`
        dictionary is not modified.

    Raises
    ------
    ValueError
        If any key in `modifications` is not present in the global ``ALLOWED_FIELDS`` list.
    TypeError
        If either `vehicle_info` or `modifications` is not a dictionary.
    """
    # Basic type checks
    if not isinstance(vehicle_info, dict):
        raise TypeError(f"vehicle_info must be a dict, got {type(vehicle_info).__name__}")
    if not isinstance(modifications, dict):
        raise TypeError(f"modifications must be a dict, got {type(modifications).__name__}")

    # Verify that all requested modifications are allowed
    for field in modifications:
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Modification of '{field}' is not permitted")

    # Create a shallow copy to avoid mutating the original
    updated_vehicle = vehicle_info.copy()

    # Apply each allowed modification
    for field, new_value in modifications.items():
        updated_vehicle[field] = new_value

    return updated_vehicle


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage and simple sanity check
    sample_vehicle = {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2018,
        "color": "Blue",
        "vin": "JTDBU4EE9B9123456",
        "mileage": 45000,
    }

    changes = {"color": "Red", "year": 2020}
    updated = modify_vehicle_data(sample_vehicle, changes)
    print("Original:", sample_vehicle)
    print("Updated :", updated)

    # Attempting to modify a disallowed field should raise an error
    try:
        modify_vehicle_data(sample_vehicle, {"owner": "Alice"})
    except ValueError as exc:
        print("Caught expected error:", exc)