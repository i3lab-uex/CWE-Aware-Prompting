# -*- coding: utf-8 -*-

"""
Module providing secure access to user profile details.
"""

from typing import Dict, Any

# Example data structures (replace with real data in production)
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

def access_profile_details(initiator_id: int, requested_profile_id: int) -> Any:
    """
    Return profile details for the requested user if access is authorized.

    Parameters
    ----------
    initiator_id : int
        The user ID of the individual making the request.
    requested_profile_id : int
        The user ID of the profile being requested.

    Returns
    -------
    dict or str
        The profile dictionary if access is granted; otherwise the string
        'Unauthorized'.
    """
    # Validate that both users exist
    if initiator_id not in USERS or requested_profile_id not in USER_PROFILES:
        return "Unauthorized"

    # Check if the initiator is requesting their own profile
    if initiator_id == requested_profile_id:
        return USER_PROFILES[requested_profile_id]

    # Check if the initiator has admin privileges
    initiator_role = USERS[initiator_id].get("role", "")
    if initiator_role.lower() == "admin":
        return USER_PROFILES[requested_profile_id]

    # Access denied
    return "Unauthorized"