# update_user_attributes.py

"""
Utility to safely update user attributes.

The function only allows modifications of a pre‑defined set of
attributes stored in the global VALID_ATTRIBUTES collection.
All other keys are ignored to prevent accidental or malicious
changes.

CWE‑664 (Improper Control of a Resource Through its Lifetime) is avoided by
not exposing or altering any external resources; the function operates
solely on in‑memory data structures.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Set


# Define the set of attributes that may be updated.
VALID_ATTRIBUTES: Set[str] = {"name", "email", "age"}


def update_user_attributes(user: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new user dictionary with only the attributes present in
    VALID_ATTRIBUTES updated from ``data``.  The original ``user``
    dictionary is left untouched.

    Parameters
    ----------
    user : dict
        Original user data.  Expected keys include at least the
        attributes in ``VALID_ATTRIBUTES`` but may contain more.
    data : dict
        Proposed updates.  Only keys present in ``VALID_ATTRIBUTES`` are applied.

    Returns
    -------
    dict
        A new dictionary containing the updated user data.

    Raises
    ------
    TypeError
        If ``user`` or ``data`` is not a dictionary.
    ValueError
        If any key in ``data`` is not in ``VALID_ATTRIBUTES``.
    """
    if not isinstance(user, dict):
        raise TypeError("user must be a dictionary")
    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")

    # Check for invalid keys
    invalid_keys = set(data) - VALID_ATTRIBUTES
    if invalid_keys:
        raise ValueError(f"Invalid attribute(s) for update: {', '.join(invalid_keys)}")

    # Create a shallow copy to avoid mutating the original user
    updated_user = copy.deepcopy(user)

    # Apply allowed updates
    for key in VALID_ATTRIBUTES:
        if key in data:
            updated_user[key] = data[key]

    return updated_user