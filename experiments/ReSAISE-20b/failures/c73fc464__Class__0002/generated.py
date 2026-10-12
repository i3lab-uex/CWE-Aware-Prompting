# -*- coding: utf-8 -*-
"""
Utility module for user profile retrieval with proper authorization checks.
"""

from typing import Dict, Any

# Example data structures. In a real application these would come from a database.
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "user"},
    2: {"role": "admin"},
    3: {"role": "user"},
}

def fetch_profile_data(requester_id: int, profile_id: int) -> Any:
    """
    Retrieve a user profile if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The user ID of the individual making the request.
    profile_id : int
        The user ID whose profile is being requested.

    Returns
    -------
    dict or str
        The requested profile data if access is granted, otherwise the string
        'Unauthorized'.

    Raises
    ------
    ValueError
        If either requester_id or profile_id does not exist in the system.
    """
    # Validate existence of both users
    if requester_id not in USERS:
        raise ValueError(f"Requester ID {requester_id} does not exist.")
    if profile_id not in USER_PROFILES:
        raise ValueError(f"Profile ID {profile_id} does not exist.")

    requester_role = USERS[requester_id].get("role", "")

    # Authorization logic
    is_self = requester_id == profile_id
    is_admin = requester_role.lower() == "admin"

    if not (is_self or is_admin):
        return "Unauthorized"

    # Return a copy to prevent accidental mutation of the original data
    return USER_PROFILES[profile_id].copy()