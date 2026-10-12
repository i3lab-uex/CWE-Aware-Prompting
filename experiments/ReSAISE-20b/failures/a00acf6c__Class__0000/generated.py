# -*- coding: utf-8 -*-
"""
Module providing access control for user profile details.

The `access_profile_details` function checks that the requestor is either
the owner of the profile or an administrator before returning the profile.
"""

from typing import Dict, Any

# Example data structures (these would normally be populated elsewhere)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "user"},
    2: {"role": "admin"},
}


def access_profile_details(initiator_id: int, requested_profile_id: int) -> Any:
    """
    Return the profile details for `requested_profile_id` if the initiator
    is authorized to view it.

    Parameters
    ----------
    initiator_id : int
        The user ID of the person making the request.
    requested_profile_id : int
        The user ID whose profile is being requested.

    Returns
    -------
    dict or str
        A copy of the profile dictionary if access is granted; otherwise
        the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either `initiator_id` or `requested_profile_id` is not present in the
        USERS or USER_PROFILES dictionaries, respectively.
    """
    # Ensure both users exist
    if initiator_id not in USERS:
        raise KeyError(f"Initiator ID {initiator_id} does not exist.")
    if requested_profile_id not in USER_PROFILES:
        raise KeyError(f"Requested profile ID {requested_profile_id} does not exist.")

    # Authorization: owner or admin
    initiator_role = USERS[initiator_id].get("role", "")
    if initiator_id != requested_profile_id and initiator_role.lower() != "admin":
        return "Unauthorized"

    # Return a shallow copy to prevent accidental mutation
    profile = USER_PROFILES[requested_profile_id]
    return dict(profile)