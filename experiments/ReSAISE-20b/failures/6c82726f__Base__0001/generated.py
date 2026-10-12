# -*- coding: utf-8 -*-
"""
Utility to safely update user attributes.

The function ensures that only a predefined set of attributes can be modified,
protecting against CWE‑915 (Improperly Controlled Modification of Dynamically‑Determined Object Attributes).
"""

from typing import Dict, Any

# Define the set of attributes that are allowed to be updated.
VALID_ATTRIBUTES = {"name", "email", "age"}


def update_user_attributes(user: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a user dictionary with new values for allowed attributes.

    Parameters
    ----------
    user : dict
        The original user dictionary. Must contain keys for all attributes that can be updated.
    data : dict
        A dictionary containing attribute names and their new values.

    Returns
    -------
    dict
        A new user dictionary with the specified updates applied.

    Raises
    ------
    ValueError
        If `data` contains any keys that are not in :data:`VALID_ATTRIBUTES`.

    Notes
    -----
    - The function does **not** modify the original `user` dictionary; it returns a new dictionary.
    - Only attributes listed in :data:`VALID_ATTRIBUTES` may be changed.
    """
    # Ensure no disallowed keys are present
    invalid_keys = set(data) - VALID_ATTRIBUTES
    if invalid_keys:
        raise ValueError(
            f"Attempted to update disallowed attributes: {sorted(invalid_keys)}"
        )

    # Create a shallow copy to avoid mutating the original
    updated_user = user.copy()

    # Apply allowed updates
    for key in data:
        updated_user[key] = data[key]

    return updated_user