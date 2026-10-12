# -*- coding: utf-8 -*-

"""
User profile viewing module.

This module provides a single function `view_user_profile` that returns
profile information for a user if the requester is authorized to view it.
The authorization rules are:

* A user may view their own profile.
* An administrator (role == "admin") may view any user's profile.

The function is deliberately simple to keep the focus on proper access
control.  It uses only standard library components.
"""

from typing import Dict, Any

# Example data structures.  In a real application these would be
# retrieved from a database or another persistent store.
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


def view_user_profile(current_user_id: int, target_user_id: int) -> Any:
    """
    Return the profile information for `target_user_id` if the requester
    identified by `current_user_id` is authorized to view it.

    Parameters
    ----------
    current_user_id : int
        The user ID of the actor requesting the data.
    target_user_id : int
        The user ID whose profile is being requested.

    Returns
    -------
    dict or str
        The target user's profile dictionary if authorized,
        otherwise the string 'Unauthorized'.

    Notes
    -----
    * The function performs a strict role check and does not expose any
      additional data beyond what is stored in `USER_PROFILES`.
    * If either user ID does not exist, the function returns 'Unauthorized'
      to avoid leaking information about existing users.
    """
    # Verify that both user IDs exist in the system
    if current_user_id not in USERS or target_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Retrieve the current user's role
    current_role = USERS[current_user_id].get("role", "")

    # Authorization logic:
    # - Allow if the requester is the same as the target
    # - Allow if the requester has admin privileges
    if current_user_id == target_user_id or current_role.lower() == "admin":
        # Return a copy to prevent accidental mutation of the original data
        return dict(USER_PROFILES[target_user_id])

    # If none of the above, deny access
    return "Unauthorized"


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     print(view_user_profile(1, 1))  # Alice viewing her own profile
#     print(view_user_profile(2, 3))  # Admin Bob viewing Carol's profile
#     print(view_user_profile(1, 3))  # Alice trying to view Carol's profile