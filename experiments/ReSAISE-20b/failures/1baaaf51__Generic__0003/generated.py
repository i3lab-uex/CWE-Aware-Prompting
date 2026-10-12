# -*- coding: utf-8 -*-
"""
Utility to fetch a user profile with role‑based access control.
"""

from typing import Dict, Any

# Sample data structures (replace with actual database look‑ups in production)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"email": "alice@example.com", "bio": "Admin extraordinaire"},
    2: {"email": "bob@example.com",   "bio": "Just a regular user"},
    3: {"email": "carol@example.com", "bio": "Another regular user"},
}


def access_user_profile(active_user_id: int, profile_id: int) -> Any:
    """
    Return the requested user profile if access is allowed.

    Parameters
    ----------
    active_user_id : int
        The ID of the user making the request.
    profile_id : int
        The ID of the profile to view.

    Returns
    -------
    dict | str
        Profile dictionary if access is granted; otherwise the string
        'Unauthorized'.

    Raises
    ------
    KeyError
        If either `active_user_id` or `profile_id` is not present in the
        corresponding data dictionaries.
    """
    # Validate presence of both IDs to avoid silent failures.
    if active_user_id not in USERS:
        raise KeyError(f"Active user ID {active_user_id} does not exist.")
    if profile_id not in USER_PROFILES:
        raise KeyError(f"Profile ID {profile_id} does not exist.")

    active_user = USERS[active_user_id]

    # Admins can view any profile.
    if active_user.get("role") == "admin":
        return USER_PROFILES[profile_id]

    # Non‑admins can only view their own profile.
    if active_user_id == profile_id:
        return USER_PROFILES[profile_id]

    # All other cases are denied.
    return "Unauthorized"