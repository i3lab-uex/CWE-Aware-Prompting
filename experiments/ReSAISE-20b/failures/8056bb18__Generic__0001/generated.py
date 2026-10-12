#!/usr/bin/env python3
"""
Vehicle data modification module.

This module provides a single function `modify_vehicle_data` that updates a
vehicle dictionary with new values while enforcing an explicit whitelist of
modifiable fields.

Author: ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Iterable

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

# Define the list of keys that are allowed to be modified.
ALLOWED_FIELDS: Iterable[str] = (
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "price",
    "owner",
)

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def modify_vehicle_data(
    vehicle_info: Dict[str, Any], modifications: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a vehicle dictionary with provided modifications while enforcing
    that only fields listed in ``ALLOWED_FIELDS`` may be changed.

    Parameters
    ----------
    vehicle_info : dict
        The original dictionary representing a vehicle.
    modifications : dict
        Dictionary mapping attribute names to new values.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle data. The original
        ``vehicle_info`` is not mutated.

    Raises
    ------
    ValueError
        If any key in ``modifications`` is not present in ``ALLOWED_FIELDS``.

    Notes
    -----
    * The function performs a shallow copy of ``vehicle_info``. Nested objects
      (e.g., lists or dictionaries) are copied by reference.
    * If ``vehicle_info`` does not contain a key present in
      ``ALLOWED_FIELDS``, it will be added with the provided value.
    """
    # Validate that all modification keys are allowed
    disallowed = set(modifications) - set(ALLOWED_FIELDS)
    if disallowed:
        raise ValueError(
            f"Modification contains disallowed fields: {', '.join(sorted(disallowed))}"
        )

    # Create a shallow copy to avoid mutating the input dictionary
    updated_vehicle = copy.copy(vehicle_info)

    # Apply modifications
    for key, value in modifications.items():
        updated_vehicle[key] = value

    return updated_vehicle