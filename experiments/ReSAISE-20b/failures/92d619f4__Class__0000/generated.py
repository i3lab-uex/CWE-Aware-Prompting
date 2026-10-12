# -*- coding: utf-8 -*-
"""
Profile viewing utility.

This module provides a single function, `fetch_profile_info`, which
returns the profile information for a requested user.  The function
ensures that only the owner of the profile or an administrator may
view a profile, mitigating CWE‑862 (Missing Authorization).

Author: ChatGPT
"""

from __future__ import annotations

# Sample data – in a real application these would come from a database
USERS = {
    1: {"username": "alice",   "role": "user"},
    2: {"username": "bob",     "role": "admin"},
    3: {"username": "carol",   "role": "user"},
}

USER_PROFILES = {
    1: {"name": "Alice Smith",   "email": "alice@example.com"},
    2: {"name": "Bob Jones",     "email": "bob@example.com"},
    3: {"name": "Carol Lee",     "email": "carol@example.com"},
}


def fetch_profile_info(logged_user_id: int, view_user_id: int) -> dict | str:
    """
    Return the profile information of `view_user_id` if the request is
    authorized, otherwise return 'Unauthorized'.

    Parameters
    ----------
    logged_user_id : int
        The ID of the user making the request.
    view_user_id : int
        The ID of the profile to be viewed.

    Returns
    -------
    dict | str
        The requested profile dictionary or the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either `logged_user_id` or `view_user_id` does not exist in the
        corresponding data stores.
    """
    # Validate existence of both users
    if logged_user_id not in USERS:
        raise KeyError(f"Logged user ID {logged_user_id} does not exist.")
    if view_user_id not in USER_PROFILES:
        raise KeyError(f"Profile ID {view_user_id} does not exist.")

    # Owner can view own profile
    if logged_user_id == view_user_id:
        return USER_PROFILES[view_user_id]

    # Admins can view any profile
    logged_role = USERS.get(logged_user_id, {}).get("role")
    if logged_role == "admin":
        return USER_PROFILES[view_user_id]

    # If neither condition is met, deny access
    return "Unauthorized"


# Example usage (commented out for unit-test friendliness)
if __name__ == "__main__":
    try:
        print(fetch_profile_info(1, 3))   # Unauthorized
        print(fetch_profile_info(2, 3))   # Carol's profile (admin access)
        print(fetch_profile_info(1, 1))   # Alice's own profile
    except KeyError as exc:
        print(f"Error: {exc}")