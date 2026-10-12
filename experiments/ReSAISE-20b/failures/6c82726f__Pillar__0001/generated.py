# -*- coding: utf-8 -*-
"""
Utility module for updating user attributes safely.

The module defines a global dictionary `VALID_ATTRIBUTES` containing the
set of attribute names that are allowed to be updated.  The function
`update_user_attributes()` validates the input data against this set,
ensures that only known attributes are modified, and returns a new
dictionary representing the updated user object.

The implementation deliberately avoids modifying the original `user`
object to preserve immutability and prevent accidental side‑effects.
"""

from copy import deepcopy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Global configuration – attributes that can be updated
# --------------------------------------------------------------------------- #
VALID_ATTRIBUTES = {"name", "email", "age"}


def update_user_attributes(user: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a user dictionary with new attribute values.

    Parameters
    ----------
    user : dict
        The original user object.  It is not modified in place.
    data : dict
        A dictionary containing attribute names and their new values.

    Returns
    -------
    dict
        A shallow copy of `user` with the specified attributes updated.

    Raises
    ------
    ValueError
        If `data` contains a key that is not in :data:`VALID_ATTRIBUTES`.

    Notes
    -----
    * Only attributes listed in `VALID_ATTRIBUTES` may be updated.
    * The function returns a new dictionary; the original `user`
      remains unchanged, protecting against unintended side‑effects.
    """
    # Validate the input data keys
    invalid_keys = set(data) - VALID_ATTRIBUTES
    if invalid_keys:
        raise ValueError(
            f"Attempted to update unsupported attributes: {', '.join(sorted(invalid_keys))}"
        )

    # Create a shallow copy of the user dict to avoid mutating the caller's data
    updated_user = deepcopy(user)

    # Apply updates
    for key, value in data.items():
        updated_user[key] = value

    return updated_user