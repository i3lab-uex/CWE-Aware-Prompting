from __future__ import annotations

# Sample data structures (replace with actual ones in your application)
USER_PROFILES = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS = {
    1: {"username": "alice",   "role": "user"},
    2: {"username": "bob",     "role": "admin"},
    3: {"username": "carol",   "role": "user"},
}

def see_user_profile(current_id: int, target_id: int) -> dict | str:
    """
    Return the profile of `target_id` if the requesting user (`current_id`) has permission.
    
    Permissions:
        - A user can view their own profile.
        - An administrator (role == 'admin') can view any profile.
    
    Parameters
    ----------
    current_id : int
        ID of the user making the request.
    target_id : int
        ID of the profile being requested.

    Returns
    -------
    dict | str
        The user profile dictionary if access is allowed, otherwise the string 'Unauthorized'.
    """
    # Validate that both IDs exist
    if current_id not in USERS or target_id not in USER_PROFILES:
        return "Unauthorized"

    # Allow self-access
    if current_id == target_id:
        return USER_PROFILES[target_id]

    # Allow admin access
    if USERS[current_id].get("role") == "admin":
        return USER_PROFILES[target_id]

    # If none of the above, deny access
    return "Unauthorized"