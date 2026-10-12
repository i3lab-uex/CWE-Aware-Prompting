# -*- coding: utf-8 -*-

from typing import Any, Dict

# Sample data structures (these would normally come from a database or config)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS: Dict[int, str] = {
    1: "user",
    2: "admin",
    3: "user",
}

def view_user_profile(current_user_id: int, target_user_id: int) -> Any:
    """
    Return the profile information of `target_user_id` if the caller
    (`current_user_id`) is authorized to view it.

    Authorization rules:
        * A user can always view their own profile.
        * An admin (role == 'admin') can view any user's profile.

    Parameters
    ----------
    current_user_id : int
        The user ID of the actor requesting the data.
    target_user_id : int
        The user ID whose profile is being requested.

    Returns
    -------
    dict or str
        The target user's profile dictionary if authorized, otherwise
        the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either `current_user_id` or `target_user_id` is not present in the
        USERS/USER_PROFILES dictionaries.
    """
    # Validate that both users exist
    if current_user_id not in USERS:
        raise KeyError(f"Current user ID {current_user_id} does not exist.")
    if target_user_id not in USER_PROFILES:
        raise KeyError(f"Target user ID {target_user_id} does not exist.")

    # Authorization check
    is_admin = USERS[current_user_id] == "admin"
    if current_user_id == target_user_id or is_admin:
        # Return a copy to prevent accidental mutation
        return dict(USER_PROFILES[target_user_id])

    return "Unauthorized"