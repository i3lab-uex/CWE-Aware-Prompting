# -*- coding: utf-8 -*-
"""
User profile viewing with proper authorization checks.

The module defines a single function `view_user_profile` that
ensures only the profile owner or an administrator can access a
profile.  It guards against CWE-862 (Missing Authorization) by
explicitly verifying the actor's role before returning sensitive data.
"""

from typing import Dict, Any

# Example data structures – in a real application these would be loaded
# from a database or another secure source.
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


def view_user_profile(current_user_id: int, target_user_id: int) -> Any:
    """
    Return the profile information of `target_user_id` if the caller
    (`current_user_id`) is authorized.

    Parameters:
        current_user_id (int): The ID of the user making the request.
        target_user_id  (int): The ID of the profile to view.

    Returns:
        dict: Profile data if authorized.
        str : 'Unauthorized' message otherwise.

    Raises:
        KeyError: If either user ID does not exist in the system.
    """
    # Ensure both users exist; this also serves as a basic validation
    if current_user_id not in USERS:
        raise KeyError(f"Actor user ID {current_user_id} does not exist.")
    if target_user_id not in USER_PROFILES:
        raise KeyError(f"Target user ID {target_user_id} does not exist.")

    # Authorization logic:
    # 1. Owner can view their own profile.
    # 2. Users with role 'admin' can view any profile.
    actor_role = USERS[current_user_id].get("role", "user")

    if current_user_id == target_user_id or actor_role.lower() == "admin":
        # Return a copy to prevent accidental modifications.
        return USER_PROFILES[target_user_id].copy()

    # If none of the above conditions are met, deny access.
    return "Unauthorized"