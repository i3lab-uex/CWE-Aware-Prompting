from typing import Dict, Any

# Example data structures (replace with actual data in production)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice",   "role": "admin"},
    2: {"name": "Bob",     "role": "user"},
    3: {"name": "Carol",   "role": "user"},
}

def access_user_profile(requesting_user_id: int, viewing_user_id: int) -> Any:
    """
    Return the requested user profile if the requesting user is authorized.
    
    Parameters
    ----------
    requesting_user_id : int
        ID of the user making the request.
    viewing_user_id : int
        ID of the profile being requested.

    Returns
    -------
    dict or str
        The user profile dictionary if access is granted, otherwise the string
        'Unauthorized'.
    """
    # Validate that both IDs exist in the system
    if requesting_user_id not in USERS or viewing_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Fetch the role of the requesting user
    requester_role = USERS[requesting_user_id].get("role", "").lower()

    # Allow access if:
    # 1. The requester is the owner of the profile
    # 2. The requester has an admin role
    if requesting_user_id == viewing_user_id or requester_role == "admin":
        # Return a copy to prevent accidental mutation of the global store
        return dict(USER_PROFILES[viewing_user_id])

    # All other cases are unauthorized
    return "Unauthorized"