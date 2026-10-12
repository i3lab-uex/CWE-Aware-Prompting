# -*- coding: utf-8 -*-

"""
Secure profile retrieval module.
"""

from typing import Any, Dict

# Sample data structures (replace with real ones in production)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"email": "alice@example.com", "bio": "Admin"},
    2: {"email": "bob@example.com",   "bio": "Developer"},
    3: {"email": "carol@example.com", "bio": "Designer"},
}


def get_user_profile(actor_user_id: int, requested_user_id: int) -> Dict[str, Any] | str:
    """
    Return the profile of `requested_user_id` if the requesting user
    has permission.  An admin may view any profile; a regular user may only
    view their own profile.

    Parameters
    ----------
    actor_user_id : int
        ID of the user making the request.
    requested_user_id : int
        ID of the profile to view.

    Returns
    -------
    dict or str
        The requested user's profile dictionary if authorized,
        otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either user ID is not present in the data structures.
    """
    # Validate that both users exist
    if actor_user_id not in USERS:
        raise KeyError(f"Actor user ID {actor_user_id} does not exist.")
    if requested_user_id not in USER_PROFILES:
        raise KeyError(f"Requested user ID {requested_user_id} does not exist.")

    actor_role = USERS[actor_user_id].get("role", "user")

    # Authorization logic
    if actor_role == "admin" or actor_user_id == requested_user_id:
        # Return a copy to prevent accidental mutation
        return dict(USER_PROFILES[requested_user_id])

    # Unauthorized access attempt
    return "Unauthorized"