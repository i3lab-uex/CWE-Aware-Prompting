from typing import Dict, Any

# Example data structures (replace with actual application data)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin"},
    2: {"role": "user"},
}

def view_user_profile(current_user_id: int, target_user_id: int) -> Any:
    """
    Return the profile of `target_user_id` if the requester is authorized.

    Authorization rules:
        * A user can view their own profile.
        * An admin (role == 'admin') can view any profile.

    Parameters
    ----------
    current_user_id : int
        The ID of the user making the request.
    target_user_id : int
        The ID of the profile to be viewed.

    Returns
    -------
    dict | str
        The requested user profile as a dictionary if authorized,
        otherwise the string 'Unauthorized'.
    """
    # Validate existence of target profile
    if target_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Fetch current user role safely
    current_user = USERS.get(current_user_id)
    if not current_user:
        return "Unauthorized"

    role = current_user.get("role", "").lower()

    # Authorization check
    if current_user_id == target_user_id or role == "admin":
        # Return a shallow copy to avoid accidental mutation
        return dict(USER_PROFILES[target_user_id])

    # If none of the above, deny access
    return "Unauthorized"