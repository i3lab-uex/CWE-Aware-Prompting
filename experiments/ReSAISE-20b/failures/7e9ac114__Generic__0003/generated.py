from __future__ import annotations

from typing import Dict, Any


# Example data structures (replace with actual data in production)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin"},
    2: {"role": "user"},
}


def see_user_profile(current_id: int, target_id: int) -> Any:
    """
    Return the profile of ``target_id`` if the requesting user (``current_id``)
    is allowed to view it. An admin can view any profile, while a normal user
    may only view their own.

    Parameters
    ----------
    current_id : int
        ID of the user making the request.
    target_id : int
        ID of the profile being requested.

    Returns
    -------
    dict or str
        The target user's profile dictionary if access is permitted,
        otherwise the string 'Unauthorized'.
    """
    # Basic validation of input types
    if not isinstance(current_id, int) or not isinstance(target_id, int):
        return "Unauthorized"

    # Verify that both users exist
    if current_id not in USERS or target_id not in USER_PROFILES:
        return "Unauthorized"

    # Fetch current user's role
    current_role = USERS.get(current_id, {}).get("role", "user")

    # Access control
    if current_role == "admin" or current_id == target_id:
        return USER_PROFILES[target_id]

    return "Unauthorized"