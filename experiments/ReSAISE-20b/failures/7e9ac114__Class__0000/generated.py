# -*- coding: utf-8 -*-
"""
User profile access module.

This module defines the function `see_user_profile` which returns a user
profile if the requesting user is allowed to view it.  The function checks
that either:
    * the requester is viewing their own profile, or
    * the requester has an administrative role.

If neither condition holds, it returns the string 'Unauthorized'.
"""

from __future__ import annotations

# Example data structures. In a real application these would be fetched
# from a database or another secure source.
USER_PROFILES = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Eve",   "email": "eve@example.com"},
}

USERS = {
    1: {"username": "alice", "role": "user"},
    2: {"username": "bob",   "role": "admin"},
    3: {"username": "eve",   "role": "user"},
}

def see_user_profile(current_id: int, target_id: int) -> dict | str:
    """
    Return the profile of `target_id` if the requesting user (`current_id`)
    is allowed to view it.  If access is not permitted, return the string
    'Unauthorized'.

    Parameters:
        current_id (int): ID of the user making the request.
        target_id  (int): ID of the profile being requested.

    Returns:
        dict | str: The user profile dictionary or 'Unauthorized'.

    Raises:
        KeyError: If either `current_id` or `target_id` does not exist in
                  USERS/USER_PROFILES.
    """
    # Validate that both users exist. Raise KeyError if not found,
    # which is a normal error for missing data rather than an
    # authorization failure.
    if current_id not in USERS:
        raise KeyError(f"Requester ID {current_id} does not exist.")
    if target_id not in USER_PROFILES:
        raise KeyError(f"Target profile ID {target_id} does not exist.")

    # Authorization logic
    requester_role = USERS[current_id]["role"]
    if current_id == target_id or requester_role.lower() == "admin":
        return USER_PROFILES[target_id]

    # If we reach here, the requester is neither the target nor an admin.
    return "Unauthorized"