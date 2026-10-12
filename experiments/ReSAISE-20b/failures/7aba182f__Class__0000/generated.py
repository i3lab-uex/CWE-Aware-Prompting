# -*- coding: utf-8 -*-
"""
Secure user profile access module.
"""

from typing import Dict, Any

# Example data structures. In a real application these would come from a database.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"email": "alice@example.com", "age": 30},
    2: {"email": "bob@example.com",   "age": 25},
    3: {"email": "carol@example.com", "age": 28},
}


def access_user_profile(requesting_user_id: int, viewing_user_id: int) -> Any:
    """
    Return the profile of `viewing_user_id` if the requesting user is authorized.

    Parameters
    ----------
    requesting_user_id : int
        ID of the user making the request.
    viewing_user_id : int
        ID of the profile being requested.

    Returns
    -------
    dict | str
        The user profile dictionary if access is granted; otherwise the string
        'Unauthorized'.

    Notes
    -----
    - A user can view their own profile.
    - An admin (role == 'admin') can view any user's profile.
    - The function performs explicit authorization checks to avoid CWE-862
      (Missing Authorization).
    """
    # Validate that both users exist
    requester = USERS.get(requesting_user_id)
    if requester is None:
        return "Unauthorized"

    # Check for self-access
    if requesting_user_id == viewing_user_id:
        return USER_PROFILES.get(viewing_user_id, "Unauthorized")

    # Check admin privilege
    if requester.get("role") == "admin":
        return USER_PROFILES.get(viewing_user_id, "Unauthorized")

    # No permission granted
    return "Unauthorized"


# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(access_user_profile(1, 2))  # admin viewing Bob's profile
    print(access_user_profile(2, 3))  # Bob trying to view Carol's profile
    print(access_user_profile(2, 2))  # Bob viewing his own profile