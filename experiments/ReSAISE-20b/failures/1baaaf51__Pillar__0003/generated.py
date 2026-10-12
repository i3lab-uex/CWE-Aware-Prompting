# -*- coding: utf-8 -*-

"""
User profile access module.

This module implements a secure function to allow users to view their own
profile or, if they have the `admin` role, any other user's profile.
It guards against CWE-284: Improper Access Control by strictly checking
the active user’s identity and role before granting access.
"""

from typing import Dict, Any

# Sample data structures. In a real application these would be fetched
# from a database or an external service.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"email": "alice@example.com", "age": 30},
    2: {"email": "bob@example.com",   "age": 25},
    3: {"email": "carol@example.com", "age": 28},
}


def access_user_profile(active_user_id: int, profile_id: int) -> Any:
    """
    Return the requested user profile if access is authorized.

    Parameters
    ----------
    active_user_id : int
        The ID of the user making the request.
    profile_id : int
        The ID of the profile to retrieve.

    Returns
    -------
    dict or str
        The requested user profile dictionary if access is granted,
        otherwise the string 'Unauthorized'.

    Notes
    -----
    - A user may view their own profile.
    - An admin (role == 'admin') may view any profile.
    - All other attempts result in 'Unauthorized'.
    """
    # Validate that both users exist
    if active_user_id not in USERS or profile_id not in USER_PROFILES:
        return "Unauthorized"

    # Check if the active user is requesting their own profile
    if active_user_id == profile_id:
        return USER_PROFILES[profile_id]

    # Retrieve the role of the active user
    active_role = USERS.get(active_user_id, {}).get("role", "")

    # Allow admin to view any profile
    if active_role.lower() == "admin":
        return USER_PROFILES[profile_id]

    # All other cases are denied
    return "Unauthorized"


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    print(access_user_profile(1, 2))   # Admin viewing Bob's profile
    print(access_user_profile(2, 2))   # Bob viewing his own profile
    print(access_user_profile(2, 1))   # Bob attempting to view Alice's profile