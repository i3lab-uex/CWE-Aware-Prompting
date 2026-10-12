# -*- coding: utf-8 -*-
"""
Utility module for safely updating vehicle dictionaries.

The `update_vehicle_info` function accepts a vehicle dictionary and an
updates dictionary. Only keys listed in the global `ALLOWED_FIELDS`
constant are applied to the vehicle; any other keys are ignored.
This mitigates CWE‑915 by preventing uncontrolled attribute
modification from external input.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import copy
import logging
from typing import Dict, Any, Iterable

# Configure a module‑level logger.  In real deployments this would be
# configured by the application, but we set a default level here.
logging.basicConfig(level=logging.WARNING)
_logger = logging.getLogger(__name__)

# List of vehicle attributes that are permitted to be modified.
ALLOWED_FIELDS: Iterable[str] = (
    "make",
    "model",
    "year",
    "owner",
    "registration",
)

def update_vehicle_info(vehicle: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a vehicle dictionary with values from *updates* only for
    fields listed in :data:`ALLOWED_FIELDS`.

    Parameters
    ----------
    vehicle :
        Dictionary representing a vehicle. It may contain any keys,
        but only the allowed fields will be updated.
    updates :
        Dictionary containing proposed changes. Only keys present in
        :data:`ALLOWED_FIELDS` will be applied.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle data.
        The original *vehicle* object is left untouched.

    Raises
    ------
    TypeError
        If either *vehicle* or *updates* is not a dictionary.
    ValueError
        If *vehicle* contains keys that are not strings (e.g. a tuple key).
    """
    if not isinstance(vehicle, dict):
        raise TypeError(f"vehicle must be a dict; got {type(vehicle).__name__}")
    if not isinstance(updates, dict):
        raise TypeError(f"updates must be a dict; got {type(updates).__name__}")

    # Ensure all vehicle keys are hashable and string‑like to avoid
    # subtle bugs or malicious key types.
    for key in vehicle:
        if not isinstance(key, str):
            raise ValueError(f"vehicle contains non‑string key: {key!r}")

    # Create a shallow copy to avoid mutating the input.
    updated_vehicle = copy.deepcopy(vehicle)

    for key, value in updates.items():
        if key in ALLOWED_FIELDS:
            updated_vehicle[key] = value
        else:
            _logger.debug(
                "Attempted to update disallowed field %s; ignoring.",
                key,
            )

    return updated_vehicle