# -*- coding: utf-8 -*-

"""
Vehicle data modification module.

This module defines a single function `modify_vehicle_data` which safely updates
vehicle information dictionaries. Only attributes listed in the global
`ALLOWED_FIELDS` list are permitted to be modified.

Security note: This implementation prevents CWE-915 by explicitly checking
that each requested field is in the allowed set before performing any update.
"""

from __future__ import annotations

# Global list of fields that are allowed to be modified
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "engine_type",
    "transmission",
    # Add more allowed fields as needed
]


def modify_vehicle_data(
    vehicle_info: dict,
    changes_to_apply: dict,
) -> dict:
    """
    Update a vehicle information dictionary with new values.

    Parameters
    ----------
    vehicle_info : dict
        The original vehicle data dictionary.
    changes_to_apply : dict
        A mapping of field names to new values that should be applied.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle data.

    Raises
    ------
    ValueError
        If `changes_to_apply` contains a field that is not in ALLOWED_FIELDS.
    TypeError
        If either argument is not a dictionary.

    Notes
    -----
    - The function does **not** modify the original `vehicle_info` dictionary;
      instead it returns a new updated copy.
    - The update is shallow: nested dictionaries or objects are not deeply
      merged. If a field in `changes_to_apply` is itself a dictionary, it
      will replace the old value entirely.
    """
    if not isinstance(vehicle_info, dict):
        raise TypeError("vehicle_info must be a dictionary")
    if not isinstance(changes_to_apply, dict):
        raise TypeError("changes_to_apply must be a dictionary")

    # Create a shallow copy to avoid mutating the original input
    updated_info = vehicle_info.copy()

    for field, new_value in changes_to_apply.items():
        if field not in ALLOWED_FIELDS:
            raise ValueError(
                f"Field '{field}' is not allowed to be modified. "
                f"Allowed fields: {ALLOWED_FIELDS}"
            )
        # Perform the update
        updated_info[field] = new_value

    return updated_info


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    original = {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2010,
        "color": "blue",
        "vin": "123456789ABCDEFG",
    }

    changes = {"color": "red", "year": 2012}
    updated = modify_vehicle_data(original, changes)
    print(updated)  # {'make': 'Toyota', ... , 'color': 'red', 'year': 2012}