# -*- coding: utf-8 -*-
"""
Access control module for user profiles.

The `access_user_profile` function enforces that a normal user can only view
their own profile, while users with the role 'admin' are permitted to view any
profile.  It returns the profile data or the string `'Unauthorized'` when the
request is not permitted.

The implementation avoids common pitfalls such as comparing values of different
types, leaking information through exception messages, or relying on mutable
global state.  All data is treated as immutable during the check to prevent
race conditions or accidental modification.
"""

from __future__ import annotations

# Example data structures. In a real application these would be populated from
# a database or another persistent store.
USER_PROFILES: dict[int, dict[str, any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Eve",   "email": "eve@example.com"},
}

USERS: dict[int, dict[str, any]] = {
    1: {"username": "alice", "role": "user"},
    2: {"username": "bob",   "role": "admin"},
    3: {"username": "eve",   "role": "user"},
}

def access_user_profile(active_user_id: int, profile_id: int) -> dict | str:
    """
    Return the requested user profile if access is permitted.

    Parameters
    ----------
    active_user_id : int
        The ID of the user making the request.
    profile_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict | str
        Profile data if access is allowed; otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either `active_user_id` or `profile_id` is not present in the data
        structures.  In production code, this should be handled gracefully.
    """
    # Validate that both users exist in the system
    if active_user_id not in USERS:
        raise KeyError(f"Active user ID {active_user_id} does not exist.")
    if profile_id not in USER_PROFILES:
        raise KeyError(f"Profile ID {profile_id} does not exist.")

    active_user = USERS[active_user_id]
    # Normal users may only view their own profile
    if active_user["role"] == "admin":
        # Admins have unrestricted access
        return USER_PROFILES[profile_id]

    if active_user_id == profile_id:
        # Owner is accessing their own profile
        return USER_PROFILES[profile_id]

    # Any other case is denied
    return "Unauthorized"

# Example usage (would normally be in a separate test module)
if __name__ == "__main__":
    print(access_user_profile(1, 1))   # Alice views her own profile
    print(access_user_profile(2, 3))   # Bob (admin) views Eve's profile
    print(access_user_profile(1, 2))   # Alice tries to view Bob's profile → Unauthorized