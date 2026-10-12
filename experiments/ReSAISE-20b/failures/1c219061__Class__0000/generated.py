# -*- coding: utf-8 -*-

"""
User profile access module.

The `get_user_profile` function ensures that only the owner of a profile
or an administrator can retrieve profile information. It performs both
authentication (by checking that the actor exists) and authorization
(CWE-862: Missing Authorization).

Author: ChatGPT
"""

from typing import Any, Dict

# Example data structures. In a real application these would be replaced
# with database queries or ORM models.
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

def get_user_profile(actor_user_id: int, requested_user_id: int) -> Any:
    """
    Retrieve a user's profile if the requesting actor is authorized.

    Parameters
    ----------
    actor_user_id : int
        ID of the user making the request.
    requested_user_id : int
        ID of the profile to retrieve.

    Returns
    -------
    dict | str
        The requested user's profile dictionary if access is granted,
        otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either the actor or requested user does not exist in the system.
    """
    # Verify that both users exist
    if actor_user_id not in USERS:
        raise KeyError(f"Actor user ID {actor_user_id} does not exist.")
    if requested_user_id not in USER_PROFILES:
        raise KeyError(f"Requested user ID {requested_user_id} does not exist.")

    actor = USERS[actor_user_id]
    # Authorization check: allow if the actor is the owner or an admin
    if actor_user_id == requested_user_id or actor.get("role") == "admin":
        return USER_PROFILES[requested_user_id]

    # If we reach this point, the actor is not authorized
    return "Unauthorized"