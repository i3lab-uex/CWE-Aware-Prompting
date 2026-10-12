from typing import Dict, Any

# Example data structures; in a real system these would be loaded from a database
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin"},
    2: {"role": "user"},
    3: {"role": "user"},
}


def get_profile_info(acting_user_id: int, viewing_user_id: int) -> Any:
    """
    Return profile details for the requested user if the acting user has permission.

    Parameters
    ----------
    acting_user_id : int
        ID of the user making the request.
    viewing_user_id : int
        ID of the profile being requested.

    Returns
    -------
    dict or str
        The profile dictionary if access is granted, otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either user ID does not exist in the USERS or USER_PROFILES dictionaries.
    """
    # Validate existence of users
    if acting_user_id not in USERS:
        raise KeyError(f"Acting user ID {acting_user_id} does not exist.")
    if viewing_user_id not in USER_PROFILES:
        raise KeyError(f"Viewing user ID {viewing_user_id} does not exist.")

    # Permission check
    if acting_user_id == viewing_user_id:
        return USER_PROFILES[viewing_user_id]

    if USERS.get(acting_user_id, {}).get("role") == "admin":
        return USER_PROFILES[viewing_user_id]

    return "Unauthorized"