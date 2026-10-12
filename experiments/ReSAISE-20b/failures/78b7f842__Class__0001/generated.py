# -*- coding: utf-8 -*-
"""
User profile access module.

This module provides a single function, `view_user_profile`, which allows
a user to view either their own profile or an administrator to view any
profile.  The implementation performs strict authorization checks in
order to avoid the CWE-862 missing‑authorization vulnerability.
"""

from typing import Dict, Any

# Example data structures. In a real application these would be
# loaded from a database or external service.
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

def view_user_profile(current_user_id: int, target_user_id: int) -> Dict[str, Any] | str:
    """
    Return the profile information of `target_user_id` if the caller is authorized.

    An actor is authorized to view a profile when:
        * They are requesting their own profile (current_user_id == target_user_id), or
        * They have the 'admin' role.

    Parameters
    ----------
    current_user_id : int
        The ID of the user making the request.
    target_user_id : int
        The ID of the profile to view.

    Returns
    -------
    dict or str
        The target user's profile dictionary if authorized; otherwise the string
        'Unauthorized'.

    Raises
    ------
    KeyError
        If either `current_user_id` or `target_user_id` does not exist in the
        USERS/USER_PROFILES dictionaries.
    """
    # Ensure both users exist to avoid leaking existence information
    if current_user_id not in USERS:
        raise KeyError(f"Current user ID {current_user_id} does not exist.")
    if target_user_id not in USER_PROFILES:
        raise KeyError(f"Target user ID {target_user_id} does not exist.")

    # Fetch the role of the actor
    current_role = USERS[current_user_id].get("role", "user")

    # Authorization logic
    authorized = (
        current_user_id == target_user_id  # self‑view
        or current_role.lower() == "admin"  # admin privilege
    )

    if not authorized:
        return "Unauthorized"

    # Return a copy to prevent accidental mutation of the original data
    return USER_PROFILES[target_user_id].copy()