# -*- coding: utf-8 -*-
"""
Vehicle attribute updater.

This module defines a single function, ``alter_vehicle_info``, which updates
selected fields of a vehicle dictionary according to a list of allowed keys.
Only the fields listed in ``ALLOWED_FIELDS`` may be modified; any attempt to
change other keys raises a :class:`KeyError`.

The function performs a shallow copy of the input dictionary before
applying modifications, leaving the original dictionary untouched.
"""

from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    # add other mutable attributes here
]

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def alter_vehicle_info(details: Dict[str, Any], modifications: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a vehicle's attributes with the provided modifications.

    Parameters
    ----------
    details : dict
        The current state of vehicle attributes.
    modifications : dict
        Fields and new values that should be applied to ``details``.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle attributes.

    Raises
    ------
    KeyError
        If ``modifications`` contains a key that is not in :data:`ALLOWED_FIELDS`.
    TypeError
        If either ``details`` or ``modifications`` is not a mapping type.
    """
    if not isinstance(details, dict):
        raise TypeError("`details` must be a dictionary.")
    if not isinstance(modifications, dict):
        raise TypeError("`modifications` must be a dictionary.")

    # Create a shallow copy so the original ``details`` remains unchanged.
    updated = details.copy()

    for key, value in modifications.items():
        if key not in ALLOWED_FIELDS:
            raise KeyError(f"Field '{key}' is not allowed to be modified.")
        updated[key] = value

    return updated