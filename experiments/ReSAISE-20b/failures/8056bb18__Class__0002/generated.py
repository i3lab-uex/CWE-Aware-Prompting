# -*- coding: utf-8 -*-

"""
Vehicle data modifier module.

This module provides a single public function, `modify_vehicle_data`, which
updates a vehicle dictionary with a set of allowed modifications.  The list of
permitted keys is defined in the global variable `ALLOWED_FIELDS`.

The function performs input validation to guard against accidental or
malicious modification of disallowed attributes.  It raises a ``ValueError``
if any requested key is not present in `ALLOWED_FIELDS`.  The original
dictionary is **not** mutated; a new dictionary containing the updates is
returned.

The implementation follows best practices for security and defensive
programming, mitigating the risk described in CWE‑913 (Improper Control of
Dynamically-Managed Code Resources).
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Configuration: list of attributes that may be updated
# --------------------------------------------------------------------------- #

ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "engine_type",
    "transmission",
    "fuel_efficiency",
    # Add other permitted fields here
]

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def modify_vehicle_data(
    vehicle_info: dict,
    modifications: dict,
) -> dict:
    """
    Return a new dictionary representing the vehicle with allowed
    modifications applied.

    Parameters
    ----------
    vehicle_info : dict
        The original vehicle data.  Must be a mapping of string keys to any
        JSON-serialisable values.
    modifications : dict
        A mapping of keys to new values.  Only keys listed in
        ``ALLOWED_FIELDS`` are permitted.

    Returns
    -------
    dict
        A shallow copy of ``vehicle_info`` with the allowed updates applied.

    Raises
    ------
    ValueError
        If ``modifications`` contains a key that is not in ``ALLOWED_FIELDS``.

    Notes
    -----
    * The function does **not** modify the input ``vehicle_info`` dictionary.
      This preserves immutability of caller data and prevents accidental
      side‑effects.
    * The check against ``ALLOWED_FIELDS`` is case-sensitive; keys must match
      exactly.
    """
    if not isinstance(vehicle_info, dict):
        raise TypeError("vehicle_info must be a dictionary")
    if not isinstance(modifications, dict):
        raise TypeError("modifications must be a dictionary")

    # Validate that all requested modifications are allowed
    disallowed = [k for k in modifications if k not in ALLOWED_FIELDS]
    if disallowed:
        raise ValueError(
            f"Attempted to modify disallowed fields: {', '.join(disallowed)}"
        )

    # Create a shallow copy to avoid mutating the original
    updated_vehicle = vehicle_info.copy()

    # Apply the allowed updates
    for key, value in modifications.items():
        updated_vehicle[key] = value

    return updated_vehicle