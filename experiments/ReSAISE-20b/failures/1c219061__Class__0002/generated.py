# -*- coding: utf-8 -*-
"""
Implementation of a simple user profile access control.
"""

from typing import Dict, Any

# Example data structures (in real applications these would be loaded from a database)
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

def get_user_profile(actor_user_id: int, requested_user_id: int) -> Any:
    """
    Return the profile information of the requested user if the actor is authorized.
    
    Parameters
    ----------
    actor_user_id : int
        ID of the user making the request.
    requested_user_id : int
        ID of the profile to retrieve.

    Returns
    -------
    dict or str
        The requested user's profile dictionary if access is granted,
        otherwise the string 'Unauthorized'.
    """
    # Basic sanity checks
    if actor_user_id not in USERS or requested_user_id not in USER_PROFILES:
        return "Unauthorized"

    actor = USERS[actor_user_id]
    # Authorization logic
    if actor_user_id == requested_user_id or actor.get("role") == "admin":
        return USER_PROFILES[requested_user_id]
    
    return "Unauthorized"