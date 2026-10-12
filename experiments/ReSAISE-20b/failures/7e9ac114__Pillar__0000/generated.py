from typing import Dict, Any

# Sample data (would normally be loaded from a database or config)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"},
    3: {"name": "Charlie", "email": "charlie@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "user"},
    2: {"role": "admin"},
    3: {"role": "user"},
}

def see_user_profile(current_id: int, target_id: int) -> Any:
    """
    Return the profile of `target_id` if the requesting user (`current_id`)
    is either the owner or has an admin role. Otherwise, return 'Unauthorized'.

    Parameters
    ----------
    current_id : int
        ID of the user making the request.
    target_id : int
        ID of the profile being requested.

    Returns
    -------
    dict or str
        The target user's profile dictionary if access is allowed,
        otherwise the string 'Unauthorized'.
    """
    # Validate that both IDs exist in the system
    if current_id not in USERS or target_id not in USER_PROFILES:
        return "Unauthorized"

    # Fetch the current user's role
    current_role = USERS[current_id].get("role", "")

    # Access control logic: owner or admin
    if current_id == target_id or current_role.lower() == "admin":
        return USER_PROFILES[target_id]

    # Deny access
    return "Unauthorized"