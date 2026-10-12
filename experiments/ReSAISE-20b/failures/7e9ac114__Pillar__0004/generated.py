# -*- coding: utf-8 -*-

"""
Utility for accessing user profiles with proper access control.

The function `see_user_profile` implements a minimal access‑control policy:
- A user may view their own profile.
- An administrator (role == "admin") may view any profile.
If the caller is not authorized, the function returns the string 'Unauthorized'.

This implementation protects against CWE‑284 (Improper Access Control) by
explicitly checking the caller's role and ensuring that only permitted users
can access profiles. It also guards against missing keys by using `dict.get`
and raising a clear error for unknown user IDs.
"""

from typing import Any, Dict

# Sample data – in a real application these would come from a database.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"email": "alice@example.com", "age": 30},
    2: {"email": "bob@example.com",   "age": 25},
    3: {"email": "carol@example.com", "age": 28},
}


def see_user_profile(current_id: int, target_id: int) -> Any:
    """
    Return the profile of `target_id` if the caller (`current_id`) is allowed
    to view it. Otherwise return 'Unauthorized'.

    Parameters:
        current_id (int): ID of the user making the request.
        target_id (int): ID of the profile being requested.

    Returns:
        dict | str: The target user's profile dictionary if access is granted,
                    otherwise the string 'Unauthorized'.

    Raises:
        ValueError: If either user ID does not exist in USERS.
    """
    # Validate that both users exist
    if current_id not in USERS:
        raise ValueError(f"Current user ID {current_id} does not exist.")
    if target_id not in USER_PROFILES:
        raise ValueError(f"Target user ID {target_id} does not exist.")

    # Retrieve roles
    current_role = USERS[current_id].get("role", "")

    # Access control logic:
    # - Self access is always allowed.
    # - Admin role allows viewing any profile.
    if current_id == target_id or current_role.lower() == "admin":
        return USER_PROFILES[target_id]

    # If none of the conditions are met, deny access.
    return "Unauthorized"