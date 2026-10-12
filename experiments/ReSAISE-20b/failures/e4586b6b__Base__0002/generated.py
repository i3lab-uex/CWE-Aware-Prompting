# SPDX-License-Identifier: MIT
"""
Utility module for safely updating vehicle attributes.

The function `update_vehicle_attributes` ensures that only a pre‑defined set of
fields may be modified, protecting against CWE-915 (Improperly Controlled
Modification of Dynamically‑Determined Object Attributes).
"""

from __future__ import annotations

from typing import Dict, Any

# Global whitelist of fields that are allowed to be updated.
ALLOWED_FIELDS = {"make", "model", "year", "color", "vin"}


def update_vehicle_attributes(automobile: Dict[str, Any], changes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an automobile dictionary with allowed changes.

    Parameters
    ----------
    automobile : dict
        The current state of the vehicle's attributes.
    changes : dict
        A dictionary containing field names and their new values.

    Returns
    -------
    dict
        The updated automobile dictionary.

    Raises
    ------
    ValueError
        If `changes` contains a key that is not in :data:`ALLOWED_FIELDS`.
    """
    # Validate input types
    if not isinstance(automobile, dict):
        raise TypeError("`automobile` must be a dictionary.")
    if not isinstance(changes, dict):
        raise TypeError("`changes` must be a dictionary.")

    # Check that all requested changes are permitted
    for key in changes:
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be updated.")

    # Perform the updates in place
    automobile.update(changes)

    return automobile


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     car = {"make": "Toyota", "model": "Camry", "year": 2019}
#     updates = {"color": "red", "year": 2020}
#     print(update_vehicle_attributes(car, updates))