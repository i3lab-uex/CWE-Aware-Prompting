#!/usr/bin/env python3
"""
Vehicle data modifier.

This module defines a single public function, `modify_vehicle_data`, which updates
a vehicle dictionary in place with only those attributes that are explicitly
allowed.  The list of permissible keys is defined by the global constant
`ALLOWED_FIELDS`.

The implementation guards against accidental modification of disallowed keys,
and it performs a shallow copy when necessary to avoid unintended side‑effects.
"""

from __future__ import annotations

from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

#: Keys that may be updated by :func:`modify_vehicle_data`.
ALLOWED_FIELDS: tuple[str, ...] = (
    "make",
    "model",
    "year",
    "color",
    "vin",
    "registration_number",
    "owner_name",
)

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def modify_vehicle_data(
    vehicle_info: Dict[str, Any], modifications: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a vehicle dictionary with authorized modifications.

    Parameters
    ----------
    vehicle_info : dict
        The original vehicle data.  This dictionary is modified in place.
    modifications : dict
        Mapping of attribute names to new values.

    Returns
    -------
    dict
        The same dictionary instance as ``vehicle_info`` after modifications.

    Raises
    ------
    ValueError
        If any key in ``modifications`` is not present in :data:`ALLOWED_FIELDS`.

    Notes
    -----
    * The function performs a shallow update; nested objects are not deep‑copied.
    * Keys present in ``modifications`` but missing from ``vehicle_info`` are
      added to the dictionary.  This allows adding new optional attributes
      while still enforcing the whitelist.

    Examples
    --------
    >>> vehicle = {"make": "Toyota", "model": "Corolla", "year": 2010}
    >>> modify_vehicle_data(vehicle, {"color": "red", "year": 2012})
    {'make': 'Toyota', 'model': 'Corolla', 'year': 2012, 'color': 'red'}
    """
    # Ensure we are working with a mutable mapping
    if not isinstance(vehicle_info, dict):
        raise TypeError("vehicle_info must be a dictionary")

    if not isinstance(modifications, dict):
        raise TypeError("modifications must be a dictionary")

    # Validate all keys before mutating to avoid partial updates
    unauthorized = [k for k in modifications if k not in ALLOWED_FIELDS]
    if unauthorized:
        raise ValueError(
            f"Attempted to modify disallowed fields: {', '.join(unauthorized)}"
        )

    # Apply the authorized updates
    vehicle_info.update(modifications)

    return vehicle_info

# --------------------------------------------------------------------------- #
# End of module
# --------------------------------------------------------------------------- #