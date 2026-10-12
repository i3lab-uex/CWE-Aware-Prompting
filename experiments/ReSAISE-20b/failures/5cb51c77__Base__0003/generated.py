#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vehicle data modifier.

This module defines a function that updates a vehicle's information dictionary
only for fields explicitly allowed. It protects against CWE-915 by refusing to
modify any attribute that is not in the global `ALLOWED_FIELDS` list.

Author: ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Iterable

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

ALLOWED_FIELDS: Iterable[str] = (
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "owner",
)

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def modify_vehicle_data(
    vehicle_info: Dict[str, Any],
    changes_to_apply: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Update a vehicle's information dictionary with the supplied changes.

    Parameters
    ----------
    vehicle_info : dict
        Original dictionary containing vehicle attributes.
    changes_to_apply : dict
        Dictionary of key/value pairs to update in `vehicle_info`.

    Returns
    -------
    dict
        A new dictionary reflecting the applied changes. The original
        `vehicle_info` remains unmodified.

    Raises
    ------
    ValueError
        If any key in `changes_to_apply` is not present in the global
        ``ALLOWED_FIELDS`` list.
    TypeError
        If either argument is not a dictionary.

    Notes
    -----
    - The function performs a shallow copy of the input dictionaries to avoid
      side‑effects on callers.
    - Only keys in ``ALLOWED_FIELDS`` may be updated; all others are rejected
      to prevent uncontrolled attribute modification.
    """
    if not isinstance(vehicle_info, dict):
        raise TypeError("vehicle_info must be a dictionary")
    if not isinstance(changes_to_apply, dict):
        raise TypeError("changes_to_apply must be a dictionary")

    # Create a shallow copy to avoid mutating the original dict
    updated_info = copy.deepcopy(vehicle_info)

    # Validate and apply changes
    for key, value in changes_to_apply.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Attempted to modify disallowed field: {key!r}")
        updated_info[key] = value

    return updated_info