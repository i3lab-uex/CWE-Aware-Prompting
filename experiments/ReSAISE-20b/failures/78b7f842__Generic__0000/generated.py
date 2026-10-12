# -*- coding: utf-8 -*-
"""
Utility to view user profiles with role‑based access control.
"""

from typing import Dict, Any

# Example data structures (replace with actual data in real usage)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS: Dict[int, str] = {
    1: "user",
    2: "admin",
    3: "user",
}


def view_user_profile(current_user_id: int, target_user_id: int) -> Any:
    """
    Return the profile information for ``target_user_id`` if the requesting user
    is authorized.

    An admin can view any profile. A normal user may only view their own profile.
    If the target user does not exist, a ``KeyError`` is raised.

    Parameters
    ----------
    current_user_id : int
        The ID of the user making the request.
    target_user_id : int
        The ID of the profile to be viewed.

    Returns
    -------
    dict or str
        The profile dictionary if access is allowed, otherwise the string
        "Unauthorized".

    Raises
    ------
    KeyError
        If either ``current_user_id`` or ``target_user_id`` is not present in the
        corresponding dictionaries.
    """
    # Validate presence of users first
    if current_user_id not in USERS:
        raise KeyError(f"Current user id {current_user_id} does not exist.")
    if target_user_id not in USER_PROFILES:
        raise KeyError(f"Target user id {target_user_id} does not exist.")

    # Authorization logic
    if current_user_id == target_user_id or USERS.get(current_user_id) == "admin":
        return USER_PROFILES[target_user_id]

    return "Unauthorized"