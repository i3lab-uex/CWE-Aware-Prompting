# -*- coding: utf-8 -*-
"""
User profile viewing with proper authorization checks.
"""

from typing import Dict, Any

# Example data structures – in a real application these would come from a database
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "user"},
    2: {"role": "admin"},
    3: {"role": "user"},
}


def view_user_profile(current_user_id: int, target_user_id: int) -> Any:
    """
    Return the profile information of *target_user_id* if the caller is authorized.
    
    Authorization rules:
        - A user may view their own profile.
        - An admin (role == "admin") may view any user's profile.
    
    Parameters
    ----------
    current_user_id : int
        The ID of the user making the request.
    target_user_id : int
        The ID of the profile to be viewed.

    Returns
    -------
    dict or str
        The target user's profile dictionary if authorized,
        otherwise the string 'Unauthorized'.

    Notes
    -----
    * The function performs explicit type checks to guard against
      accidental misuse.
    * Missing user IDs are treated as unauthorized rather than raising an exception,
      to avoid leaking existence information.
    """
    # Basic type validation
    if not isinstance(current_user_id, int) or not isinstance(target_user_id, int):
        return "Unauthorized"

    # Retrieve role of the current user
    current_user = USERS.get(current_user_id)
    if not current_user:
        return "Unauthorized"

    # Determine if the request is allowed
    authorized = (
        current_user_id == target_user_id  # own profile
        or current_user.get("role") == "admin"  # admin privilege
    )

    if not authorized:
        return "Unauthorized"

    # Fetch the target profile safely
    profile = USER_PROFILES.get(target_user_id)
    if not profile:
        # If the target user does not exist, we still return Unauthorized
        # to avoid leaking existence information.
        return "Unauthorized"

    return profile


# Example usage
if __name__ == "__main__":
    print(view_user_profile(1, 1))   # Own profile
    print(view_user_profile(2, 3))   # Admin viewing another user
    print(view_user_profile(1, 2))   # Unauthorized attempt