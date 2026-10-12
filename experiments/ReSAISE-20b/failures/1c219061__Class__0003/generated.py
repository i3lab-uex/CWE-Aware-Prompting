# -*- coding: utf-8 -*-
"""
User profile access module.

This module defines a single function `get_user_profile` that allows a user
to view their own profile or, if the actor has an administrative role,
view any user's profile.  The implementation follows the principle of
least privilege and checks authorization before returning sensitive data.
"""

from typing import Dict, Any

# Example user and profile data structures.  In a real application these
# would come from a database or an external service.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"email": "alice@example.com", "bio": "Admin extraordinaire"},
    2: {"email": "bob@example.com",   "bio": "Just a regular user"},
    3: {"email": "carol@example.com", "bio": "Python enthusiast"},
}


def get_user_profile(actor_user_id: int, requested_user_id: int) -> Any:
    """
    Return the profile information for ``requested_user_id`` if the actor
    (identified by ``actor_user_id``) is authorized to view it.

    Parameters
    ----------
    actor_user_id : int
        The ID of the user initiating the request.
    requested_user_id : int
        The ID of the profile that is being requested.

    Returns
    -------
    dict or str
        The profile dictionary for the requested user if access is granted.
        Otherwise returns the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either ``actor_user_id`` or ``requested_user_id`` is not present in
        the USERS/USER_PROFILES dictionaries.
    """
    # Validate that both users exist
    if actor_user_id not in USERS:
        raise KeyError(f"Actor user ID {actor_user_id} does not exist.")
    if requested_user_id not in USER_PROFILES:
        raise KeyError(f"Requested user ID {requested_user_id} does not exist.")

    actor = USERS[actor_user_id]
    # Authorization check:
    # - Users can view their own profile
    # - Admins can view any profile
    if actor_user_id == requested_user_id or actor.get("role") == "admin":
        return USER_PROFILES[requested_user_id]

    # Deny access
    return "Unauthorized"


# Example usage (for manual testing only; remove or guard with __name__ == "__main__")
if __name__ == "__main__":
    print(get_user_profile(1, 2))  # Admin viewing Bob's profile
    print(get_user_profile(2, 3))  # Bob trying to view Carol's profile
    print(get_user_profile(2, 2))  # Bob viewing his own profile