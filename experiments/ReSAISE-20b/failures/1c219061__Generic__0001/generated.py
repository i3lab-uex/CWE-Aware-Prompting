# -*- coding: utf-8 -*-

"""
User profile access control module.
"""

from typing import Dict, Any

# Sample data structures (replace with real data in production)
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


def get_user_profile(actor_user_id: int, requested_user_id: int) -> Any:
    """
    Return the profile of `requested_user_id` if the caller is allowed to view it.

    Parameters
    ----------
    actor_user_id : int
        The ID of the user making the request.
    requested_user_id : int
        The ID of the profile to retrieve.

    Returns
    -------
    dict | str
        The requested user's profile dictionary if authorized,
        otherwise the string 'Unauthorized'.

    Notes
    -----
    - A user can view their own profile.
    - Users with the role 'admin' can view any profile.
    - If either user ID is unknown, access is denied.
    """
    # Verify both users exist
    if actor_user_id not in USERS or requested_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Allow self-access
    if actor_user_id == requested_user_id:
        return USER_PROFILES[requested_user_id]

    # Allow admin access
    actor_role = USERS.get(actor_user_id, {}).get("role", "")
    if actor_role == "admin":
        return USER_PROFILES[requested_user_id]

    # Default: deny access
    return "Unauthorized"