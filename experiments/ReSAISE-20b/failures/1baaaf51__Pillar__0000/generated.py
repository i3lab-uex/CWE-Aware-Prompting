# -*- coding: utf-8 -*-

from typing import Any, Dict

# Example data structures. In a real application these would be fetched from
# a database or an external service.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"bio": "Admin of the system", "email": "alice@example.com"},
    2: {"bio": "Developer",           "email": "bob@example.com"},
    3: {"bio": "Designer",            "email": "carol@example.com"},
}


def access_user_profile(active_user_id: int, profile_id: int) -> Any:
    """
    Return the requested user's profile if access is allowed.

    Parameters
    ----------
    active_user_id : int
        ID of the user making the request.
    profile_id : int
        ID of the profile being requested.

    Returns
    -------
    dict | str
        The profile dictionary if access is granted, otherwise the string
        'Unauthorized'.

    Raises
    ------
    KeyError
        If either user ID is not present in USERS or USER_PROFILES.
    """
    # Validate input types
    if not isinstance(active_user_id, int) or not isinstance(profile_id, int):
        raise TypeError("User IDs must be integers")

    # Ensure the requested profile exists
    try:
        requested_profile = USER_PROFILES[profile_id]
    except KeyError as exc:
        raise KeyError(f"Profile ID {profile_id} does not exist") from exc

    # Ensure the active user exists
    try:
        active_user = USERS[active_user_id]
    except KeyError as exc:
        raise KeyError(f"Active user ID {active_user_id} does not exist") from exc

    # Access control logic
    is_owner = active_user_id == profile_id
    is_admin = active_user.get("role") == "admin"

    if is_owner or is_admin:
        # Return a copy to prevent accidental modification of the stored data
        return dict(requested_profile)
    else:
        # Do not leak any profile information to unauthorized users
        return "Unauthorized"