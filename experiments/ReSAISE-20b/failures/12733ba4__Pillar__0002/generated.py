from typing import Dict, Any

# Example data structures (replace with actual data in production)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Eve",   "email": "eve@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin"},
    2: {"role": "user"},
    3: {"role": "user"},
}

def display_user_profile(active_user_id: int, profile_user_id: int) -> Any:
    """
    Return the requested user profile if the active user has permission.
    
    Parameters
    ----------
    active_user_id : int
        The ID of the user making the request.
    profile_user_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict or str
        The user profile dictionary if access is allowed,
        otherwise the string 'Unauthorized'.
    """
    # Validate that both user IDs exist
    if active_user_id not in USERS or profile_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Determine the role of the active user
    role = USERS[active_user_id].get("role", "")

    # Allow access if the active user is an admin or accessing their own profile
    if role == "admin" or active_user_id == profile_user_id:
        return USER_PROFILES[profile_user_id]

    # All other cases are unauthorized
    return "Unauthorized"