# -*- coding: utf-8 -*-

"""
User profile access control module.

This module provides the `fetch_profile_data` function which enforces
authorization checks based on user roles. Administrators are allowed to view
any user's profile, while regular users can only access their own profile.
"""

from typing import Dict, Any

# Sample data structures (replace with real data sources in production)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"email": "alice@example.com", "bio": "Admin user."},
    2: {"email": "bob@example.com",   "bio": "Regular user."},
    3: {"email": "carol@example.com", "bio": "Another user."},
}


def fetch_profile_data(requester_id: int, profile_id: int) -> Any:
    """
    Retrieve the profile data for a given user, enforcing proper authorization.

    Parameters
    ----------
    requester_id : int
        The ID of the user making the request.
    profile_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict or str
        The profile data dictionary if access is granted,
        otherwise the string 'Unauthorized'.

    Notes
    -----
    - Administrators (role == 'admin') may view any profile.
    - Regular users may only view their own profile.
    - If either user ID is unknown, access is denied.

    Raises
    ------
    None
        This function does not raise exceptions; it returns a string indicating
        unauthorized access for invalid requests.
    """
    # Validate that both users exist
    requester = USERS.get(requester_id)
    if not requester:
        return "Unauthorized"

    # Admins can access any profile
    if requester.get("role") == "admin":
        return USER_PROFILES.get(profile_id, "Unauthorized")

    # Non-admins can only access their own profile
    if requester_id == profile_id:
        return USER_PROFILES.get(profile_id, "Unauthorized")

    # All other cases are unauthorized
    return "Unauthorized"