# -*- coding: utf-8 -*-

"""
Implementation of a secure user profile access function.
"""

from typing import Dict, Any

# Example data structures (replace with real data in production)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"username": "alice",   "role": "user"},
    2: {"username": "bob",     "role": "admin"},
}


def access_user_profile(requesting_user_id: int, viewing_user_id: int) -> Any:
    """
    Return the profile of `viewing_user_id` if the requesting user is allowed to view it.
    A user can always view their own profile; an admin can view any profile.

    Parameters
    ----------
    requesting_user_id : int
        ID of the user making the request.
    viewing_user_id : int
        ID of the profile being requested.

    Returns
    -------
    dict or str
        The user profile if access is granted, otherwise the string 'Unauthorized'.

    Raises
    ------
    ValueError
        If either user ID does not exist in the system.
    """
    # Validate that both users exist
    if requesting_user_id not in USERS:
        raise ValueError(f"Requesting user ID {requesting_user_id} does not exist.")
    if viewing_user_id not in USER_PROFILES:
        raise ValueError(f"Viewing user ID {viewing_user_id} does not exist.")

    # Retrieve the requesting user's role
    requester_role = USERS[requesting_user_id].get("role", "user")

    # Access control logic
    if requesting_user_id == viewing_user_id or requester_role.lower() == "admin":
        return USER_PROFILES[viewing_user_id]

    # If no permission, return Unauthorized
    return "Unauthorized"