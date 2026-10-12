# -*- coding: utf-8 -*-

"""
User profile access control module.
"""

from typing import Dict, Any

# Example data structures (replace with real data in production)
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


def access_user_profile(active_user_id: int, profile_id: int) -> Any:
    """
    Return the requested user profile if access is permitted.

    Parameters
    ----------
    active_user_id : int
        ID of the user making the request.
    profile_id : int
        ID of the profile to view.

    Returns
    -------
    dict | str
        The requested user profile dictionary if access is allowed,
        otherwise the string 'Unauthorized'.

    Notes
    -----
    * A user can view their own profile.
    * An admin (role == 'admin') can view any profile.
    * If either user ID does not exist, the function returns 'Unauthorized'.
      (This avoids leaking existence information.)
    """
    # Validate that both IDs exist in the system
    if active_user_id not in USERS or profile_id not in USER_PROFILES:
        return "Unauthorized"

    # Retrieve the role of the active user
    role = USERS.get(active_user_id, {}).get("role", "")

    # Permission checks
    if active_user_id == profile_id:
        return USER_PROFILES[profile_id]

    if role.lower() == "admin":
        return USER_PROFILES[profile_id]

    # Default: deny access
    return "Unauthorized"


# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(access_user_profile(1, 1))   # Own profile
    print(access_user_profile(2, 3))   # Admin viewing another's profile
    print(access_user_profile(1, 2))   # Unauthorized attempt