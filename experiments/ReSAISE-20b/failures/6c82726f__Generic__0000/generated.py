# -*- coding: utf-8 -*-

"""
Utility module for updating user attributes safely.

The `update_user_attributes` function ensures that only whitelisted
attributes are modified.  It performs a shallow copy of the original user
dictionary to avoid side‑effects on the caller's data.
"""

from typing import Dict, Any

# Global set of attributes that may be updated
VALID_ATTRIBUTES = {"name", "email", "age"}


def update_user_attributes(user: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new user dictionary with the provided attributes updated.

    Parameters
    ----------
    user : dict
        The original user dictionary.
    data : dict
        Dictionary containing attributes to update.

    Returns
    -------
    dict
        A new dictionary representing the updated user.

    Raises
    ------
    ValueError
        If `data` contains keys that are not in :data:`VALID_ATTRIBUTES`.

    Notes
    -----
    - The function does **not** modify the original `user` dictionary.
    - Only keys present in :data:`VALID_ATTRIBUTES` are considered; all
      others trigger a ``ValueError`` to prevent accidental injection of
      unsupported attributes.
    """
    # Validate incoming keys
    invalid_keys = set(data) - VALID_ATTRIBUTES
    if invalid_keys:
        raise ValueError(f"Attempted to update unsupported attributes: {sorted(invalid_keys)}")

    # Create a shallow copy of the original user dict
    updated_user = user.copy()

    # Update with validated data
    for key, value in data.items():
        updated_user[key] = value

    return updated_user