#!/usr/bin/env python3
"""
Vehicle information adjustment module.

Provides a single public function:
    adjust_vehicle_info(auto: dict, modifications: dict) -> dict

The function updates only the attributes listed in the global ALLOWED_FIELDS list.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Define the fields that are allowed to be modified.
# In a real project this list might come from configuration or constants
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    # Add additional permitted fields here
]

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def adjust_vehicle_info(auto: dict, modifications: dict) -> dict:
    """
    Update an automobile dictionary with a set of permitted modifications.

    Parameters
    ----------
    auto : dict
        The original vehicle dictionary. Keys are expected to be strings.
    modifications : dict
        A mapping of attribute names to new values.

    Returns
    -------
    dict
        The updated vehicle dictionary. The original `auto` is modified in place.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If any key in `modifications` is not in ``ALLOWED_FIELDS``.
    """
    # Basic type checks
    if not isinstance(auto, dict):
        raise TypeError(f"'auto' must be a dict; got {type(auto).__name__}")
    if not isinstance(modifications, dict):
        raise TypeError(f"'modifications' must be a dict; got {type(modifications).__name__}")

    # Ensure all modification keys are allowed
    disallowed = set(modifications) - set(ALLOWED_FIELDS)
    if disallowed:
        raise ValueError(f"Modification keys not allowed: {sorted(disallowed)}")

    # Perform updates
    auto.update(modifications)

    return auto

# --------------------------------------------------------------------------- #
# Example usage (commented out)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     vehicle = {"make": "Toyota", "model": "Camry", "year": 2019, "color": "blue"}
#     changes = {"color": "red", "year": 2020}
#     updated_vehicle = adjust_vehicle_info(vehicle, changes)
#     print(updated_vehicle)