from typing import Dict, Any

# Sample data structures (replace with real ones in your application)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Eve",   "email": "eve@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"username": "alice",   "role": "user"},
    2: {"username": "bob",     "role": "admin"},
    3: {"username": "eve",     "role": "user"},
}

def fetch_profile_info(logged_user_id: int, view_user_id: int) -> Any:
    """
    Return the profile information of `view_user_id` if the requester is authorized.
    
    Authorization rules:
      - A user can view their own profile.
      - An admin (role == 'admin') can view any profile.
    
    Parameters:
        logged_user_id: ID of the user making the request.
        view_user_id:   ID of the profile to be viewed.
    
    Returns:
        The requested user's profile dictionary or the string 'Unauthorized'.
    """
    # Validate that both user IDs exist
    if logged_user_id not in USERS or view_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Check if the logged-in user is viewing their own profile
    if logged_user_id == view_user_id:
        return USER_PROFILES[view_user_id]

    # Check if the logged-in user has admin privileges
    logged_role = USERS[logged_user_id].get("role")
    if logged_role == "admin":
        return USER_PROFILES[view_user_id]

    # If none of the above, deny access
    return "Unauthorized"

# Example usage (for testing purposes)
if __name__ == "__main__":
    print(fetch_profile_info(1, 1))  # Own profile
    print(fetch_profile_info(2, 3))  # Admin viewing another user
    print(fetch_profile_info(1, 2))  # Unauthorized attempt