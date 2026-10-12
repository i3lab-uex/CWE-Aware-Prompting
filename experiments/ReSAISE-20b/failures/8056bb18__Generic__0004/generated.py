# -*- coding: utf-8 -*-

"""
Utility to update vehicle information while enforcing allowed fields.
"""

from typing import Dict, Any

# Global list of fields that are permitted to be modified
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "owner",
]

def modify_vehicle_data(
    vehicle_info: Dict[str, Any], modifications: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a vehicle dictionary with new values for permitted fields.

    Parameters
    ----------
    vehicle_info : dict
        Dictionary containing the current state of a vehicle.
    modifications : dict
        Dictionary mapping field names to new values that should be applied.

    Returns
    -------
    dict
        The updated vehicle dictionary.

    Raises
    ------
    ValueError
        If any key in ``modifications`` is not present in :data:`ALLOWED_FIELDS`.

    Notes
    -----
    The function mutates ``vehicle_info`` in place and also returns the same object
    for convenience.  This design keeps behaviour predictable while allowing
    callers to ignore the return value if they prefer.
    """
    # Validate that all requested fields are allowed
    invalid_fields = [k for k in modifications if k not in ALLOWED_FIELDS]
    if invalid_fields:
        raise ValueError(
            f"Attempted to modify disallowed fields: {', '.join(invalid_fields)}"
        )

    # Apply allowed modifications
    for field, new_value in modifications.items():
        vehicle_info[field] = new_value

    return vehicle_info