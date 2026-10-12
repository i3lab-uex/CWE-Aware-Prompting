# -*- coding: utf-8 -*-

"""
Module providing access-controlled retrieval of user profiles.
"""

from typing import Dict, Any

# Example data structures (replace with actual data sources)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Eve",   "email": "eve@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"username": "alice", "role": "user"},
    2: {"username": "bob",   "role": "admin"},
    3: {"username": "eve",   "role": "user"},
}


def display_user_profile(active_user_id: int, profile_user_id: int) -> Any:
    """
    Return the requested user profile if access is authorized.

    Parameters
    ----------
    active_user_id : int
        ID of the user making the request.
    profile_user_id : int
        ID of the profile being requested.

    Returns
    -------
    dict | str
        The user profile dictionary if access is allowed,
        otherwise the string 'Unauthorized'.

    Notes
    -----
    - A user may view their own profile.
    - Users with the role 'admin' can view any profile.
    - All other access attempts are denied.

    Security
    --------
    This function implements proper access control (CWE-284) by explicitly checking
    the identity and role of the requesting user before returning sensitive data.
    """
    # Verify that both users exist
    if active_user_id not in USERS or profile_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Retrieve the role of the active user
    active_user_role = USERS[active_user_id].get("role", "")

    # Allow access if the user is requesting their own profile
    if active_user_id == profile_user_id:
        return USER_PROFILES[profile_user_id]

    # Allow access if the user is an administrator
    if active_user_role.lower() == "admin":
        return USER_PROFILES[profile_user_id]

    # Deny all other access attempts
    return "Unauthorized"