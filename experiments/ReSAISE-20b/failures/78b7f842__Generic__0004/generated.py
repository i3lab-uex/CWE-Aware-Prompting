# user_profile_viewer.py

from typing import Dict, Any

# Example data structures (replace with real data in production)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"}
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "user"},
    2: {"role": "admin"},
    3: {"role": "user"}
}


def view_user_profile(current_user_id: int, target_user_id: int) -> Any:
    """
    Return the profile of `target_user_id` if the requesting user
    (`current_user_id`) is authorized to view it.

    Authorization rules:
        - A user can view their own profile.
        - An admin (role == 'admin') can view any profile.

    Parameters
    ----------
    current_user_id : int
        ID of the user making the request.
    target_user_id : int
        ID of the profile to be retrieved.

    Returns
    -------
    dict | str
        The target user's profile dictionary if authorized,
        otherwise the string 'Unauthorized'.
    """
    # Basic validation of user existence
    if current_user_id not in USERS:
        return "Unauthorized"
    if target_user_id not in USER_PROFILES:
        return "User not found"

    # Determine the role of the current user
    role = USERS[current_user_id].get("role", "")

    # Check authorization
    if current_user_id == target_user_id or role.lower() == "admin":
        return USER_PROFILES[target_user_id]

    # Default: not authorized
    return "Unauthorized"


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    print(view_user_profile(1, 1))   # Alice views own profile
    print(view_user_profile(2, 3))   # Admin Bob views Carol's profile
    print(view_user_profile(3, 1))   # Carol tries to view Alice's profile (Unauthorized)