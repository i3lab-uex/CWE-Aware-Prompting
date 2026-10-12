# -*- coding: utf-8 -*-
"""
Utility module for user profile access.
"""

from typing import Any, Dict

# Example data structures. In a real application these would be loaded from a database.
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin"},
    2: {"role": "user"},
    3: {"role": "user"},
}


def get_profile_info(acting_user_id: int, viewing_user_id: int) -> Any:
    """
    Return the profile details for `viewing_user_id` if the request is authorized.

    Parameters
    ----------
    acting_user_id : int
        The user ID of the individual making the request.
    viewing_user_id : int
        The user ID whose profile is being requested.

    Returns
    -------
    dict | str
        The profile dictionary if access is granted, otherwise the string 'Unauthorized'.

    Notes
    -----
    - A user can view their own profile.
    - Users with the role 'admin' may view any user's profile.
    - All other requests are denied.

    Raises
    ------
    KeyError
        If either the acting user or the profile being viewed does not exist.
    """
    # Validate existence of both users
    if acting_user_id not in USERS:
        raise KeyError(f"Acting user ID {acting_user_id} does not exist.")
    if viewing_user_id not in USER_PROFILES:
        raise KeyError(f"Profile for user ID {viewing_user_id} does not exist.")

    # Authorization check
    if acting_user_id == viewing_user_id:
        return USER_PROFILES[viewing_user_id]

    acting_role = USERS[acting_user_id].get("role", "")
    if acting_role == "admin":
        return USER_PROFILES[viewing_user_id]

    # Access denied
    return "Unauthorized"