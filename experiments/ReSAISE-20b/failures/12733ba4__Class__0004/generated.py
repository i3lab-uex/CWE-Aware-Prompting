# -*- coding: utf-8 -*-

"""
User profile access module.
Author: ChatGPT
"""

from typing import Dict, Any

# Sample data – in a real application these would come from a database.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"bio": "Admin of the system",   "email": "alice@example.com"},
    2: {"bio": "Developer",            "email": "bob@example.com"},
    3: {"bio": "Designer",             "email": "carol@example.com"},
}


def display_user_profile(active_user_id: int, profile_user_id: int) -> Dict[str, Any] | str:
    """
    Return the requested user profile if the caller is authorized.

    Parameters
    ----------
    active_user_id : int
        The ID of the user making the request.
    profile_user_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict or str
        The user profile dictionary if access is allowed,
        otherwise the string 'Unauthorized'.
    """
    # Validate input: check that both IDs exist in our data structures.
    if active_user_id not in USERS or profile_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Authorization check: allow if the user is viewing their own profile
    # or if they have an admin role.
    active_user = USERS[active_user_id]
    is_admin = active_user.get("role") == "admin"
    if active_user_id != profile_user_id and not is_admin:
        return "Unauthorized"

    # Return a copy of the profile to avoid accidental mutation.
    return USER_PROFILES[profile_user_id].copy()