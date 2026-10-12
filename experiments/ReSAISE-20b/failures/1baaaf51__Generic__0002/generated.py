# -*- coding: utf-8 -*-

"""
Utility for accessing user profiles with role‑based access control.

The module defines a single public function `access_user_profile` that
enforces the following rules:

1. A user may view their own profile.
2. An administrator (role == "admin") may view any user's profile.
3. All other attempts result in the string 'Unauthorized'.

Missing users or profiles raise a `KeyError` to signal an invalid request.
"""

from __future__ import annotations

# Example data structures – replace with your actual data sources
USERS = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES = {
    1: {"email": "alice@example.com", "bio": "Admin of the system."},
    2: {"email": "bob@example.com",   "bio": "Regular user."},
    3: {"email": "carol@example.com", "bio": "Another regular user."},
}


def access_user_profile(active_user_id: int, profile_id: int) -> dict | str:
    """
    Return the requested user profile if access is permitted.

    Parameters
    ----------
    active_user_id : int
        ID of the user making the request.
    profile_id : int
        ID of the profile being requested.

    Returns
    -------
    dict | str
        The profile dictionary if access is allowed, otherwise the string
        'Unauthorized'.

    Raises
    ------
    KeyError
        If either the active user or requested profile does not exist.
    """
    # Validate existence of users
    if active_user_id not in USERS:
        raise KeyError(f"Active user ID {active_user_id} does not exist.")
    if profile_id not in USER_PROFILES:
        raise KeyError(f"Profile ID {profile_id} does not exist.")

    # Own profile: always allowed
    if active_user_id == profile_id:
        return USER_PROFILES[profile_id]

    # Admin privilege check
    if USERS.get(active_user_id, {}).get("role") == "admin":
        return USER_PROFILES[profile_id]

    # All other cases are forbidden
    return "Unauthorized"