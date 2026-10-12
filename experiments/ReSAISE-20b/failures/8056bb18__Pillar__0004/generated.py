# -*- coding: utf-8 -*-
"""
Vehicle data modification module.

This module defines a single public function, `modify_vehicle_data`, which updates
selected attributes of a vehicle dictionary in a controlled and secure manner.
"""

from __future__ import annotations

from typing import Dict, Any, Iterable

# Global list of fields that are allowed to be modified.
ALLOWED_FIELDS: Iterable[str] = (
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "fuel_type",
    "transmission",
)

def _validate_inputs(vehicle_info: Dict[str, Any], modifications: Dict[str, Any]) -> None:
    """
    Validate the inputs before performing any modifications.

    Raises:
        TypeError: If either argument is not a dictionary.
        ValueError: If any modification key is not allowed.
    """
    if not isinstance(vehicle_info, dict):
        raise TypeError(f"vehicle_info must be a dict, got {type(vehicle_info).__name__}")

    if not isinstance(modifications, dict):
        raise TypeError(f"modifications must be a dict, got {type(modifications).__name__}")

    # Check that all modification keys are permitted.
    invalid_keys = [k for k in modifications if k not in ALLOWED_FIELDS]
    if invalid_keys:
        raise ValueError(
            f"The following fields are not allowed to be modified: {', '.join(invalid_keys)}"
        )

def modify_vehicle_data(vehicle_info: Dict[str, Any], modifications: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update only the permitted attributes of a vehicle dictionary.

    The function performs validation to ensure that:
      * Both inputs are dictionaries.
      * Only fields listed in ``ALLOWED_FIELDS`` can be updated.

    The original dictionary is not mutated; instead a shallow copy with the
    updates applied is returned.

    Parameters
    ----------
    vehicle_info : dict
        The original vehicle data.
    modifications : dict
        Mapping of attribute names to their new values.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle data.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If any modification key is not in ``ALLOWED_FIELDS``.
    """
    # Validate arguments early to avoid side effects.
    _validate_inputs(vehicle_info, modifications)

    # Create a shallow copy so the caller's data remains unchanged.
    updated_vehicle = vehicle_info.copy()

    # Apply each permitted modification.
    for key, value in modifications.items():
        updated_vehicle[key] = value

    return updated_vehicle