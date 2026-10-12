from __future__ import annotations

# Sample data structures (replace with actual data in real usage)
USER_PROFILES = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS = {
    1: {"role": "user"},
    2: {"role": "admin"},
    3: {"role": "user"},
}

def access_user_profile(requesting_user_id: int, viewing_user_id: int):
    """
    Return the profile of `viewing_user_id` if the requesting user is either
    the same person or has an 'admin' role. Otherwise return 'Unauthorized'.

    Parameters:
        requesting_user_id (int): ID of the user making the request.
        viewing_user_id (int):   ID of the profile being requested.

    Returns:
        dict | str: The user profile dictionary if access is granted,
                    otherwise the string 'Unauthorized'.
    """
    # Validate that both user IDs exist
    if requesting_user_id not in USERS or viewing_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Fetch role of the requesting user
    requester_role = USERS[requesting_user_id].get("role", "user")

    # Access control: same user or admin
    if requester_role == "admin" or requesting_user_id == viewing_user_id:
        return USER_PROFILES[viewing_user_id]

    # Default: unauthorized
    return "Unauthorized"