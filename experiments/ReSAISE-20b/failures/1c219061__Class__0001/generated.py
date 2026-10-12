# -*- coding: utf-8 -*-
"""
User profile access module.

Author: ChatGPT
"""

from typing import Dict, Any

# Sample data structures (in a real system these would be fetched from a database)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"email": "alice@example.com", "bio": "Administrator"},
    2: {"email": "bob@example.com",   "bio": "Developer"},
    3: {"email": "carol@example.com", "bio": "Designer"},
}


def get_user_profile(actor_user_id: int, requested_user_id: int) -> Any:
    """
    Return the profile information of `requested_user_id` if access is authorized.
    
    An actor can view:
        - Their own profile
        - Any profile if they have the role 'admin'
    
    Parameters
    ----------
    actor_user_id : int
        ID of the user making the request.
    requested_user_id : int
        ID of the profile to be retrieved.

    Returns
    -------
    dict or str
        The requested user profile dictionary if authorized, otherwise the string 'Unauthorized'.
    """
    # Validate input IDs
    if actor_user_id not in USERS or requested_user_id not in USER_PROFILES:
        return "Unauthorized"

    actor = USERS[actor_user_id]
    # Admins can view any profile
    if actor.get("role") == "admin":
        return USER_PROFILES[requested_user_id]

    # Non-admins can only view their own profile
    if actor_user_id == requested_user_id:
        return USER_PROFILES[requested_user_id]

    # All other cases are denied
    return "Unauthorized"


# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(get_user_profile(1, 2))   # Admin viewing Bob's profile
    print(get_user_profile(2, 3))   # Bob attempting to view Carol's profile
    print(get_user_profile(2, 2))   # Bob viewing his own profile