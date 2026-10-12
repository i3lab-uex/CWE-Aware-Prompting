# -*- coding: utf-8 -*-
"""
Simple user profile access control.

The module defines a single public function `access_user_profile` that checks
whether the requesting user has permission to view another user's profile.
The check is performed based on the following rules:

* A user can always view their own profile.
* An admin (role == "admin") can view any profile.

If the requested user does not exist or the active user lacks permission,
the function returns the string ``"Unauthorized"``.  In case either
`active_user_id` or `profile_id` is missing from the user database,
a ``ValueError`` is raised to signal a programming error rather than
an authorization failure.

The data structures are intentionally minimal; in real code these would be
replaced by database look‑ups or ORM queries.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Mock data
# --------------------------------------------------------------------------- #

# USERS maps user_id to a dict containing at least the role of the user.
USERS = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

# USER_PROFILES maps user_id to profile information.
USER_PROFILES = {
    1: {"user_id": 1, "email": "alice@example.com", "bio": "Administrator"},
    2: {"user_id": 2, "email": "bob@example.com",   "bio": "Developer"},
    3: {"user_id": 3, "email": "carol@example.com", "bio": "Designer"},
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def access_user_profile(active_user_id: int, profile_id: int) -> dict | str:
    """
    Return the profile information for ``profile_id`` if ``active_user_id``
    is authorized to view it.

    Parameters
    ----------
    active_user_id : int
        ID of the user making the request.
    profile_id : int
        ID of the profile to be retrieved.

    Returns
    -------
    dict | str
        The requested user profile if access is allowed, otherwise the string
        ``"Unauthorized"``.

    Raises
    ------
    ValueError
        If either the active user or the requested profile does not exist in
        the system.  This is a programming error and should be handled by
        the caller.
    """
    # Verify that both users exist in the system
    if active_user_id not in USERS:
        raise ValueError(f"Active user ID {active_user_id} does not exist.")
    if profile_id not in USER_PROFILES:
        raise ValueError(f"Profile ID {profile_id} does not exist.")

    # Self‑view is always allowed
    if active_user_id == profile_id:
        return USER_PROFILES[profile_id]

    # Admins can view any profile
    if USERS.get(active_user_id, {}).get("role") == "admin":
        return USER_PROFILES[profile_id]

    # Otherwise, deny access
    return "Unauthorized"

# --------------------------------------------------------------------------- #
# Example usage (for debugging only; remove or guard with __name__ == "__main__")
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # These examples illustrate expected behaviour.
    print(access_user_profile(1, 2))  # admin viewing Bob's profile
    print(access_user_profile(2, 3))  # user Bob trying to view Carol's profile
    print(access_user_profile(2, 2))  # Bob viewing his own profile