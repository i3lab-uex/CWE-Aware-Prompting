from typing import Dict, Any

# Example data structures (replace with actual data in real usage)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "user"},
    2: {"role": "admin"},
    3: {"role": "user"},
}


def see_user_profile(current_id: int, target_id: int) -> Any:
    """
    Return the profile of `target_id` if the requester is allowed to view it.
    An administrator can view any profile; otherwise a user may only view their own.

    Parameters
    ----------
    current_id : int
        ID of the user making the request.
    target_id : int
        ID of the profile being requested.

    Returns
    -------
    dict or str
        The target user's profile dictionary if access is granted,
        otherwise the string 'Unauthorized'.
    """
    # Validate that both IDs exist
    if current_id not in USERS or target_id not in USER_PROFILES:
        return "Unauthorized"

    # Allow self‑view
    if current_id == target_id:
        return USER_PROFILES[target_id]

    # Allow admin view
    if USERS[current_id].get("role") == "admin":
        return USER_PROFILES[target_id]

    # Deny all other cases
    return "Unauthorized"