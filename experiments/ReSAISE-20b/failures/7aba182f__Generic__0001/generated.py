from __future__ import annotations

# Sample data structures – in a real application these would be populated elsewhere
USERS = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob", "role": "user"},
    3: {"name": "Charlie", "role": "user"},
}

USER_PROFILES = {
    1: {"email": "alice@example.com", "age": 30},
    2: {"email": "bob@example.com", "age": 25},
    3: {"email": "charlie@example.com", "age": 28},
}

def access_user_profile(requesting_user_id: int, viewing_user_id: int) -> dict | str:
    """
    Return the profile of `viewing_user_id` if the requesting user has permission.
    
    Permission rules:
        - A user may view their own profile.
        - Users with the role 'admin' may view any profile.
    
    Parameters
    ----------
    requesting_user_id : int
        ID of the user making the request.
    viewing_user_id : int
        ID of the profile being requested.
    
    Returns
    -------
    dict | str
        The user profile dictionary if access is granted, otherwise the string 'Unauthorized'.
    """
    
    # Basic validation: ensure both users exist
    if requesting_user_id not in USERS or viewing_user_id not in USER_PROFILES:
        return "Unauthorized"
    
    # Check if the requesting user is an admin
    requester_role = USERS[requesting_user_id].get("role", "").lower()
    if requester_role == "admin":
        return USER_PROFILES[viewing_user_id]
    
    # Non-admins may only view their own profile
    if requesting_user_id == viewing_user_id:
        return USER_PROFILES[viewing_user_id]
    
    # All other cases are unauthorized
    return "Unauthorized"