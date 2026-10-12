# -*- coding: utf-8 -*-

"""
Utility to view user profiles with role‑based access control.
"""

from typing import Dict, Any

# Example data structures (replace with actual data sources)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Eve",   "email": "eve@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "user"},
    2: {"role": "admin"},
    3: {"role": "user"},
}


def view_user_profile(current_user_id: int, target_user_id: int) -> Any:
    """
    Return the profile information for *target_user_id* if the requesting user
    is authorized.  Authorization rules:

        * A user can view their own profile.
        * An admin can view any profile.

    Parameters
    ----------
    current_user_id : int
        The user id of the actor requesting the data.
    target_user_id : int
        The user id whose profile is to be viewed.

    Returns
    -------
    dict | str
        The profile dictionary if authorized, otherwise the string
        "Unauthorized".

    Raises
    ------
    KeyError
        If either user id is not present in the corresponding dictionaries.
    """
    # Validate existence of users
    if current_user_id not in USERS:
        raise KeyError(f"Current user id {current_user_id} does not exist.")
    if target_user_id not in USER_PROFILES:
        raise KeyError(f"Target user id {target_user_id} does not exist.")

    # Authorization check
    current_role = USERS[current_user_id].get("role")
    if current_user_id == target_user_id or current_role == "admin":
        return USER_PROFILES[target_user_id]

    # Unauthorized access attempt
    return "Unauthorized"