from typing import Dict, Any

# Example data structures (replace with actual data in production)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin"},
    2: {"role": "user"},
    3: {"role": "user"},
}

def fetch_profile_info(logged_user_id: int, view_user_id: int) -> Any:
    """
    Return the profile of `view_user_id` if the requesting user is authorized.
    
    Authorization rules:
        - A user can view their own profile.
        - An admin (role == 'admin') can view any profile.
    
    Parameters
    ----------
    logged_user_id : int
        ID of the user making the request.
    view_user_id : int
        ID of the profile to be viewed.

    Returns
    -------
    dict or str
        The requested user's profile dictionary, or the string 'Unauthorized'
        if access is denied.
    """
    # Validate that both users exist
    if logged_user_id not in USERS or view_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Self‑view
    if logged_user_id == view_user_id:
        return USER_PROFILES[view_user_id]

    # Admin privilege
    if USERS.get(logged_user_id, {}).get("role") == "admin":
        return USER_PROFILES[view_user_id]

    # Default: unauthorized
    return "Unauthorized"