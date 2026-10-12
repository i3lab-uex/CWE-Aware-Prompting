# Example data structures (to be replaced with real ones in the application)
USER_PROFILES = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS = {
    1: {"role": "admin",   "name": "Alice"},
    2: {"role": "user",    "name": "Bob"},
    3: {"role": "user",    "name": "Carol"},
}


def get_profile_info(acting_user_id: int, viewing_user_id: int):
    """
    Return the profile details for `viewing_user_id` if the request is authorized.
    
    Parameters
    ----------
    acting_user_id : int
        The user id of the individual making the request.
    viewing_user_id : int
        The user id whose profile is being requested.

    Returns
    -------
    dict or str
        The profile dictionary if access is granted, otherwise the string 'Unauthorized'.
    
    Raises
    ------
    KeyError
        If either user id is not present in the USERS or USER_PROFILES dictionaries.
    """
    # Validate existence of both users
    if acting_user_id not in USERS:
        raise KeyError(f"Acting user id {acting_user_id} does not exist.")
    if viewing_user_id not in USER_PROFILES:
        raise KeyError(f"Viewing user id {viewing_user_id} does not exist.")

    # Determine if the acting user is authorized
    acting_role = USERS[acting_user_id].get("role", "user")
    if acting_user_id == viewing_user_id or acting_role.lower() == "admin":
        # Return a copy to prevent accidental modification of the original data
        return USER_PROFILES[viewing_user_id].copy()
    
    # Unauthorized access attempt
    return "Unauthorized"