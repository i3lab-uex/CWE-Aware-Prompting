# -*- coding: utf-8 -*-

"""
User profile access module.

This module implements a simple authorization check to allow users to view
their own profiles, while administrators are granted access to any profile.
The implementation follows the best practices for avoiding CWE-862
(Missing Authorization).
"""

from typing import Dict, Any

# Sample data structures (replace with actual database lookups in production)
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


def get_profile_info(acting_user_id: int, viewing_user_id: int) -> Any:
    """
    Retrieve a user's profile if the acting user is authorized.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user making the request.
    viewing_user_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict or str
        The profile dictionary if access is granted,
        otherwise the string 'Unauthorized'.

    Notes
    -----
    * Only administrators (role == 'admin') may view any profile.
    * Regular users may only view their own profile.
    * If either user ID is unknown, the request is denied.
    """
    # Verify that both users exist
    acting_user = USERS.get(acting_user_id)
    if not acting_user:
        return "Unauthorized"

    # Authorization check
    is_admin = acting_user.get("role") == "admin"
    if not (is_admin or acting_user_id == viewing_user_id):
        return "Unauthorized"

    # Fetch the requested profile
    profile = USER_PROFILES.get(viewing_user_id)
    if not profile:
        return "Unauthorized"

    # Return a copy to avoid accidental mutation of the global store
    return profile.copy()


# Example usage (for manual testing)
if __name__ == "__main__":
    print(get_profile_info(1, 1))   # Alice viewing her own profile
    print(get_profile_info(1, 2))   # Alice attempting to view Bob's profile
    print(get_profile_info(2, 3))   # Admin viewing Carol's profile