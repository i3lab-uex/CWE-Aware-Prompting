# -*- coding: utf-8 -*-

from typing import Any, Dict

# Sample data structures (replace with real ones in your application)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"email": "alice@example.com", "bio": "Admin of the system"},
    2: {"email": "bob@example.com",   "bio": "Regular user"},
    3: {"email": "carol@example.com", "bio": "Another regular user"},
}


def get_user_profile(actor_user_id: int, requested_user_id: int) -> Dict[str, Any] | str:
    """
    Return the profile of `requested_user_id` if the caller (`actor_user_id`) is
    authorized to view it.  An admin may view any profile; a regular user can only
    view their own.

    Parameters
    ----------
    actor_user_id : int
        ID of the user making the request.
    requested_user_id : int
        ID of the profile being requested.

    Returns
    -------
    dict | str
        The profile dictionary if access is allowed, otherwise the string
        'Unauthorized'.

    Raises
    ------
    KeyError
        If either the actor or requested user does not exist in USERS/USER_PROFILES.
    """
    # Validate existence of users
    if actor_user_id not in USERS:
        raise KeyError(f"Actor user ID {actor_user_id} does not exist.")
    if requested_user_id not in USER_PROFILES:
        raise KeyError(f"Requested user ID {requested_user_id} does not exist.")

    actor = USERS[actor_user_id]
    # Admins can view any profile
    if actor.get("role") == "admin":
        return USER_PROFILES[requested_user_id]

    # Regular users can only view their own profile
    if actor_user_id == requested_user_id:
        return USER_PROFILES[requested_user_id]

    # All other cases are unauthorized
    return "Unauthorized"


# Example usage (uncomment to test)
# print(get_user_profile(1, 2))   # admin viewing Bob's profile
# print(get_user_profile(2, 3))   # unauthorized
# print(get_user_profile(2, 2))   # Bob viewing his own profile