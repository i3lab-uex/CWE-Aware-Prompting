# -*- coding: utf-8 -*-
"""
Access control for user profiles.

The function `access_user_profile` checks whether the requesting user
is allowed to view the profile of another user.  A request is permitted
if:

* The requesting user id matches the target profile id (self‑view).
* The requesting user has a role of 'admin' or 'superuser'.

If the request is not allowed, the string ``"Unauthorized"`` is returned.

The implementation follows the principle of least privilege and
handles missing data defensively to avoid information leakage.
"""

from __future__ import annotations

# Example user and profile data
USERS: dict[int, dict[str, str]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "superuser"},
    4: {"name": "Dave",  "role": "user"},
}

USER_PROFILES: dict[int, dict[str, str]] = {
    1: {"email": "alice@example.com", "bio": "Administrator"},
    2: {"email": "bob@example.com",   "bio": "Developer"},
    3: {"email": "carol@example.com", "bio": "Lead Architect"},
    4: {"email": "dave@example.com",  "bio": "Intern"},
}

def access_user_profile(requesting_user_id: int, viewing_user_id: int) -> dict[str, str] | str:
    """
    Return the profile of `viewing_user_id` if the request is authorized,
    otherwise return 'Unauthorized'.

    Parameters
    ----------
    requesting_user_id : int
        The ID of the user making the request.
    viewing_user_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict[str, str] | str
        The target user profile or the string 'Unauthorized'.
    """
    # Validate that both users exist
    requester = USERS.get(requesting_user_id)
    target_profile = USER_PROFILES.get(viewing_user_id)

    if requester is None or target_profile is None:
        # If either ID is unknown, deny access to avoid leaking existence
        return "Unauthorized"

    # Self‑view is always allowed
    if requesting_user_id == viewing_user_id:
        return target_profile

    # Administrators can view any profile
    if requester.get("role") in {"admin", "superuser"}:
        return target_profile

    # Default: deny access
    return "Unauthorized"

# Example usage (uncomment to test)
# print(access_user_profile(1, 2))  # admin viewing Bob
# print(access_user_profile(2, 1))  # Bob trying to view Alice (should be Unauthorized)
# print(access_user_profile(3, 4))  # superuser viewing Dave