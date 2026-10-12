# -*- coding: utf-8 -*-

"""
Secure user profile access module.

This module provides the `access_user_profile` function, which enforces
proper access control when retrieving user profiles. The function ensures
that only the profile owner or users with an 'admin' role can view a
profile. All other attempts result in an explicit 'Unauthorized'
response, preventing CWE-284 (Improper Access Control) vulnerabilities.
"""

from typing import Dict, Any

# Example data structures. In a real application these would come from
# a database or an external service.
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


def access_user_profile(active_user_id: int, profile_id: int) -> Any:
    """
    Retrieve a user profile if the requesting user has permission.

    Parameters
    ----------
    active_user_id : int
        The ID of the user making the request.
    profile_id : int
        The ID of the profile to be retrieved.

    Returns
    -------
    dict | str
        The requested user profile dictionary if access is granted,
        otherwise the string 'Unauthorized'.

    Notes
    -----
    - A user may view their own profile.
    - Users with the role 'admin' can view any profile.
    - All other access attempts return 'Unauthorized'.
    """
    # Validate that both users exist
    if active_user_id not in USERS or profile_id not in USER_PROFILES:
        return "Unauthorized"

    # Owner check
    if active_user_id == profile_id:
        return USER_PROFILES[profile_id]

    # Admin check
    active_user = USERS.get(active_user_id)
    if active_user and active_user.get("role") == "admin":
        return USER_PROFILES[profile_id]

    # Default: deny access
    return "Unauthorized"


# Example usage (for manual testing only)
if __name__ == "__main__":
    print(access_user_profile(1, 2))   # Admin accessing Bob's profile
    print(access_user_profile(2, 2))   # Bob accessing own profile
    print(access_user_profile(3, 1))   # Carol trying to access Alice's profile