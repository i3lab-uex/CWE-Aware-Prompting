#!/usr/bin/env python3
"""
Vehicle attribute updater.

The module exposes a single function `update_vehicle_attributes` which updates
only the fields that are listed in the global ``ALLOWED_FIELDS`` list.
Attempting to modify a disallowed field raises a :class:`ValueError`.

The function returns a new dictionary containing the updated state, leaving
the original input untouched.
"""

from __future__ import annotations

from typing import Dict, Any, Iterable


# --------------------------------------------------------------------------- #
#  Global configuration
# --------------------------------------------------------------------------- #

ALLOWED_FIELDS: Iterable[str] = (
    "make",
    "model",
    "year",
    "color",
    "vin",
)


# --------------------------------------------------------------------------- #
#  Public API
# --------------------------------------------------------------------------- #

def update_vehicle_attributes(
    automobile: Dict[str, Any], changes: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Return a new vehicle dictionary with allowed fields updated.

    Parameters
    ----------
    automobile : dict
        The original state of the vehicle. It may contain arbitrary keys.
    changes : dict
        Mapping of field names to new values that should be applied.

    Returns
    -------
    dict
        A shallow copy of ``automobile`` with the allowed changes applied.

    Raises
    ------
    ValueError
        If any key in ``changes`` is not present in :data:`ALLOWED_FIELDS`.

    Notes
    -----
    * The function does **not** modify ``automobile`` in place.
    * Only keys listed in :data:`ALLOWED_FIELDS` are accepted; all others
      trigger an exception to avoid accidental tampering.
    """
    # Validate input types early for clarity
    if not isinstance(automobile, dict):
        raise TypeError("`automobile` must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("`changes` must be a dictionary")

    # Create a shallow copy to avoid mutating the original
    updated = dict(automobile)

    for key, value in changes.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(
                f"Field '{key}' is not allowed to be updated. "
                f"Allowed fields: {sorted(ALLOWED_FIELDS)}"
            )
        updated[key] = value

    return updated


# --------------------------------------------------------------------------- #
#  Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    vehicle = {"make": "Toyota", "model": "Camry", "year": 2020, "color": "red"}
    updates = {"color": "blue", "year": 2021}
    try:
        new_vehicle = update_vehicle_attributes(vehicle, updates)
        print("Original:", vehicle)
        print("Updated :", new_vehicle)
    except Exception as exc:
        print(f"Error: {exc}")