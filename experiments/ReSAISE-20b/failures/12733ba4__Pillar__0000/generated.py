# -*- coding: utf-8 -*-
"""
Module providing secure user profile access.
"""

from typing import Dict, Any

# Example data structures (replace with actual application data)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "user"},
    3: {"username": "charlie", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"full_name": "Alice Smith",   "email": "alice@example.com"},
    2: {"full_name": "Bob Jones",     "email": "bob@example.com"},
    3: {"full_name": "Charlie Brown", "email": "charlie@example.com"},
}


def display_user_profile(active_user_id: int, profile_user_id: int) -> Any:
    """
    Return the requested user profile if the active user is allowed to view it.
    An admin can view any profile. A regular user can only view their own profile.

    Args:
        active_user_id: ID of the user making the request.
        profile_user_id: ID of the profile being requested.

    Returns:
        The user profile dictionary if access is granted, otherwise the string
        'Unauthorized'.

    Raises:
        KeyError: If either user ID does not exist in the system.
    """
    # Validate that both users exist
    if active_user_id not in USERS:
        raise KeyError(f"Active user ID {active_user_id} does not exist.")
    if profile_user_id not in USER_PROFILES:
        raise KeyError(f"Profile user ID {profile_user_id} does not exist.")

    active_user = USERS[active_user_id]
    # Check for admin role or self-access
    if active_user.get("role") == "admin" or active_user_id == profile_user_id:
        return USER_PROFILES[profile_user_id]

    # Access denied
    return "Unauthorized"