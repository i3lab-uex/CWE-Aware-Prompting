# -*- coding: utf-8 -*-

"""
User profile access module.

This module provides a function to safely retrieve user profiles
while enforcing proper authorization checks.
"""

# Sample data structures (replace with real data in production)
USER_PROFILES = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS = {
    1: {"username": "alice",   "role": "user"},
    2: {"username": "bob",     "role": "admin"},
    3: {"username": "carol",   "role": "user"},
}


def display_user_profile(active_user_id: int, profile_user_id: int):
    """
    Return the requested user profile if the requesting user is authorized.

    Parameters
    ----------
    active_user_id : int
        ID of the user making the request.
    profile_user_id : int
        ID of the profile being requested.

    Returns
    -------
    dict or str
        The user profile dictionary if access is allowed; otherwise the string 'Unauthorized'.
    """
    # Basic input validation
    if not isinstance(active_user_id, int) or not isinstance(profile_user_id, int):
        return "Unauthorized"

    # Retrieve the active user record
    active_user = USERS.get(active_user_id)
    if not active_user:
        return "Unauthorized"

    # Authorization logic
    is_admin = active_user.get("role") == "admin"
    is_self = active_user_id == profile_user_id

    if not (is_admin or is_self):
        return "Unauthorized"

    # Retrieve the requested profile
    profile = USER_PROFILES.get(profile_user_id)
    if not profile:
        return "Unauthorized"

    # Return a copy to prevent accidental mutation
    return dict(profile)