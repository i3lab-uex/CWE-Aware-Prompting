# -*- coding: utf-8 -*-
"""
Utility for viewing user profiles with role‑based access control.
"""

from __future__ import annotations

from typing import Any, Dict

# Example data structures – replace with real data in production
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin"},
    2: {"role": "user"},
}

def _is_admin(user_id: int) -> bool:
    """Return True if the user has an admin role."""
    return USERS.get(user_id, {}).get("role") == "admin"

def view_user_profile(current_user_id: int, target_user_id: int) -> Any:
    """
    Return the profile information of *target_user_id* if the caller is authorized.

    Parameters
    ----------
    current_user_id : int
        The user ID of the actor making the request.
    target_user_id : int
        The user ID whose profile is being requested.

    Returns
    -------
    dict or str
        The target user's profile data if authorized, otherwise an error message.

    Notes
    -----
    * A user can view their own profile.
    * An admin can view any user's profile.
    * If the target user does not exist, a 'User not found' message is returned.
    """
    # Basic sanity checks
    if current_user_id not in USERS:
        return "Unauthorized: actor does not exist"
    if target_user_id not in USER_PROFILES:
        return "User not found"

    # Authorization logic
    if current_user_id == target_user_id or _is_admin(current_user_id):
        # Return a copy to prevent accidental mutation of the original data
        return USER_PROFILES[target_user_id].copy()

    return "Unauthorized"

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    print(view_user_profile(1, 2))  # Admin viewing Bob
    print(view_user_profile(2, 1))  # Bob attempting to view Alice – should be Unauthorized
    print(view_user_profile(2, 2))  # Bob viewing own profile – should succeed