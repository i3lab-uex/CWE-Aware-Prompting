# -*- coding: utf-8 -*-
"""
Vehicle attribute updater.

This module defines a single public function, :func:`alter_vehicle_info`, which
updates the attributes of a vehicle represented by a dictionary. Only keys that
are listed in :data:`ALLOWED_FIELDS` may be modified; attempting to change any
other key raises a ``ValueError``.  The function performs a shallow copy of the
input dictionary so that callers are not surprised by in‑place modifications.

The implementation is intentionally simple but guards against common
misuses, such as accidentally modifying the original dictionary or attempting
to write disallowed keys.  It does not attempt to validate the values beyond
ensuring they are present in the ``modifications`` mapping.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Public constants
# --------------------------------------------------------------------------- #

#: Fields that may be updated by :func:`alter_vehicle_info`.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "engine_size",
]

# --------------------------------------------------------------------------- #
# Exceptions
# --------------------------------------------------------------------------- #

class InvalidFieldError(ValueError):
    """
    Raised when an attempt is made to modify a field that is not in
    :data:`ALLOWED_FIELDS`.
    """
    pass

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def alter_vehicle_info(details: dict, modifications: dict) -> dict:
    """
    Update allowed fields of a vehicle dictionary.

    Parameters
    ----------
    details : dict
        The current state of the vehicle's attributes.
    modifications : dict
        Keys and new values to apply.  Only keys present in
        :data:`ALLOWED_FIELDS` are permitted.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle information.
        The original ``details`` mapping is left untouched.

    Raises
    ------
    InvalidFieldError
        If any key in ``modifications`` is not listed in :data:`ALLOWED_FIELDS`.
    TypeError
        If either argument is not a mapping type.

    Notes
    -----
    The function performs a shallow copy of ``details`` before applying changes.
    This means nested mutable objects are still shared between the original and
    returned dictionary.  If a deep copy is required, callers should use
    :func:`copy.deepcopy` before invoking this function.
    """
    if not isinstance(details, dict):
        raise TypeError(f"'details' must be a dict, got {type(details).__name__}")
    if not isinstance(modifications, dict):
        raise TypeError(f"'modifications' must be a dict, got {type(modifications).__name__}")

    # Validate keys
    disallowed = set(modifications) - set(ALLOWED_FIELDS)
    if disallowed:
        raise InvalidFieldError(
            f"Attempted to modify disallowed fields: {', '.join(sorted(disallowed))}"
        )

    # Shallow copy to avoid mutating the original
    updated = details.copy()

    # Apply allowed modifications
    for key, value in modifications.items():
        updated[key] = value

    return updated

# --------------------------------------------------------------------------- #
# Example usage (commented out to avoid side effects during import)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    vehicle = {
        "make": "Toyota",
        "model": "Camry",
        "year": 2018,
        "color": "red",
        "vin": "123ABC456DEF",
    }

    changes = {"color": "blue", "year": 2020}
    try:
        new_vehicle = alter_vehicle_info(vehicle, changes)
        print(new_vehicle)
    except Exception as exc:
        print(f"Error: {exc}")