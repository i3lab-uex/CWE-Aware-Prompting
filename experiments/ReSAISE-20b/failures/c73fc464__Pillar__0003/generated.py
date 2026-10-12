# -*- coding: utf-8 -*-
"""
Secure profile fetching module.

This module implements the `fetch_profile_data` function which provides
controlled access to user profiles. Only a user can view their own profile,
and users with the 'admin' role are allowed to view any profile.

The implementation follows best practices for access control and
defensive programming to mitigate CWE‑284 (Improper Access Control).
"""

from __future__ import annotations

from typing import Dict, Any

# Sample data structures. In a real application these would come from a database.
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


def _get_user_role(user_id: int) -> str:
    """
    Retrieve the role of a user.

    Raises:
        KeyError: If the user_id does not exist in USERS.
    """
    return USERS[user_id]["role"]


def fetch_profile_data(requester_id: int, profile_id: int) -> Dict[str, Any] | str:
    """
    Return the profile details for `profile_id` if access is allowed.

    Access rules:
        - A user can view their own profile.
        - Users with the role 'admin' can view any profile.

    Parameters
    ----------
    requester_id : int
        The user ID of the individual making the request.
    profile_id : int
        The user ID of the profile being requested.

    Returns
    -------
    dict | str
        The profile dictionary if access is granted, otherwise the string
        'Unauthorized'.

    Raises
    ------
    KeyError
        If either `requester_id` or `profile_id` is not present in the data
        dictionaries. This indicates a programming error (e.g., missing user).
    """
    # Validate that both IDs exist; this also protects against injection of
    # arbitrary keys into the dictionaries.
    if requester_id not in USERS:
        raise KeyError(f"Requester ID {requester_id} does not exist.")
    if profile_id not in USER_PROFILES:
        raise KeyError(f"Profile ID {profile_id} does not exist.")

    # Determine if the requester has permission.
    is_self = requester_id == profile_id
    is_admin = _get_user_role(requester_id) == "admin"

    if not (is_self or is_admin):
        return "Unauthorized"

    # Return a shallow copy to prevent accidental mutation of the stored data.
    return USER_PROFILES[profile_id].copy()


# Example usage (for demonstration only; remove or guard in production)
if __name__ == "__main__":
    print(fetch_profile_data(1, 1))  # Own profile
    print(fetch_profile_data(2, 3))  # Admin viewing another's profile
    print(fetch_profile_data(3, 1))  # Unauthorized attempt