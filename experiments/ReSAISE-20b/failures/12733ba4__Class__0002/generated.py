# -*- coding: utf-8 -*-

"""
Utility module for user profile access.
"""

from typing import Dict, Any

# Sample data structures – replace with real ones in production
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"username": "alice",   "role": "user"},
    2: {"username": "bob",     "role": "admin"},
}


def display_user_profile(active_user_id: int, profile_user_id: int) -> Any:
    """
    Return the requested user profile if access is authorized.

    Parameters
    ----------
    active_user_id : int
        The ID of the user making the request.
    profile_user_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict | str
        The user profile dictionary if access is granted,
        otherwise the string 'Unauthorized'.

    Notes
    -----
    Authorization logic:
      * A user may view their own profile.
      * An administrator (role == 'admin') may view any profile.

    Raises
    ------
    KeyError
        If either the active user or requested profile does not exist.
    """
    # Validate that both users exist
    if active_user_id not in USERS:
        raise KeyError(f"Active user ID {active_user_id} does not exist.")
    if profile_user_id not in USER_PROFILES:
        raise KeyError(f"Profile user ID {profile_user_id} does not exist.")

    # Fetch the active user's role
    active_role = USERS[active_user_id].get("role", "user")

    # Authorization check
    if active_user_id == profile_user_id or active_role.lower() == "admin":
        return USER_PROFILES[profile_user_id]

    # Deny access
    return "Unauthorized"