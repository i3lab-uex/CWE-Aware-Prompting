# -*- coding: utf-8 -*-

"""
User profile access module.

This module defines the `access_user_profile` function which enforces
authorization checks to prevent CWE-862: Missing Authorization.
"""

from typing import Any, Dict

# Example data structures. In a real application these would come from
# a database or external service.
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

def access_user_profile(active_user_id: int, profile_id: int) -> Any:
    """
    Return the requested user profile if access is permitted.

    Parameters
    ----------
    active_user_id : int
        ID of the user making the request.
    profile_id : int
        ID of the profile to retrieve.

    Returns
    -------
    dict | str
        The requested user profile dictionary if authorized,
        otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either `active_user_id` or `profile_id` does not exist in the
        USERS/USER_PROFILES dictionaries.
    """
    # Validate that both IDs exist to avoid ambiguous errors
    if active_user_id not in USERS:
        raise KeyError(f"Active user ID {active_user_id} does not exist.")
    if profile_id not in USER_PROFILES:
        raise KeyError(f"Profile ID {profile_id} does not exist.")

    # Retrieve the active user's role
    active_role = USERS[active_user_id]["role"]

    # Authorization logic:
    # - Users can view their own profile.
    # - Admins can view any profile.
    if active_user_id == profile_id or active_role.lower() == "admin":
        return USER_PROFILES[profile_id]

    # Deny access
    return "Unauthorized"

# Example usage (commented out for production):
# if __name__ == "__main__":
#     print(access_user_profile(1, 1))  # Own profile
#     print(access_user_profile(2, 3))  # Admin viewing another user
#     print(access_user_profile(1, 2))  # Unauthorized