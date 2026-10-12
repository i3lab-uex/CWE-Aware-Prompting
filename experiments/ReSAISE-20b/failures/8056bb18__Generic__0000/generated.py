# -*- coding: utf-8 -*-
"""
Vehicle data modification utility.

This module defines a global list `ALLOWED_FIELDS` containing the keys that
are permitted to be updated in a vehicle dictionary.  The function
`modify_vehicle_data` applies authorized modifications and returns the
updated vehicle information.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any


# --------------------------------------------------------------------------- #
#  Global configuration
# --------------------------------------------------------------------------- #
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "engine_type",
    "transmission",
    "fuel_type",
    # Add more fields here as needed
]


# --------------------------------------------------------------------------- #
#  Core functionality
# --------------------------------------------------------------------------- #
def modify_vehicle_data(
    vehicle_info: Dict[str, Any],
    modifications: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a vehicle dictionary with only allowed fields.

    Parameters
    ----------
    vehicle_info : dict
        Original vehicle data.  Must be a mapping of attribute names to values.
    modifications : dict
        Dictionary containing new values for fields that should be updated.

    Returns
    -------
    dict
        A new dictionary containing the original data with authorized updates applied.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If any key in ``modifications`` is not present in :data:`ALLOWED_FIELDS`.

    Notes
    -----
    - The original ``vehicle_info`` is not modified; a deep copy is returned.
    - Keys in ``modifications`` that are not present in the original
      dictionary will be added to the returned result if they are allowed.
    """
    # Validate input types
    if not isinstance(vehicle_info, dict):
        raise TypeError("vehicle_info must be a dictionary")
    if not isinstance(modifications, dict):
        raise TypeError("modifications must be a dictionary")

    # Validate allowed fields
    unauthorized_keys = set(modifications) - set(ALLOWED_FIELDS)
    if unauthorized_keys:
        raise ValueError(
            f"Attempted to modify unauthorized fields: {', '.join(sorted(unauthorized_keys))}"
        )

    # Create a deep copy to avoid mutating the original
    updated_vehicle = copy.deepcopy(vehicle_info)

    # Apply authorized modifications
    for key, value in modifications.items():
        updated_vehicle[key] = value

    return updated_vehicle