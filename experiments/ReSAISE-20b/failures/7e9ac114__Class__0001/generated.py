# -*- coding: utf-8 -*-
"""
Implementation of see_user_profile with proper authorization checks.
"""

from typing import Dict, Any

# Sample data structures – replace or extend as needed
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "user"},
    2: {"role": "admin"},
    3: {"role": "user"},
}

def see_user_profile(current_id: int, target_id: int) -> Any:
    """
    Return the profile of `target_id` if the caller is allowed to view it.

    Parameters
    ----------
    current_id : int
        ID of the user making the request.
    target_id : int
        ID of the profile being requested.

    Returns
    -------
    dict or str
        The user profile dictionary if access is allowed,
        otherwise the string 'Unauthorized'.

    Notes
    -----
    Authorization logic:
      * A user can always view their own profile.
      * Users with role 'admin' may view any profile.
    """
    # Verify that the current user exists
    if current_id not in USERS:
        return "Unauthorized"

    # Check for self-access or admin privileges
    if current_id == target_id:
        pass  # Self access allowed
    elif USERS[current_id].get("role") == "admin":
        pass  # Admin access allowed
    else:
        return "Unauthorized"

    # Retrieve the target profile if it exists
    profile = USER_PROFILES.get(target_id)
    return profile if profile is not None else "Unauthorized"