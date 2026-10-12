# -*- coding: utf-8 -*-

"""
Utility for retrieving user profile data with role-based access control.
"""

# Example data structures (replace with real data sources in production)
USER_PROFILES = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Eve",   "email": "eve@example.com"},
}

USERS = {
    1: {"role": "admin",   "name": "Alice"},
    2: {"role": "user",    "name": "Bob"},
    3: {"role": "moderator","name":"Eve"},
}

def fetch_profile_data(requester_id: int, profile_id: int):
    """
    Retrieve a user profile if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The ID of the user making the request.
    profile_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict | str
        The requested profile data if access is granted, otherwise the string
        'Unauthorized'.

    Raises
    ------
    ValueError
        If either user ID does not exist in the system.
    """
    # Validate that both IDs are present
    if requester_id not in USERS:
        raise ValueError(f"Requester ID {requester_id} does not exist.")
    if profile_id not in USER_PROFILES:
        raise ValueError(f"Profile ID {profile_id} does not exist.")

    # Grant access if the requester is viewing their own profile
    if requester_id == profile_id:
        return USER_PROFILES[profile_id]

    # Grant access if the requester has an admin role
    requester_role = USERS[requester_id].get("role", "").lower()
    if requester_role == "admin":
        return USER_PROFILES[profile_id]

    # All other cases are unauthorized
    return "Unauthorized"