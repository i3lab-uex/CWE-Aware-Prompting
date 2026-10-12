from typing import Dict, Any

# Example data structures (replace with real ones in your application)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"bio": "Admin profile",      "email": "alice@example.com"},
    2: {"bio": "Bob's bio",          "email": "bob@example.com"},
    3: {"bio": "Carol's bio",        "email": "carol@example.com"},
}

def access_user_profile(active_user_id: int, profile_id: int) -> Dict[str, Any] | str:
    """
    Return the requested user profile if access is allowed.
    
    Parameters
    ----------
    active_user_id : int
        ID of the user making the request.
    profile_id : int
        ID of the profile to view.
    
    Returns
    -------
    dict or str
        The requested profile dictionary, or 'Unauthorized' if access is denied.
    
    Raises
    ------
    KeyError
        If either the active user or requested profile does not exist.
    """
    
    # Validate that both users exist
    if active_user_id not in USERS:
        raise KeyError(f"Active user ID {active_user_id} does not exist.")
    if profile_id not in USER_PROFILES:
        raise KeyError(f"Profile ID {profile_id} does not exist.")
    
    active_user = USERS[active_user_id]
    
    # Allow if user is admin or accessing own profile
    if active_user.get("role") == "admin" or active_user_id == profile_id:
        return USER_PROFILES[profile_id]
    
    # Deny otherwise
    return "Unauthorized"