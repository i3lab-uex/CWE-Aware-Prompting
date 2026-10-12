# -*- coding: utf-8 -*-
"""
User profile access module.

This module implements the `access_user_profile` function that enforces
proper authorization checks before returning a user's profile.
"""

from typing import Dict, Any

# Sample data structures. In real usage these would be populated from a database.
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"username": "alice", "role": "user"},
    2: {"username": "bob",   "role": "admin"},
    3: {"username": "carol", "role": "user"},
}


def access_user_profile(requesting_user_id: int, viewing_user_id: int) -> Any:
    """
    Return the profile of `viewing_user_id` if the request is authorized.

    Parameters
    ----------
    requesting_user_id : int
        ID of the user making the request.
    viewing_user_id : int
        ID of the profile being requested.

    Returns
    -------
    dict | str
        The user profile dictionary if access is granted; otherwise the string
        'Unauthorized'.

    Notes
    -----
    - A user can view their own profile.
    - An administrator (role == 'admin') can view any user's profile.
    - If the requesting user ID does not exist in USERS, access is denied.
    """
    # Verify that both users exist
    if requesting_user_id not in USERS or viewing_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Fetch role of the requesting user
    requester_role = USERS[requesting_user_id].get("role", "")

    # Authorization logic
    if requesting_user_id == viewing_user_id:
        return USER_PROFILES[viewing_user_id]
    if requester_role.lower() == "admin":
        return USER_PROFILES[viewing_user_id]

    # If none of the conditions are met, deny access
    return "Unauthorized"


# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(access_user_profile(1, 1))   # Alice viewing own profile
    print(access_user_profile(2, 3))   # Admin Bob viewing Carol's profile
    print(access_user_profile(1, 2))   # Alice trying to view Bob's profile (should be denied)