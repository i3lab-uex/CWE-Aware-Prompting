#!/usr/bin/env python3
"""
Access‑controlled profile viewer.

The module defines a single function `get_profile_info` that allows
users to view their own profile and lets administrators inspect any
user's profile.  It protects against CWE‑284 by checking the role of
the acting user before returning sensitive data.
"""

from __future__ import annotations

from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Sample data structures (replace with real storage in production)
# --------------------------------------------------------------------------- #

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


# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def get_profile_info(acting_user_id: int, viewing_user_id: int) -> Dict[str, Any] | str:
    """
    Return profile details for `viewing_user_id` if the request is authorized.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user making the request.
    viewing_user_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict | str
        The profile dictionary if access is granted; otherwise the string
        'Unauthorized'.

    Notes
    -----
    * A user can view their own profile.
    * An administrator (role == 'admin') can view any profile.
    * All other requests are denied.
    * The function performs type and existence checks to avoid accidental
      leaks or errors.
    """
    # Validate input types – if wrong type, treat as unauthorized
    if not isinstance(acting_user_id, int) or not isinstance(viewing_user_id, int):
        return "Unauthorized"

    # Verify both users exist
    if acting_user_id not in USERS or viewing_user_id not in USER_PROFILES:
        return "Unauthorized"

    acting_role = USERS[acting_user_id].get("role", "")
    # Allow self‑view
    if acting_user_id == viewing_user_id:
        return USER_PROFILES[viewing_user_id].copy()

    # Allow admin view
    if acting_role.lower() == "admin":
        return USER_PROFILES[viewing_user_id].copy()

    # All other cases are unauthorized
    return "Unauthorized"


# --------------------------------------------------------------------------- #
# Example usage (remove or guard in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    print(get_profile_info(1, 1))   # Alice views herself
    print(get_profile_info(2, 3))   # Admin Bob views Carol
    print(get_profile_info(1, 2))   # Alice attempts to view Bob – denied