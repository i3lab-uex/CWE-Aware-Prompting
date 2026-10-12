# -*- coding: utf-8 -*-
"""
Access control for user profiles.

The function checks whether the requesting user is allowed to view the
requested profile.  A user can always view their own profile; an
administrator (role == "admin") may view any user's profile.
"""

from typing import Dict, Any

# Example data structures (replace with real ones in production)
USERS: Dict[int, Dict[str, Any]] = {
    # user_id: {"username": str, "role": str}
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    # user_id: profile data
}

def access_user_profile(requesting_user_id: int, viewing_user_id: int) -> Any:
    """
    Return the requested user profile if the requester is authorized,
    otherwise return the string 'Unauthorized'.

    Parameters
    ----------
    requesting_user_id : int
        ID of the user making the request.
    viewing_user_id : int
        ID of the profile being requested.

    Returns
    -------
    Any
        The user profile dictionary or 'Unauthorized'.
    """
    # Fetch the requesting user's record safely
    requester = USERS.get(requesting_user_id)
    if requester is None:
        return "Unauthorized"

    # Allow access if the user is viewing their own profile
    if requesting_user_id == viewing_user_id:
        return USER_PROFILES.get(viewing_user_id, "Unauthorized")

    # Allow access if the user has an admin role
    if requester.get("role") == "admin":
        return USER_PROFILES.get(viewing_user_id, "Unauthorized")

    # Default: deny access
    return "Unauthorized"