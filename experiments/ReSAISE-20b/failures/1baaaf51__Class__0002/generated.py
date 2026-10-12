# -*- coding: utf-8 -*-
"""
Secure profile access module.

This module implements the `access_user_profile` function, which enforces
proper authorization checks before returning user profile data.  The
implementation follows the principle of least privilege and protects
against CWE‑862 (Missing Authorization).

Author: ChatGPT
"""

from typing import Dict, Any

# Example data structures (replace with real data in production)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"username": "alice",   "role": "user"},
    2: {"username": "bob_admin","role": "admin"},
}


def access_user_profile(active_user_id: int, profile_id: int) -> Any:
    """
    Return the requested user profile if access is authorized.

    Parameters
    ----------
    active_user_id : int
        ID of the user making the request.
    profile_id : int
        ID of the profile to retrieve.

    Returns
    -------
    dict | str
        The requested user profile dictionary on success, or the string
        'Unauthorized' if access is denied.

    Notes
    -----
    - A user may view their own profile.
    - Users with the role 'admin' can view any profile.
    - The function performs explicit authorization checks and guards
      against missing user or profile entries to avoid information leaks.
    """
    # Validate input types
    if not isinstance(active_user_id, int) or not isinstance(profile_id, int):
        raise TypeError("User IDs must be integers")

    # Retrieve active user data
    active_user = USERS.get(active_user_id)
    if active_user is None:
        # Unknown user; treat as unauthorized
        return "Unauthorized"

    # Authorization logic
    is_self = active_user_id == profile_id
    is_admin = active_user.get("role") == "admin"

    if not (is_self or is_admin):
        return "Unauthorized"

    # Retrieve the requested profile
    profile = USER_PROFILES.get(profile_id)
    if profile is None:
        # Profile does not exist; avoid leaking existence information
        return "Unauthorized"

    # Return a copy to prevent accidental mutation of the global store
    return profile.copy()


# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     print(access_user_profile(1, 1))   # Own profile
#     print(access_user_profile(2, 1))   # Admin viewing others' profile
#     print(access_user_profile(1, 2))   # Unauthorized attempt