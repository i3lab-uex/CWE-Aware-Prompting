# -*- coding: utf-8 -*-
"""
Module providing a secure way to view user profiles.

The function `see_user_profile` ensures that only the owner of a profile
or an administrator can access any user’s profile.  It protects against
CWE-284 (Improper Access Control) by explicitly checking the requesting
user’s role before returning sensitive data.
"""

from typing import Dict, Any

# Example data structures (replace with actual data sources in production)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Eve",   "email": "eve@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"username": "alice",   "role": "user"},
    2: {"username": "bob",     "role": "admin"},
    3: {"username": "eve",     "role": "user"},
}

def see_user_profile(current_id: int, target_id: int) -> Any:
    """
    Return the profile of `target_id` if the requesting user (`current_id`)
    is either the owner or has an administrative role.

    Parameters
    ----------
    current_id : int
        The ID of the user making the request.
    target_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict | str
        The user profile dictionary if access is allowed, otherwise the string
        'Unauthorized'.

    Notes
    -----
    * The function does **not** raise exceptions for unauthorized access;
      it simply returns a string to avoid leaking information.
    * Role names are case‑sensitive; adjust the comparison if your system uses
      different conventions.
    """
    # Verify that both users exist in the data stores
    if current_id not in USERS or target_id not in USER_PROFILES:
        return "Unauthorized"

    # Retrieve the role of the requesting user
    current_role = USERS[current_id].get("role", "").lower()

    # Access is granted if the user is an admin or is requesting their own profile
    if current_role == "admin" or current_id == target_id:
        return USER_PROFILES[target_id]

    # Default: deny access
    return "Unauthorized"