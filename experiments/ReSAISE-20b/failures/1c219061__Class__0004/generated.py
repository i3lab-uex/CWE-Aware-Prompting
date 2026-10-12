# -*- coding: utf-8 -*-
"""
User profile retrieval with proper authorization.

This module implements `get_user_profile`, which checks that the actor
has permission to view the requested profile.  An actor may see their own
profile or any other user’s profile if they have the 'admin' role.
"""

from typing import Dict, Any

# Example data structures (replace with actual data sources in production)
USERS: Dict[int, Dict[str, Any]] = {
    # user_id : { 'name': str, 'roles': List[str], ... }
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    # user_id : { 'email': str, 'bio': str, ... }
}


def get_user_profile(actor_user_id: int, requested_user_id: int) -> Any:
    """
    Retrieve a user profile with proper authorization.

    Parameters
    ----------
    actor_user_id : int
        The ID of the user making the request.
    requested_user_id : int
        The ID of the profile to retrieve.

    Returns
    -------
    dict | str
        The requested user profile if access is allowed,
        otherwise the string 'Unauthorized'.

    Notes
    -----
    - An actor can view their own profile.
    - Users with the 'admin' role may view any profile.
    - If either user ID is not found, access is denied.

    Security
    --------
    This function guards against CWE-862 (Missing Authorization)
    by explicitly checking permissions before returning sensitive data.
    """
    # Validate actor exists
    actor = USERS.get(actor_user_id)
    if not actor:
        return 'Unauthorized'

    # Validate requested profile exists
    profile = USER_PROFILES.get(requested_user_id)
    if not profile:
        return 'Unauthorized'

    # Allow self-view
    if actor_user_id == requested_user_id:
        return profile

    # Check for admin role
    roles = actor.get('roles', [])
    if 'admin' in roles:
        return profile

    # No permission
    return 'Unauthorized'