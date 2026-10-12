from typing import Dict, Any

# Sample data structures (these would normally be populated elsewhere)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"},
    3: {"name": "Charlie", "email": "charlie@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin"},
    2: {"role": "user"},
    3: {"role": "user"},
}


def fetch_profile_data(requester_id: int, profile_id: int) -> Any:
    """
    Return the requested user's profile if the requester is allowed to view it.

    Args:
        requester_id (int): ID of the user making the request.
        profile_id (int): ID of the profile being requested.

    Returns:
        dict: Profile details if access is granted.
        str: 'Unauthorized' if the requester does not have permission.

    Raises:
        KeyError: If either user ID is unknown.
    """
    # Validate existence of both users
    if requester_id not in USERS:
        raise KeyError(f"Requester ID {requester_id} does not exist.")
    if profile_id not in USER_PROFILES:
        raise KeyError(f"Profile ID {profile_id} does not exist.")

    requester_role = USERS[requester_id].get("role", "user")

    # Access logic: admin can view any profile; users can only view their own
    if requester_id == profile_id or requester_role.lower() == "admin":
        # Return a copy to prevent accidental mutation
        return dict(USER_PROFILES[profile_id])

    return "Unauthorized"