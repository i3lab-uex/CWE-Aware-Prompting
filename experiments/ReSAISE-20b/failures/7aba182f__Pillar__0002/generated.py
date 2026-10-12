# -*- coding: utf-8 -*-
"""
Implements access control for user profiles.
"""

from typing import Dict, Any

# Example data structures. In real usage these would come from a database or config.
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

def access_user_profile(requesting_user_id: int, viewing_user_id: int) -> Any:
    """
    Grant access to a user profile if the requesting user is the owner or an admin.

    Parameters
    ----------
    requesting_user_id : int
        ID of the user making the request.
    viewing_user_id : int
        ID of the profile being requested.

    Returns
    -------
    dict or str
        The requested user profile if access is allowed, otherwise the string 'Unauthorized'.
    """
    # Validate that both users exist
    requester = USERS.get(requesting_user_id)
    target_profile = USER_PROFILES.get(viewing_user_id)

    if requester is None or target_profile is None:
        return "Unauthorized"

    # Admins can view any profile; users can only view their own
    if requester["role"] == "admin" or requesting_user_id == viewing_user_id:
        return target_profile

    return "Unauthorized"