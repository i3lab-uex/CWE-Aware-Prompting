# -*- coding: utf-8 -*-
"""
Utility module for accessing user profiles with proper access control.
"""

from typing import Dict, Any

# Sample data structures – in a real system these would be fetched from a database.
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Eve",   "email": "eve@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin"},
    2: {"role": "user"},
    3: {"role": "user"},
}

def get_profile_info(acting_user_id: int, viewing_user_id: int) -> Dict[str, Any] | str:
    """
    Return profile details for the requested user if access is allowed.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user making the request.
    viewing_user_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict or str
        Profile dictionary if access is granted, otherwise the string 'Unauthorized'.

    Raises
    ------
    ValueError
        If either user ID is not present in the system.
    """
    # Validate that both users exist
    if acting_user_id not in USERS:
        raise ValueError(f"Acting user ID {acting_user_id} does not exist.")
    if viewing_user_id not in USER_PROFILES:
        raise ValueError(f"Viewing user ID {viewing_user_id} does not exist.")

    # Fetch roles
    acting_role = USERS[acting_user_id].get("role", "user")

    # Access control logic
    if acting_user_id == viewing_user_id or acting_role.lower() == "admin":
        return USER_PROFILES[viewing_user_id]

    # Deny access
    return "Unauthorized"