# -*- coding: utf-8 -*-
"""
Utility to fetch user profiles with proper access control.

The module defines `display_user_profile`, which checks that the requesting
user is either viewing their own profile or has an administrative role.
"""

from __future__ import annotations

# Example data structures; replace with real database lookups in production.
USER_PROFILES: dict[int, dict] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS: dict[int, dict] = {
    1: {"username": "alice",   "role": "user"},
    2: {"username": "bob",     "role": "admin"},
    3: {"username": "carol",   "role": "user"},
}


def display_user_profile(active_user_id: int, profile_user_id: int) -> dict | str:
    """
    Return the requested user profile if access is permitted.

    Parameters
    ----------
    active_user_id : int
        The ID of the user making the request.
    profile_user_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict | str
        The user profile dictionary if the caller is authorized,
        otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either user ID does not exist in the system.
    """
    # Validate that both users exist
    if active_user_id not in USERS:
        raise KeyError(f"Active user ID {active_user_id} does not exist.")
    if profile_user_id not in USER_PROFILES:
        raise KeyError(f"Profile user ID {profile_user_id} does not exist.")

    # Access control: allow self-view or admin role
    active_role = USERS[active_user_id].get("role", "user")
    if active_user_id != profile_user_id and active_role.lower() != "admin":
        return "Unauthorized"

    # Return a copy to prevent accidental mutation of the stored profile
    return USER_PROFILES[profile_user_id].copy()


# Example usage (commented out; remove comments to run):
# print(display_user_profile(1, 1))   # Alice viewing own profile
# print(display_user_profile(2, 3))   # Admin Bob viewing Carol's profile
# print(display_user_profile(1, 2))   # Alice attempting to view Bob's profile -> Unauthorized