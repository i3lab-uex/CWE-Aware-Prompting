# -*- coding: utf-8 -*-
"""
Secure user profile viewing implementation.

The function ensures that only the owner of a profile or an administrator
can access any user's profile data.  It protects against CWE-284
Improper Access Control by performing explicit checks on the user role
and identity before returning sensitive information.

Author: OpenAI ChatGPT
"""

from typing import Dict, Any

# Example data – in a real system these would come from a database
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

# Role mapping: user_id -> role
USERS: Dict[int, str] = {
    1: "user",
    2: "admin",
    3: "user",
}

def view_user_profile(current_user_id: int, target_user_id: int) -> Any:
    """
    Return the profile of *target_user_id* if the requesting user is
    authorized.

    Parameters
    ----------
    current_user_id : int
        The ID of the user making the request.
    target_user_id : int
        The ID of the profile to be viewed.

    Returns
    -------
    dict | str
        The requested user profile dictionary if access is granted,
        otherwise the string 'Unauthorized'.

    Notes
    -----
    * A user may view their own profile.
    * An administrator (role 'admin') may view any profile.
    * If either user ID does not exist, the function returns
      'Unauthorized' rather than revealing existence of accounts.
    """
    # Validate that both user IDs exist in the system
    if current_user_id not in USERS or target_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Determine the role of the requesting user
    requester_role = USERS.get(current_user_id)

    # Authorization logic:
    # - Owner can view their own profile
    # - Admin can view any profile
    if current_user_id == target_user_id or requester_role == "admin":
        # Return a copy to prevent accidental mutation of the global data
        return dict(USER_PROFILES[target_user_id])

    # If none of the conditions are met, deny access
    return "Unauthorized"

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    print(view_user_profile(1, 1))  # Alice viewing herself
    print(view_user_profile(2, 3))  # Admin Bob viewing Carol
    print(view_user_profile(1, 2))  # Alice trying to view Bob (unauthorized)