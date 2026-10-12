# SPDX-License-Identifier: MIT
"""
Vehicle data modification module.

The function `modify_vehicle_data` updates only the fields that are explicitly
listed in the global `ALLOWED_FIELDS`. It returns a new dictionary containing
the updated data, leaving the original input unchanged to avoid unintended
side‑effects.  This design mitigates CWE‑664 by ensuring that resource (the
vehicle data dictionary) is only altered in a controlled manner.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Iterable


# List of attribute names that are permitted to be updated.
ALLOWED_FIELDS: Iterable[str] = (
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
)


def modify_vehicle_data(
    vehicle_info: Dict[str, Any], modifications: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Return a new dictionary representing the vehicle with authorized updates applied.

    Parameters
    ----------
    vehicle_info : dict
        The original vehicle data. Must be a mapping from string keys to values.
    modifications : dict
        Mapping of field names to new values that should be applied.

    Returns
    -------
    dict
        A copy of `vehicle_info` with the allowed fields updated.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If any key in `modifications` is not present in `ALLOWED_FIELDS`.
    """

    if not isinstance(vehicle_info, dict):
        raise TypeError("vehicle_info must be a dictionary")
    if not isinstance(modifications, dict):
        raise TypeError("modifications must be a dictionary")

    # Create a shallow copy to avoid mutating the original input.
    updated_vehicle = copy.deepcopy(vehicle_info)

    for field, new_value in modifications.items():
        if field not in ALLOWED_FIELDS:
            raise ValueError(
                f"Field '{field}' is not allowed to be modified. "
                f"Allowed fields: {sorted(ALLOWED_FIELDS)}"
            )
        updated_vehicle[field] = new_value

    return updated_vehicle