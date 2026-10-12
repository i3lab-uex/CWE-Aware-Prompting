# -*- coding: utf-8 -*-

# Example data structures (these would normally be imported or defined elsewhere)
USER_PROFILES = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Eve",   "email": "eve@example.com"},
}

USERS = {
    1: {"username": "alice",   "role": "user"},
    2: {"username": "bob",     "role": "admin"},
    3: {"username": "eve",     "role": "user"},
}


def see_user_profile(current_id: int, target_id: int):
    """
    Return the profile of `target_id` if the requesting user (`current_id`) is
    either the same person or has an admin role.

    Parameters
    ----------
    current_id : int
        ID of the user making the request.
    target_id : int
        ID of the profile being requested.

    Returns
    -------
    dict | str
        The target user's profile dictionary if access is allowed,
        otherwise the string 'Unauthorized'.
    """
    # Basic validation: ensure both IDs exist in our user base
    if current_id not in USERS or target_id not in USER_PROFILES:
        return "Unauthorized"

    # Fetch current user details
    current_user = USERS[current_id]
    role = current_user.get("role", "")

    # Allow if user is requesting own profile
    if current_id == target_id:
        return USER_PROFILES[target_id]

    # Allow admins to view any profile
    if role.lower() == "admin":
        return USER_PROFILES[target_id]

    # All other cases are unauthorized
    return "Unauthorized"