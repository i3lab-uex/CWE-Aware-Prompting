# -*- coding: utf-8 -*-

from typing import Dict, Any

# Example data structures (replace with real data in production)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"username": "alice",   "role": "user"},
    2: {"username": "bob",     "role": "admin"},
    3: {"username": "carol",   "role": "user"},
}


def display_user_profile(active_user_id: int, profile_user_id: int) -> Any:
    """
    Return the profile of *profile_user_id* if the requesting user
    (*active_user_id*) has permission to view it.

    Permission rules:
        - A user can view their own profile.
        - An admin (role == 'admin') can view any user's profile.

    Parameters
    ----------
    active_user_id : int
        ID of the user making the request.
    profile_user_id : int
        ID of the profile being requested.

    Returns
    -------
    dict | str
        The requested user profile if access is allowed, otherwise the string
        'Unauthorized'.
    """
    # Validate that both users exist
    if active_user_id not in USERS or profile_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Check if the active user is allowed to view the requested profile
    if active_user_id == profile_user_id:
        return USER_PROFILES[profile_user_id]

    # Check for admin role
    if USERS.get(active_user_id, {}).get("role") == "admin":
        return USER_PROFILES[profile_user_id]

    # If none of the conditions are met, deny access
    return "Unauthorized"