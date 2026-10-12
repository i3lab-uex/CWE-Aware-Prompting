# -*- coding: utf-8 -*-
"""
User profile access control module.

This module defines a single function `display_user_profile` that
enforces proper authorization when retrieving user profiles.

Author: ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample data (for illustration purposes)
# In a real application these would come from a database or external service.
# --------------------------------------------------------------------------- #
USER_PROFILES = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS = {
    1: {"username": "alice",   "role": "user"},
    2: {"username": "bob",     "role": "admin"},
    3: {"username": "carol",   "role": "user"},
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _has_access(active_user_id: int, profile_user_id: int) -> bool:
    """
    Determine whether the active user is allowed to view the requested profile.

    Rules:
        * A user can always view their own profile.
        * Users with the role 'admin' may view any profile.

    Parameters
    ----------
    active_user_id : int
        ID of the user making the request.
    profile_user_id : int
        ID of the profile being requested.

    Returns
    -------
    bool
        True if access is permitted, False otherwise.
    """
    # Basic validation: ensure both users exist
    if active_user_id not in USERS or profile_user_id not in USER_PROFILES:
        return False

    if active_user_id == profile_user_id:
        return True

    active_role = USERS[active_user_id].get("role", "").lower()
    return active_role == "admin"


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def display_user_profile(active_user_id: int, profile_user_id: int) -> dict | str:
    """
    Return the requested user profile if access is allowed.

    Parameters
    ----------
    active_user_id : int
        ID of the user making the request.
    profile_user_id : int
        ID of the profile being requested.

    Returns
    -------
    dict | str
        The user profile dictionary if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    This function intentionally does not raise exceptions for missing users to avoid
    leaking information about user existence.  It follows the principle of least
    privilege and guards against CWE-284 (Improper Access Control).
    """
    if _has_access(active_user_id, profile_user_id):
        # Return a shallow copy to prevent accidental modifications
        return dict(USER_PROFILES.get(profile_user_id, {}))
    return "Unauthorized"


# --------------------------------------------------------------------------- #
# Example usage (commented out to avoid side effects)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Active user is Bob (admin) viewing Alice's profile
    print(display_user_profile(2, 1))   # Expected: Alice's profile

    # Active user is Carol trying to view Bob's profile
    print(display_user_profile(3, 2))   # Expected: 'Unauthorized'

    # Active user is Alice viewing her own profile
    print(display_user_profile(1, 1))   # Expected: Alice's profile