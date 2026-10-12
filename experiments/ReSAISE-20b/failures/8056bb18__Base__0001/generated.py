# SPDX-License-Identifier: MIT
"""
Vehicle data modification utility.

This module provides a single function, ``modify_vehicle_data``, which safely
updates an existing vehicle dictionary.  Only attributes listed in the global
``ALLOWED_FIELDS`` constant may be modified, protecting against accidental or
malicious changes to sensitive data.
"""

from __future__ import annotations

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
    "engine_type",
    "transmission",
    # Add more permitted fields here as needed
]

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def modify_vehicle_data(
    vehicle_info: Dict[str, Any],
    modifications: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a vehicle dictionary with authorized changes.

    Parameters
    ----------
    vehicle_info : dict
        The original vehicle data.  This dictionary is modified in place.
    modifications : dict
        A mapping of attribute names to new values.  Only keys present in
        ``ALLOWED_FIELDS`` will be applied.

    Returns
    -------
    dict
        The updated vehicle dictionary (the same object that was passed in).

    Raises
    ------
    ValueError
        If any key in ``modifications`` is not permitted.
    TypeError
        If ``vehicle_info`` or ``modifications`` are not dictionaries.

    Notes
    -----
    - The function performs a shallow update; nested structures are not
      recursively merged.
    - No other side effects occur beyond updating ``vehicle_info``.

    Examples
    --------
    >>> vehicle = {'make': 'Toyota', 'model': 'Corolla', 'year': 2018}
    >>> modify_vehicle_data(vehicle, {'color': 'red', 'vin': '12345'})
    {'make': 'Toyota', 'model': 'Corolla', 'year': 2018, 'color': 'red', 'vin': '12345'}
    """
    if not isinstance(vehicle_info, dict):
        raise TypeError("vehicle_info must be a dictionary")
    if not isinstance(modifications, dict):
        raise TypeError("modifications must be a dictionary")

    # Identify any disallowed keys
    disallowed = [k for k in modifications if k not in ALLOWED_FIELDS]
    if disallowed:
        raise ValueError(
            f"Attempted to modify disallowed fields: {', '.join(disallowed)}"
        )

    # Apply the authorized updates
    for key, value in modifications.items():
        vehicle_info[key] = value

    return vehicle_info