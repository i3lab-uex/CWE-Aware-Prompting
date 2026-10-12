# -*- coding: utf-8 -*-

from typing import Dict, Any

# Example data structures. In a real application these would come from a database.
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

def fetch_profile_info(logged_user_id: int, view_user_id: int) -> Any:
    """
    Return the profile information of `view_user_id` if the caller is authorized.

    An admin can view any profile. A regular user may only view their own profile.
    If the caller is not authorized, return the string 'Unauthorized'.

    Parameters
    ----------
    logged_user_id : int
        The ID of the user making the request.
    view_user_id : int
        The ID of the profile to be viewed.

    Returns
    -------
    dict | str
        The requested user profile, or 'Unauthorized'.
    """
    # Validate that both users exist
    if logged_user_id not in USERS or view_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Determine the role of the logged-in user
    role = USERS[logged_user_id].get("role", "user")

    # Authorization logic
    if role == "admin" or logged_user_id == view_user_id:
        return USER_PROFILES[view_user_id]

    # Access denied
    return "Unauthorized"