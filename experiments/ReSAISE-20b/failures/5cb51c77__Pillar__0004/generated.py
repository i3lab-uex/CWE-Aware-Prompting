# SPDX-License-Identifier: MIT

"""
Vehicle data modification module.

This module defines a single function `modify_vehicle_data` that updates
vehicle attributes only if they are listed in the global `ALLOWED_FIELDS`
set. The function performs basic validation and returns a new dictionary
containing the updated values, leaving the original input untouched.

CWE-664 (Improper Control of a Resource Through its Lifetime) is mitigated
by ensuring that no external resources (files, network connections, etc.)
are opened or held beyond the scope of this function. The function operates
solely on in‑memory data structures, so no resource lifetime issues arise.
"""

from __future__ import annotations

ALLOWED_FIELDS = {
    "make",
    "model",
    "year",
    "color",
    "vin",
    "engine_type",
    "transmission",
}


def modify_vehicle_data(
    vehicle_info: dict[str, any], changes_to_apply: dict[str, any]
) -> dict[str, any]:
    """
    Return a new dictionary containing the vehicle data after applying
    allowed changes.

    Parameters
    ----------
    vehicle_info : dict[str, any]
        Original vehicle details.
    changes_to_apply : dict[str, any]
        Fields to update and their new values.

    Returns
    -------
    dict[str, any]
        Updated vehicle details.

    Raises
    ------
    ValueError
        If any key in `changes_to_apply` is not present in `ALLOWED_FIELDS`.
    TypeError
        If either argument is not a dictionary.
    """
    if not isinstance(vehicle_info, dict):
        raise TypeError("vehicle_info must be a dictionary")
    if not isinstance(changes_to_apply, dict):
        raise TypeError("changes_to_apply must be a dictionary")

    # Create a shallow copy to avoid mutating the original data.
    updated_info = vehicle_info.copy()

    for field, new_value in changes_to_apply.items():
        if field not in ALLOWED_FIELDS:
            raise ValueError(
                f"Field '{field}' is not allowed to be modified. "
                f"Allowed fields: {sorted(ALLOWED_FIELDS)}"
            )
        updated_info[field] = new_value

    return updated_info