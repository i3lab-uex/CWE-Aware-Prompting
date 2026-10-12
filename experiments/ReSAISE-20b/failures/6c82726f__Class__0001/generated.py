# -*- coding: utf-8 -*-

"""
User attribute update module.

This module provides a single public function, `update_user_attributes`,
which safely updates attributes of a user dictionary.  Only keys listed
in the global `VALID_ATTRIBUTES` mapping are allowed to be modified.
Each key is also associated with an expected type; values that do not
match the declared type are rejected.

The function returns a new dictionary containing the updated user
information, leaving the original `user` dictionary unchanged.
"""

from __future__ import annotations

import copy
from typing import Any, Dict, Mapping, Type


# --------------------------------------------------------------------------- #
# Global configuration: allowed attributes and their expected types
# --------------------------------------------------------------------------- #

VALID_ATTRIBUTES: Mapping[str, Type[Any]] = {
    "name": str,
    "email": str,
    "age": int,
}


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def update_user_attributes(user: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a user dictionary with new attribute values.

    Parameters
    ----------
    user : dict
        The original user data.  It may contain any keys, but only the keys
        listed in :data:`VALID_ATTRIBUTES` will be considered for update.
    data : dict
        A dictionary containing attribute names as keys and the new values.

    Returns
    -------
    dict
        A new dictionary containing the updated user data.  The original
        `user` dictionary is not modified.

    Raises
    ------
    ValueError
        If any key in `data` is not allowed or the value type does not match
        the expected type declared in :data:`VALID_ATTRIBUTES`.

    Notes
    -----
    - The function performs a shallow copy of the original user data.
      Nested objects are not deeply cloned; only top‑level keys are updated.
    - The function is intentionally defensive: it validates both key names
      and value types to avoid CWE‑913 vulnerabilities.
    """
    # Create a shallow copy so that the caller's data is not mutated
    updated_user = copy.deepcopy(user)

    for key, new_value in data.items():
        if key not in VALID_ATTRIBUTES:
            raise ValueError(f"Attribute '{key}' is not allowed to be updated.")

        expected_type = VALID_ATTRIBUTES[key]
        if not isinstance(new_value, expected_type):
            raise ValueError(
                f"Invalid type for attribute '{key}': "
                f"expected {expected_type.__name__}, got {type(new_value).__name__}"
            )

        updated_user[key] = new_value

    return updated_user


# --------------------------------------------------------------------------- #
# Example usage (for manual testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    sample_user = {"name": "Alice", "email": "alice@example.com", "age": 30}
    updates = {"name": "Alice B.", "age": 31}

    try:
        new_user = update_user_attributes(sample_user, updates)
        print("Original:", sample_user)
        print("Updated :", new_user)
    except ValueError as exc:
        print(f"Update failed: {exc}")