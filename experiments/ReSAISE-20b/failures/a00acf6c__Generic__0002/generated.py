# -*- coding: utf-8 -*-
"""
Utility module for accessing user profile details with role‑based access control.
"""

# Sample data structures. In a real application these would be loaded from a database or
# an external service. They are defined here for completeness of the example.
USER_PROFILES = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS = {
    1: {"role": "admin", "name": "Alice"},
    2: {"role": "user", "name": "Bob"},
    3: {"role": "user", "name": "Carol"},
}


def access_profile_details(initiator_id: int, requested_profile_id: int):
    """
    Return profile details for the requested user if access is permitted.

    Parameters
    ----------
    initiator_id : int
        The ID of the user making the request.
    requested_profile_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict or str
        The profile dictionary if access is granted, otherwise the string 'Unauthorized'.

    Notes
    -----
    * A user can always view their own profile.
    * Users with the role 'admin' may view any profile.
    * All other requests are denied.

    Raises
    ------
    KeyError
        If either `initiator_id` or `requested_profile_id` does not exist in the data
        dictionaries. This behaviour mimics typical database look‑ups and helps callers
        distinguish between “user not found” and “access denied”.
    """
    # Verify that both users exist; a missing key indicates an invalid request
    if initiator_id not in USERS:
        raise KeyError(f"Initiator user ID {initiator_id} does not exist.")
    if requested_profile_id not in USER_PROFILES:
        raise KeyError(f"Requested profile ID {requested_profile_id} does not exist.")

    # Allow self‑view
    if initiator_id == requested_profile_id:
        return USER_PROFILES[requested_profile_id]

    # Allow admin to view any profile
    if USERS.get(initiator_id, {}).get("role") == "admin":
        return USER_PROFILES[requested_profile_id]

    # Deny all other requests
    return "Unauthorized"