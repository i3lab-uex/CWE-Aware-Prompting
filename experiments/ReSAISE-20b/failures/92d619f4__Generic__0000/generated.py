# ------------------------------
# User profile access module
# ------------------------------

from typing import Dict, Any

# Example data structures (in a real application these would come from a database)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"email": "alice@example.com", "bio": "Admin of the system"},
    2: {"email": "bob@example.com",   "bio": "Just a regular user"},
    3: {"email": "carol@example.com", "bio": "Another regular user"},
}


def fetch_profile_info(logged_user_id: int, view_user_id: int) -> Any:
    """
    Return the profile information of `view_user_id` if access is allowed.

    Parameters
    ----------
    logged_user_id : int
        The ID of the user initiating the request.
    view_user_id : int
        The ID of the profile to be viewed.

    Returns
    -------
    dict or str
        The requested user's profile dictionary if authorized,
        otherwise the string 'Unauthorized'.

    Raises
    ------
    ValueError
        If either user ID does not exist in the system.
    """
    # Validate existence of both users
    if logged_user_id not in USERS:
        raise ValueError(f"Logged user ID {logged_user_id} does not exist.")
    if view_user_id not in USER_PROFILES:
        raise ValueError(f"Profile ID {view_user_id} does not exist.")

    # Allow self‑view
    if logged_user_id == view_user_id:
        return USER_PROFILES[view_user_id]

    # Check if the logged user has admin privileges
    logged_role = USERS[logged_user_id].get("role", "").lower()
    if logged_role == "admin":
        return USER_PROFILES[view_user_id]

    # If none of the above, deny access
    return "Unauthorized"


# ------------------------------
# Example usage (for testing)
# ------------------------------
if __name__ == "__main__":
    # Admin viewing another user's profile
    print(fetch_profile_info(1, 2))   # Expected: Bob's profile

    # Regular user attempting to view another user's profile
    print(fetch_profile_info(2, 3))   # Expected: 'Unauthorized'

    # User viewing own profile
    print(fetch_profile_info(3, 3))   # Expected: Carol's profile