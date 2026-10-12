# -*- coding: utf-8 -*-

from typing import Any, Dict

# Example data structures (replace with real data in production)
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


def see_user_profile(current_id: int, target_id: int) -> Any:
    """
    Return the profile of `target_id` if the requester (`current_id`) is authorized.
    Authorization rules:
      * A user can view their own profile.
      * An admin (role == 'admin') can view any user's profile.

    Parameters
    ----------
    current_id : int
        The ID of the user making the request.
    target_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict or str
        The requested user profile if access is allowed, otherwise the string 'Unauthorized'.
    """
    # Basic sanity checks
    if not isinstance(current_id, int) or not isinstance(target_id, int):
        return "Unauthorized"

    # Verify both IDs exist in the system
    if current_id not in USERS or target_id not in USER_PROFILES:
        return "Unauthorized"

    # Self-access
    if current_id == target_id:
        return USER_PROFILES[target_id]

    # Admin access
    current_user = USERS[current_id]
    if current_user.get("role") == "admin":
        return USER_PROFILES[target_id]

    # All other cases are unauthorized
    return "Unauthorized"