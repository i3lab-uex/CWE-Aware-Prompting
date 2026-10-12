# frozen: noqa

"""
Vehicle attributes update module.

This module provides a single public function, `update_vehicle_attributes`,
which applies user-specified changes to an existing vehicle dictionary
while enforcing a whitelist of modifiable fields.
"""

from __future__ import annotations

# Whitelist of keys that are allowed to be updated
ALLOWED_FIELDS = {"make", "model", "year", "color", "vin"}

def update_vehicle_attributes(automobile: dict, changes: dict) -> dict:
    """
    Update the attributes of a vehicle dictionary with new values.

    Parameters
    ----------
    automobile : dict
        The current state of the vehicle's attributes.
    changes : dict
        A dictionary containing fields and their new values.

    Returns
    -------
    dict
        A new dictionary with the applied changes.

    Raises
    ------
    KeyError
        If any key in ``changes`` is not present in :data:`ALLOWED_FIELDS`.
    TypeError
        If either ``automobile`` or ``changes`` is not a mapping type.
    """
    # Ensure both arguments are dictionaries (or subclasses of Mapping)
    if not isinstance(automobile, dict):
        raise TypeError("`automobile` must be a dictionary.")
    if not isinstance(changes, dict):
        raise TypeError("`changes` must be a dictionary.")

    # Check for disallowed fields
    invalid_keys = set(changes) - ALLOWED_FIELDS
    if invalid_keys:
        raise KeyError(
            f"Attempted to modify disallowed fields: {sorted(invalid_keys)}"
        )

    # Create a shallow copy to avoid mutating the original vehicle dict
    updated = automobile.copy()

    # Apply allowed changes
    for key, value in changes.items():
        updated[key] = value

    return updated