# -*- coding: utf-8 -*-

"""
Security-aware implementation of user profile access control.

The function checks that the requesting user is either:
* The owner of the requested profile, or
* An administrator (role == 'admin').

If neither condition is met, the function returns the string "Unauthorized".
"""

from typing import Dict, Any

# Example data structures (replace with actual data in production)
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

def display_user_profile(active_user_id: int, profile_user_id: int) -> Any:
    """
    Return the requested user profile if access is authorized.

    Parameters
    ----------
    active_user_id : int
        ID of the user making the request.
    profile_user_id : int
        ID of the profile being requested.

    Returns
    -------
    dict or str
        The user profile dictionary if authorized, otherwise the string "Unauthorized".
    """
    # Validate input IDs
    if active_user_id not in USERS or profile_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Authorization check
    active_user = USERS[active_user_id]
    is_admin = active_user.get("role", "").lower() == "admin"
    if active_user_id != profile_user_id and not is_admin:
        return "Unauthorized"

    # Return a copy to prevent accidental mutation of the global store
    return USER_PROFILES[profile_user_id].copy()