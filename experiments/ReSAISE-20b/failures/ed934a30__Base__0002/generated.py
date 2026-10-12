# -*- coding: utf-8 -*-
"""
Vehicle attribute updater.

This module defines a single function, ``alter_vehicle_info``, that safely updates
the attributes of a vehicle dictionary.  Only the keys listed in the global
``ALLOWED_FIELDS`` constant are permitted to be modified.  Any attempt to modify
a disallowed field will raise a ``ValueError``.

The function performs a shallow copy of the input dictionary to avoid
side‑effects on the caller's data structure.
"""

from __future__ import annotations

# List of keys that may be updated.  Add or remove entries as needed.
ALLOWED_FIELDS = {"make", "model", "year", "color", "vin"}

def alter_vehicle_info(details: dict, modifications: dict) -> dict:
    """
    Update a vehicle's attributes with the provided ``modifications`` dictionary.

    Parameters
    ----------
    details : dict
        Current vehicle attributes.  Keys not in ``ALLOWED_FIELDS`` are ignored.
    modifications : dict
        Proposed updates.  Only keys in ``ALLOWED_FIELDS`` will be applied.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle attributes.

    Raises
    ------
    ValueError
        If ``modifications`` contains any keys that are not in ``ALLOWED_FIELDS``.

    Notes
    -----
    - The function returns a new dictionary; the original ``details`` remains unchanged.
    - Keys present in ``modifications`` but not in ``details`` are added to the result
      if they are allowed.
    """
    # Validate modification keys first
    invalid_keys = set(modifications) - ALLOWED_FIELDS
    if invalid_keys:
        raise ValueError(
            f"Attempted to modify disallowed fields: {', '.join(sorted(invalid_keys))}"
        )

    # Create a shallow copy to avoid mutating the caller's dict
    updated = details.copy()

    # Apply allowed modifications
    for key, value in modifications.items():
        updated[key] = value

    return updated


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     vehicle = {"make": "Toyota", "model": "Corolla", "year": 2010}
#     mods = {"color": "red", "year": 2012}
#     print(alter_vehicle_info(vehicle, mods))