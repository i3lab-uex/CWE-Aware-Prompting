# -*- coding: utf-8 -*-
"""
Module providing user profile access with proper authorization checks.
"""

from typing import Any, Dict

# Example data structures. In a real application these would come from
# a database or an external service.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"email": "alice@example.com", "age": 30},
    2: {"email": "bob@example.com",   "age": 25},
    3: {"email": "carol@example.com", "age": 28},
}


def access_user_profile(active_user_id: int, profile_id: int) -> Any:
    """
    Return the requested user profile if the caller is authorized.

    Parameters
    ----------
    active_user_id : int
        ID of the user making the request.
    profile_id : int
        ID of the profile being requested.

    Returns
    -------
    dict | str
        The user profile dictionary if access is granted, otherwise the string
        'Unauthorized'.

    Notes
    -----
    * A user can view their own profile.
    * An admin (role == 'admin') can view any profile.
    * If either the active user or target profile does not exist, access is denied.
    """
    # Verify that both users exist
    active_user = USERS.get(active_user_id)
    target_profile = USER_PROFILES.get(profile_id)

    if active_user is None or target_profile is None:
        # Either the requester or requested profile does not exist
        return "Unauthorized"

    # Authorization logic
    if active_user_id == profile_id:
        # Users can always view their own profile
        return target_profile

    if active_user.get("role") == "admin":
        # Admins can view any profile
        return target_profile

    # All other cases are denied
    return "Unauthorized"