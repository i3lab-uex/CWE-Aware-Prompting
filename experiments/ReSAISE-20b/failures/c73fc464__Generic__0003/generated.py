# -*- coding: utf-8 -*-

"""
Implementation of fetch_profile_data

The function checks whether the requester has permission to view
the requested profile.  Permission is granted if:
* The requester is an administrator (role == 'admin')
* OR the requester is requesting their own profile.

The function returns the profile dictionary if access is granted,
otherwise it returns the string 'Unauthorized'.
"""

from typing import Dict, Any

# Example data structures (these would normally be provided elsewhere)
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

def fetch_profile_data(requester_id: int, profile_id: int) -> Any:
    """
    Return the profile details for *profile_id* if the request
    originates from an admin or the user themselves.

    Parameters:
        requester_id (int): ID of the user making the request.
        profile_id   (int): ID of the profile being requested.

    Returns:
        dict: The profile details if access is granted.
        str : 'Unauthorized' otherwise.

    Raises:
        KeyError: If either user ID is not present in the data.
    """
    # Validate that both users exist
    if requester_id not in USERS:
        raise KeyError(f"Requester ID {requester_id} does not exist.")
    if profile_id not in USER_PROFILES:
        raise KeyError(f"Profile ID {profile_id} does not exist.")

    requester_role = USERS[requester_id].get("role", "user")

    # Permission check
    if requester_role == "admin" or requester_id == profile_id:
        return USER_PROFILES[profile_id]

    # Access denied
    return "Unauthorized"