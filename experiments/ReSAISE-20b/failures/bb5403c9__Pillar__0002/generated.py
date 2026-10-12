# -*- coding: utf-8 -*-

"""
Implements get_profile_info with proper access control.
"""

from typing import Dict, Any

# Example data structures (replace or extend as needed)
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


def get_profile_info(acting_user_id: int, viewing_user_id: int) -> Any:
    """
    Return profile details if the acting user is authorized.

    Parameters
    ----------
    acting_user_id : int
        User ID of the requester.
    viewing_user_id : int
        User ID whose profile is being requested.

    Returns
    -------
    dict or str
        The profile dictionary if access is granted; otherwise the string
        "Unauthorized".

    Notes
    -----
    * An admin may view any profile.
    * A non-admin can only view their own profile.
    * If either user ID is unknown, the request is treated as unauthorized.
    """
    # Validate that both IDs exist
    if acting_user_id not in USERS or viewing_user_id not in USER_PROFILES:
        return "Unauthorized"

    acting_role = USERS[acting_user_id].get("role", "").lower()

    # Admins can view any profile
    if acting_role == "admin":
        return USER_PROFILES[viewing_user_id]

    # Non-admins may only view their own profile
    if acting_user_id == viewing_user_id:
        return USER_PROFILES[viewing_user_id]

    # All other cases are unauthorized
    return "Unauthorized"