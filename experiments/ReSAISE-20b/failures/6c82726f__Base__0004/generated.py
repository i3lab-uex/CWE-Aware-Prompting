# -*- coding: utf-8 -*-

"""
Utility for safely updating user attributes.
"""

from __future__ import annotations

# A whitelist of attributes that are allowed to be updated.
VALID_ATTRIBUTES = {"name", "email", "age"}

def update_user_attributes(user: dict, data: dict) -> dict:
    """
    Update a user dictionary with new attribute values in a safe manner.

    Parameters
    ----------
    user : dict
        Existing user object.  The function does not modify this dictionary in place.
    data : dict
        Mapping of attribute names to new values.

    Returns
    -------
    dict
        A new dictionary containing the updated user attributes.

    Raises
    ------
    ValueError
        If any key in ``data`` is not present in :data:`VALID_ATTRIBUTES`.
    """
    # Create a shallow copy to avoid mutating the original user dict.
    updated_user = user.copy()

    for key, value in data.items():
        if key not in VALID_ATTRIBUTES:
            raise ValueError(f"Attempt to update disallowed attribute: {key!r}")

        updated_user[key] = value

    return updated_user