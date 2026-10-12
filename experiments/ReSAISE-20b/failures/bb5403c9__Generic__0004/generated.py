# Sample data structures (replace with actual data in real usage)
USER_PROFILES = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS = {
    1: {"role": "admin"},
    2: {"role": "user"},
    3: {"role": "user"},
}

def get_profile_info(acting_user_id: int, viewing_user_id: int):
    """
    Return the profile details for `viewing_user_id` if the request is authorized.
    
    Parameters
    ----------
    acting_user_id : int
        The ID of the user making the request.
    viewing_user_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict or str
        The profile dictionary if access is granted, otherwise the string 'Unauthorized'.
    """
    # Validate that both users exist
    if acting_user_id not in USERS or viewing_user_id not in USER_PROFILES:
        return "Unauthorized"

    # If the user is requesting their own profile
    if acting_user_id == viewing_user_id:
        return USER_PROFILES[viewing_user_id]

    # If the acting user is an administrator
    if USERS.get(acting_user_id, {}).get("role") == "admin":
        return USER_PROFILES[viewing_user_id]

    # Otherwise, deny access
    return "Unauthorized"