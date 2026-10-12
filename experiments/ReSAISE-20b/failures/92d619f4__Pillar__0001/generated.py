#!/usr/bin/env python3
"""
Module providing a secure profile lookup function.
"""

from typing import Dict, Any

# Example data structures (replace with actual data in production)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"email": "alice@example.com", "age": 30},
    2: {"email": "bob@example.com",   "age": 25},
    3: {"email": "carol@example.com","age": 28},
}

def fetch_profile_info(logged_user_id: int, view_user_id: int) -> Any:
    """
    Return the profile information for *view_user_id* if the request
    is authorized.  A user may view their own profile; an admin may
    view any profile.

    Parameters
    ----------
    logged_user_id : int
        ID of the user making the request.
    view_user_id : int
        ID of the profile to retrieve.

    Returns
    -------
    dict | str
        The requested user profile dictionary, or the string
        'Unauthorized' if access is denied.

    Raises
    ------
    KeyError
        If either *logged_user_id* or *view_user_id* is not present in the
        USERS/USER_PROFILES dictionaries.
    """
    # Validate that both users exist; raise KeyError if not
    requester = USERS[logged_user_id]          # may raise KeyError
    target_profile = USER_PROFILES[view_user_id]  # may raise KeyError

    # Determine access rights
    if logged_user_id == view_user_id:
        return target_profile

    # Only admins can access other profiles
    if requester.get("role") == "admin":
        return target_profile

    # All other cases are unauthorized
    return "Unauthorized"