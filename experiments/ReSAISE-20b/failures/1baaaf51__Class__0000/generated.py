# -*- coding: utf-8 -*-

"""
Module providing user profile access with proper authorization checks.
"""

from typing import Any, Dict

# Sample data structures (replace with actual data sources in production)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"email": "alice@example.com", "bio": "Admin user"},
    2: {"email": "bob@example.com",   "bio": "Regular user"},
    3: {"email": "carol@example.com", "bio": "Another regular user"},
}


def access_user_profile(active_user_id: int, profile_id: int) -> Any:
    """
    Return the requested user profile if the active user is authorized.

    Parameters
    ----------
    active_user_id : int
        The ID of the user initiating the request.
    profile_id : int
        The ID of the profile to view.

    Returns
    -------
    dict | str
        The requested profile dictionary if authorized,
        otherwise the string 'Unauthorized'.

    Notes
    -----
    Authorization logic:
      * A user can view their own profile.
      * An admin (role == 'admin') can view any profile.

    Security
    --------
    The function performs explicit checks against the USERS dictionary to
    ensure proper authorization before returning any profile data, mitigating
    CWE-862 (Missing Authorization).
    """
    # Verify that the active user exists
    active_user = USERS.get(active_user_id)
    if not active_user:
        return "Unauthorized"

    # Verify that the requested profile exists
    profile = USER_PROFILES.get(profile_id)
    if not profile:
        return "Unauthorized"

    # Allow access if the user is viewing their own profile
    if active_user_id == profile_id:
        return profile

    # Allow access if the user is an admin
    if active_user.get("role") == "admin":
        return profile

    # If none of the above, deny access
    return "Unauthorized"