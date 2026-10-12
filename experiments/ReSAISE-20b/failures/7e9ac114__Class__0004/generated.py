# -*- coding: utf-8 -*-

"""
Author: OpenAI ChatGPT
"""

from typing import Any, Dict

# Example data structures (replace with actual data in production)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"username": "alice", "role": "user"},
    2: {"username": "bob",   "role": "admin"},
}


def see_user_profile(current_id: int, target_id: int) -> Any:
    """
    Return the profile of `target_id` if the caller (`current_id`) is authorized.

    Authorization rules:
        * A user may view their own profile.
        * An administrator (role == "admin") may view any profile.

    Parameters
    ----------
    current_id : int
        ID of the user making the request.
    target_id : int
        ID of the profile being requested.

    Returns
    -------
    dict | str
        The target user's profile dictionary if authorized, otherwise the string 'Unauthorized'.
    """
    # Verify that both users exist
    current_user = USERS.get(current_id)
    target_profile = USER_PROFILES.get(target_id)

    if current_user is None or target_profile is None:
        # Either the requesting user or the target profile does not exist
        return "Unauthorized"

    # Authorization check
    if current_id == target_id or current_user.get("role") == "admin":
        return target_profile

    # Access denied
    return "Unauthorized"