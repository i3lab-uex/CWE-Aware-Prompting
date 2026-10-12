# -*- coding: utf-8 -*-
"""
User profile access module.

This module defines a single function `get_user_profile` that returns the
profile of a requested user if the actor has sufficient permissions.
"""

from typing import Dict, Any

# Example data structures – replace with real ones in production
USERS: Dict[int, Dict[str, Any]] = {
    # user_id : { "name": str, "role": str }
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    # user_id : { profile fields }
    1: {"email": "alice@example.com", "age": 30},
    2: {"email": "bob@example.com",   "age": 25},
    3: {"email": "carol@example.com","age": 28},
}

def get_user_profile(actor_user_id: int, requested_user_id: int) -> Any:
    """
    Return the profile of `requested_user_id` if the actor has permission.

    Parameters
    ----------
    actor_user_id : int
        The ID of the user making the request.
    requested_user_id : int
        The ID of the profile to be retrieved.

    Returns
    -------
    dict or str
        The requested user's profile dictionary if access is allowed,
        otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either user ID does not exist in the USERS or USER_PROFILES data.
    """
    # Validate existence of both users
    if actor_user_id not in USERS:
        raise KeyError(f"Actor user ID {actor_user_id} does not exist.")
    if requested_user_id not in USER_PROFILES:
        raise KeyError(f"Requested user ID {requested_user_id} does not exist.")

    actor_role = USERS[actor_user_id].get("role", "").lower()

    # Permission check: admin can view any profile; users can only view their own
    if actor_role == "admin" or actor_user_id == requested_user_id:
        return USER_PROFILES[requested_user_id]

    # Deny access
    return "Unauthorized"