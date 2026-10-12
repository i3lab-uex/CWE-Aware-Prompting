# -*- coding: utf-8 -*-
"""
Author: ChatGPT
Description:
    Provides a secure function to retrieve user profile information with proper
    authorization checks.

CWE-862: Missing Authorization – the function ensures that only the profile owner
or an administrator can access a profile. It also validates inputs to guard
against dictionary key errors and potential injection attacks.
"""

from typing import Dict, Any

# Example data structures (replace with actual application data)
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

def get_profile_info(acting_user_id: int, viewing_user_id: int) -> Any:
    """
    Return the profile of `viewing_user_id` if the request is authorized.

    Parameters
    ----------
    acting_user_id : int
        The user id of the individual making the request.
    viewing_user_id : int
        The user id of the profile being requested.

    Returns
    -------
    dict or str
        Profile details if access is granted, otherwise the string 'Unauthorized'.

    Raises
    ------
    ValueError
        If either user id is not present in the system.
    """
    # Basic type validation (optional but helps catch misuse)
    if not isinstance(acting_user_id, int) or not isinstance(viewing_user_id, int):
        raise TypeError("User IDs must be integers.")

    # Ensure both users exist
    if acting_user_id not in USERS:
        raise ValueError(f"Acting user id {acting_user_id} does not exist.")
    if viewing_user_id not in USER_PROFILES:
        raise ValueError(f"Profile for user id {viewing_user_id} does not exist.")

    # Authorization check: owner or admin
    acting_role = USERS[acting_user_id]["role"]
    if acting_user_id != viewing_user_id and acting_role.lower() != "admin":
        return "Unauthorized"

    # Return a copy to prevent accidental mutation
    return USER_PROFILES[viewing_user_id].copy()