# access_profile_details.py

from __future__ import annotations
from typing import Dict, Any

# Example data structures (replace with actual data in production)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    # ... more profiles
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin"},
    2: {"role": "user"},
    # ... more users
}


def access_profile_details(initiator_id: int, requested_profile_id: int) -> Dict[str, Any] | str:
    """
    Return the profile details if access is allowed.

    Parameters
    ----------
    initiator_id : int
        The user ID of the individual making the request.
    requested_profile_id : int
        The user ID of the profile being requested.

    Returns
    -------
    dict or str
        Profile details dictionary if access is granted, otherwise the string
        'Unauthorized'.
    """
    # Validate input types
    if not isinstance(initiator_id, int) or not isinstance(requested_profile_id, int):
        return "Unauthorized"

    # Check that both users exist
    initiator = USERS.get(initiator_id)
    requested_profile = USER_PROFILES.get(requested_profile_id)

    if initiator is None or requested_profile is None:
        return "Unauthorized"

    # Only admins can view other users' profiles
    if initiator_id == requested_profile_id:
        return requested_profile

    # Admin check
    if initiator.get("role") == "admin":
        return requested_profile

    # Default: unauthorized
    return "Unauthorized"