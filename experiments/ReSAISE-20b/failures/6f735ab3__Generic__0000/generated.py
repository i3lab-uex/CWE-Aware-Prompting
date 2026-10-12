# -*- coding: utf-8 -*-
"""
Vehicle update helper module.
"""

from __future__ import annotations

# List of attributes that may be modified.  The list can be extended
# in a single place without touching the logic of ``update_vehicle_info``.
ALLOWED_FIELDS = {"make", "model", "year", "owner", "registration"}


def update_vehicle_info(vehicle: dict, updates: dict) -> dict:
    """
    Update a vehicle dictionary with new values.

    Parameters
    ----------
    vehicle : dict
        The original vehicle data.  It is *not* modified in place.
    updates : dict
        Mapping of field names to new values.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle data.

    Raises
    ------
    ValueError
        If ``updates`` contains a key that is not in :data:`ALLOWED_FIELDS`.

    Notes
    -----
    * The function performs a shallow copy of ``vehicle`` to avoid side‑effects.
    * Keys in ``updates`` that are not allowed raise an exception to prevent
      accidental tampering with protected fields (e.g., ``id`` or ``created_at``).
    """
    if not isinstance(vehicle, dict):
        raise TypeError("vehicle must be a dictionary")
    if not isinstance(updates, dict):
        raise TypeError("updates must be a dictionary")

    # Guard against unknown or forbidden keys
    disallowed = set(updates) - ALLOWED_FIELDS
    if disallowed:
        raise ValueError(
            f"Attempted to update forbidden fields: {', '.join(sorted(disallowed))}"
        )

    # Create a shallow copy so the original vehicle remains unchanged
    updated = vehicle.copy()
    updated.update(updates)
    return updated


# Example usage (remove or comment out in production code):
if __name__ == "__main__":
    vehicle = {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2010,
        "owner": "Alice",
        "registration": "XYZ1234",
    }

    try:
        new_vehicle = update_vehicle_info(vehicle, {"year": 2012, "owner": "Bob"})
        print("Updated vehicle:", new_vehicle)
    except Exception as exc:
        print(f"Error: {exc}")