from typing import Any, Dict

# Sample data structures (to be replaced with actual application data)
USERS: Dict[int, Dict[str, Any]] = {
    # Example:
    # 1: {"name": "Alice", "role": "admin"},
    # 2: {"name": "Bob",   "role": "user"}
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    # Example:
    # 1: {"email": "alice@example.com", "age": 30},
    # 2: {"email": "bob@example.com",   "age": 25}
}

def fetch_profile_info(logged_user_id: int, view_user_id: int) -> Any:
    """
    Return the profile information for `view_user_id` if the caller is authorized.
    
    Authorization rules:
      * A user can view their own profile.
      * An admin (role == 'admin') can view any user's profile.
    
    Parameters
    ----------
    logged_user_id : int
        ID of the user making the request.
    view_user_id : int
        ID of the profile to be retrieved.
    
    Returns
    -------
    dict | str
        The requested user's profile data or the string 'Unauthorized'.
    
    Raises
    ------
    KeyError
        If either `logged_user_id` or `view_user_id` does not exist in the system.
    """
    # Validate existence of users
    if logged_user_id not in USERS:
        raise KeyError(f"Logged user ID {logged_user_id} does not exist.")
    if view_user_id not in USER_PROFILES:
        raise KeyError(f"Profile ID {view_user_id} does not exist.")
    
    # Determine role of the logged user
    logged_role = USERS[logged_user_id].get("role", "").lower()
    
    # Authorization check
    if logged_user_id != view_user_id and logged_role != "admin":
        return "Unauthorized"
    
    # Return the requested profile
    return USER_PROFILES[view_user_id]