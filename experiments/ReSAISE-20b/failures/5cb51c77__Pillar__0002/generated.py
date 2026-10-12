# modify_vehicle_data.py

"""
Utility to safely update vehicle data dictionaries.

The function `modify_vehicle_data` updates only the fields specified in
the global list `ALLOWED_FIELDS`.  It validates inputs and raises a
`ValueError` if an attempt is made to modify disallowed fields or if
the input types are incorrect.

Security Note:
- The function performs a shallow copy of the vehicle data before
  applying changes to avoid side‑effects on the original dictionary.
- It does not perform deep validation of field values; callers should
  ensure that the new values are appropriate for their application.
"""

from __future__ import annotations

# Global list of fields that may be updated
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
]

def modify_vehicle_data(
    vehicle_info: dict,
    changes_to_apply: dict
) -> dict:
    """
    Update allowed fields in a vehicle information dictionary.

    Parameters
    ----------
    vehicle_info : dict
        Original vehicle data.  Must be a mapping of string keys to values.
    changes_to_apply : dict
        Mapping of field names to new values.  Only keys present in
        `ALLOWED_FIELDS` will be applied.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle data.  The input
        `vehicle_info` is not modified.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If `changes_to_apply` contains keys that are not in
        `ALLOWED_FIELDS`.
    """
    # Basic type checks
    if not isinstance(vehicle_info, dict):
        raise TypeError("vehicle_info must be a dictionary")
    if not isinstance(changes_to_apply, dict):
        raise TypeError("changes_to_apply must be a dictionary")

    # Detect disallowed fields
    invalid_keys = set(changes_to_apply) - set(ALLOWED_FIELDS)
    if invalid_keys:
        raise ValueError(
            f"Attempted to modify disallowed fields: {sorted(invalid_keys)}"
        )

    # Create a shallow copy to avoid mutating the original
    updated_info = vehicle_info.copy()

    # Apply changes
    for key, value in changes_to_apply.items():
        updated_info[key] = value

    return updated_info