from typing import Dict, Any

# Example data structures (replace with actual data in production)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"bio": "Admin of the system", "email": "alice@example.com"},
    2: {"bio": "Regular user",       "email": "bob@example.com"},
    3: {"bio": "Another regular user","email": "carol@example.com"},
}

def get_user_profile(actor_user_id: int, requested_user_id: int) -> Any:
    """
    Return the profile of `requested_user_id` if the actor has permission.

    Parameters
    ----------
    actor_user_id : int
        ID of the user making the request.
    requested_user_id : int
        ID of the profile to retrieve.

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
    # Validate that both users exist
    if actor_user_id not in USERS:
        raise ValueError(f"Actor user ID {actor_user_id} does not exist.")
    if requested_user_id not in USER_PROFILES:
        raise ValueError(f"Requested user ID {requested_user_id} does not exist.")

    # Determine actor's role
    actor_role = USERS[actor_user_id].get("role", "").lower()

    # Access control: allow if actor is the same as requested or an admin
    if actor_user_id == requested_user_id or actor_role == "admin":
        return USER_PROFILES[requested_user_id]

    # Deny access otherwise
    return "Unauthorized"