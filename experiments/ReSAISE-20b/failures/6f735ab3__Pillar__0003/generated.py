# -*- coding: utf-8 -*-
"""
Vehicle information updater.

The module defines a single public function, :func:`update_vehicle_info`, that
updates a vehicle dictionary only for fields listed in the global constant
``ALLOWED_FIELDS``.  The function performs strict type checking and raises a
descriptive exception when an invalid field is supplied.

CWE-664 (Improper Control of a Resource Through its Lifetime) is avoided by
creating and returning a new dictionary instead of mutating the original
``vehicle`` argument, ensuring that callers cannot accidentally alter the
source data after the function returns.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

#: Attributes that are permitted to be updated.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "owner",
    "registration",
]

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def update_vehicle_info(vehicle: dict, updates: dict) -> dict:
    """
    Return a new vehicle dictionary with the supplied ``updates`` applied.

    Parameters
    ----------
    vehicle :
        A mapping representing a vehicle.  It must be a dictionary and is
        considered read‑only by this function.
    updates :
        A mapping of attributes to new values.  Only keys present in
        :data:`ALLOWED_FIELDS` are accepted.

    Returns
    -------
    dict
        A new dictionary containing the original vehicle data updated with
        ``updates``.  The input ``vehicle`` is not modified.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If ``updates`` contains keys that are not listed in :data:`ALLOWED_FIELDS`.

    Notes
    -----
    * The function performs a shallow copy of the ``vehicle`` dictionary.
      Nested mutable objects are **not** deep‑copied.  If nested structures
      require isolation, callers should perform their own copying.
    * The function is deliberately strict about field names to avoid
      accidental injection of unexpected data, mitigating risks associated
      with improper resource control.
    """
    if not isinstance(vehicle, dict):
        raise TypeError(f"'vehicle' must be a dict; got {type(vehicle).__name__}")

    if not isinstance(updates, dict):
        raise TypeError(f"'updates' must be a dict; got {type(updates).__name__}")

    # Create a shallow copy to preserve the original vehicle dictionary.
    updated_vehicle = dict(vehicle)

    for key, value in updates.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(
                f"Field '{key}' is not allowed to be updated. "
                f"Allowed fields: {sorted(ALLOWED_FIELDS)}"
            )
        # Assign the new value.  Any validation of ``value`` itself is
        # left to higher‑level logic.
        updated_vehicle[key] = value

    return updated_vehicle