# -*- coding: utf-8 -*-
"""
Utility for retrieving user profiles with proper authorization checks.
"""

from typing import Dict, Any

# Sample data structures – in a real application these would come from a database or
# an external service.  They are defined here for completeness of the example.
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Eve",   "email": "eve@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"username": "alice",   "role": "user"},
    2: {"username": "bob",     "role": "admin"},
    3: {"username": "eve",     "role": "user"},
}


def see_user_profile(current_id: int, target_id: int) -> Dict[str, Any] | str:
    """
    Return the profile of *target_id* if the caller (*current_id*) is authorized.

    Authorization rules:
      - A user may view their own profile.
      - An administrator (role == "admin") may view any profile.

    Parameters
    ----------
    current_id : int
        The ID of the user making the request.
    target_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict or str
        The target user's profile dictionary if access is granted, otherwise the string
        'Unauthorized'.
    """
    # Validate that both users exist
    if current_id not in USERS or target_id not in USER_PROFILES:
        return "Unauthorized"

    # Fetch the current user's role
    current_role = USERS[current_id].get("role", "")

    # Authorization check
    if current_id == target_id or current_role.lower() == "admin":
        return USER_PROFILES[target_id]

    # Deny access
    return "Unauthorized"