# -*- coding: utf-8 -*-

"""
Implementation of a simple access‑controlled profile fetcher.
The function checks whether the requesting user is either
* the owner of the requested profile, or
* has an admin role.
If neither condition holds, it returns "Unauthorized".

The module uses two dictionaries that must be supplied by the caller:
    - USERS:   {user_id: {"role": "admin" | "user", ...}}
    - USER_PROFILES: {user_id: profile_dict}
"""

from typing import Dict, Any

# Example data structures (to be replaced with real ones in production)
USERS: Dict[int, Dict[str, Any]] = {}
USER_PROFILES: Dict[int, Dict[str, Any]] = {}

def fetch_profile_info(logged_user_id: int, view_user_id: int) -> Any:
    """
    Retrieve the profile information for a user if access is permitted.

    Parameters
    ----------
    logged_user_id : int
        The ID of the user making the request.
    view_user_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict or str
        The profile dictionary if access is allowed, otherwise the string
        "Unauthorized".

    Raises
    ------
    KeyError
        If either the requesting user or the requested profile does not exist.
    """

    # Validate that both users exist
    if logged_user_id not in USERS:
        raise KeyError(f"Logged user ID {logged_user_id} does not exist.")
    if view_user_id not in USER_PROFILES:
        raise KeyError(f"Profile for user ID {view_user_id} does not exist.")

    # Retrieve the role of the logged‑in user
    requester_role = USERS[logged_user_id].get("role", "user")

    # Access control logic
    if logged_user_id == view_user_id or requester_role.lower() == "admin":
        # Authorized: return a copy to avoid accidental mutation
        return dict(USER_PROFILES[view_user_id])

    # Denied access
    return "Unauthorized"