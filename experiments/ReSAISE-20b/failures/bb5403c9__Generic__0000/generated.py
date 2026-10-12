# -*- coding: utf-8 -*-
"""
Utility module for user profile access control.
"""

from typing import Dict, Any

# Example data structures – in a real application these would be populated from a database
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
    Return the profile details for *viewing_user_id* if the requesting user (*acting_user_id*)
    is allowed to view it.

    Access rules:
        * A user may always view their own profile.
        * An administrator (role == 'admin') may view any profile.
        * All other requests are denied.

    Parameters
    ----------
    acting_user_id : int
        The user id of the person making the request.
    viewing_user_id : int
        The user id whose profile is being requested.

    Returns
    -------
    dict | str
        Profile dictionary if access is granted, otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either user id is not present in the data stores.
    """
    # Validate that both users exist
    if acting_user_id not in USERS:
        raise KeyError(f"Acting user id {acting_user_id} does not exist.")
    if viewing_user_id not in USER_PROFILES:
        raise KeyError(f"Viewing user id {viewing_user_id} does not exist.")

    # Check if the acting user is an admin
    acting_role = USERS[acting_user_id].get("role")
    if acting_role == "admin":
        return USER_PROFILES[viewing_user_id]

    # If not an admin, the user may only view their own profile
    if acting_user_id == viewing_user_id:
        return USER_PROFILES[viewing_user_id]

    # All other cases are unauthorized
    return "Unauthorized"