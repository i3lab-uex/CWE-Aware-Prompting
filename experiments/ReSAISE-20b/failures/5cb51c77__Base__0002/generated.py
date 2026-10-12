#!/usr/bin/env python3
"""
Vehicle data modifier.

This module defines a single public function `modify_vehicle_data` that updates a
dictionary containing vehicle information. Only keys listed in the global
``ALLOWED_FIELDS`` list may be modified; any attempt to change a disallowed key
will raise a ``ValueError``.  The function returns a new dictionary that
contains the updated values while preserving all other original entries.

The implementation is intentionally defensive: it performs type checks,
creates a shallow copy to avoid mutating the caller's data, and rejects
non‑string keys.  This mitigates CWE‑915 by ensuring that only a whitelist of
attributes can be altered.
"""

from __future__ import annotations

from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Allowed fields for a vehicle.  This list acts as the whitelist that
# controls which attributes may be modified.
# --------------------------------------------------------------------------- #
ALLOWED_FIELDS = {"make", "model", "year", "color", "vin"}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def modify_vehicle_data(
    vehicle_info: Dict[str, Any],
    changes_to_apply: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update ``vehicle_info`` with values from ``changes_to_apply`` only for keys
    that are present in the global ``ALLOWED_FIELDS`` set.

    Parameters
    ----------
    vehicle_info : dict
        Dictionary containing the original vehicle data.
    changes_to_apply : dict
        Dictionary mapping field names to new values.

    Returns
    -------
    dict
        A shallow copy of ``vehicle_info`` with the allowed updates applied.

    Raises
    ------
    ValueError
        If any key in ``changes_to_apply`` is not a string or is not part of
        the ``ALLOWED_FIELDS`` set.

    Notes
    -----
    * The function does **not** modify the input ``vehicle_info`` in place.
      A new dictionary is returned.
    * Only top‑level keys are considered; nested structures are left untouched.
    """
    if not isinstance(vehicle_info, dict):
        raise TypeError("vehicle_info must be a dictionary")

    if not isinstance(changes_to_apply, dict):
        raise TypeError("changes_to_apply must be a dictionary")

    # Create a shallow copy to avoid mutating the original
    updated = vehicle_info.copy()

    for key, new_value in changes_to_apply.items():
        if not isinstance(key, str):
            raise ValueError(f"Field name must be a string; got {key!r}")

        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Attempted to modify disallowed field: {key!r}")

        # Apply the change
        updated[key] = new_value

    return updated

# --------------------------------------------------------------------------- #
# Example usage (commented out to keep module import clean)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     original = {"make": "Toyota", "model": "Corolla", "year": 2010}
#     changes = {"year": 2021, "color": "blue"}
#     print(modify_vehicle_data(original, changes))