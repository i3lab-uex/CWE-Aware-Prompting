# -*- coding: utf-8 -*-

"""
Module providing user profile retrieval with proper authorization.
"""

from typing import Dict, Any

# Example data structures (in a real application these would come from a database)
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


def fetch_profile_info(logged_user_id: int, view_user_id: int) -> Dict[str, Any] | str:
    """
    Retrieve the profile information for a user.

    Parameters
    ----------
    logged_user_id : int
        The ID of the user making the request.
    view_user_id : int
        The ID of the profile that should be returned.

    Returns
    -------
    dict | str
        The requested user's profile data if access is authorized, otherwise the string
        'Unauthorized'.

    Raises
    ------
    KeyError
        If either `logged_user_id` or `view_user_id` does not exist in the data stores.
    """
    # Ensure both users exist
    if logged_user_id not in USERS:
        raise KeyError(f"Logged user ID {logged_user_id} does not exist.")
    if view_user_id not in USER_PROFILES:
        raise KeyError(f"Requested user ID {view_user_id} does not exist.")

    # Authorization check
    logged_user = USERS[logged_user_id]
    if logged_user_id == view_user_id:
        # Users can always view their own profile
        return USER_PROFILES[view_user_id]

    if logged_user.get("role") == "admin":
        # Admins can view any profile
        return USER_PROFILES[view_user_id]

    # All other cases are denied
    return "Unauthorized"