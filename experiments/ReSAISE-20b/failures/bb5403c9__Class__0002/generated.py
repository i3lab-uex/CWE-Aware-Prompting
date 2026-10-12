# -*- coding: utf-8 -*-
"""
Profile access module

This module defines a single function `get_profile_info` that returns
profile details for a requested user.  The function enforces proper
authorization checks to prevent CWE‑862: Missing Authorization.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# Example data structures.  In a real application these would be
# retrieved from a database or another persistent store.
USER_PROFILES: dict[int, dict] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Eve",   "email": "eve@example.com"},
}

USERS: dict[int, dict] = {
    1: {"role": "admin"},
    2: {"role": "user"},
    3: {"role": "user"},
}

# Role constants
ADMIN_ROLE = "admin"
USER_ROLE = "user"


def get_profile_info(acting_user_id: int, viewing_user_id: int) -> dict | str:
    """
    Return profile information for the requested user if the requesting
    actor is authorized.

    Parameters
    ----------
    acting_user_id : int
        The user ID of the individual making the request.
    viewing_user_id : int
        The user ID whose profile is being requested.

    Returns
    -------
    dict | str
        Profile dictionary if access is granted, otherwise the string
        'Unauthorized'.

    Notes
    -----
    * An actor may view their own profile.
    * Administrators may view any user's profile.
    * All other requests are denied.
    """
    # Quick checks for existence
    if acting_user_id not in USERS or viewing_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Retrieve role of the acting user
    acting_role = USERS[acting_user_id].get("role", USER_ROLE)

    # Authorization logic
    if acting_user_id == viewing_user_id:
        # Self‑access is always allowed
        return USER_PROFILES[viewing_user_id]

    if acting_role == ADMIN_ROLE:
        # Admins can view any profile
        return USER_PROFILES[viewing_user_id]

    # All other cases are denied
    return "Unauthorized"