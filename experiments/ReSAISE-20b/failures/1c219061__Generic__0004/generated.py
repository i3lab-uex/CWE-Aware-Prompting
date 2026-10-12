from __future__ import annotations

# Sample data structures (replace with actual ones in your application)
USERS = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES = {
    1: {"bio": "Admin of the system", "email": "alice@example.com"},
    2: {"bio": "Regular user",        "email": "bob@example.com"},
    3: {"bio": "Another user",       "email": "carol@example.com"},
}

def get_user_profile(actor_user_id: int, requested_user_id: int):
    """
    Return the profile information of `requested_user_id` if the requesting user
    (`actor_user_id`) is authorized.

    Authorization rules:
        - An admin can view any profile.
        - A non-admin user can only view their own profile.

    Parameters
    ----------
    actor_user_id : int
        ID of the user making the request.
    requested_user_id : int
        ID of the profile to retrieve.

    Returns
    -------
    dict | str
        The requested user's profile data, or the string 'Unauthorized'
        if access is denied.

    Raises
    ------
    KeyError
        If either `actor_user_id` or `requested_user_id` does not exist in the
        USERS/USER_PROFILES dictionaries.
    """
    # Validate that both users exist
    if actor_user_id not in USERS:
        raise KeyError(f"Actor user ID {actor_user_id} does not exist.")
    if requested_user_id not in USER_PROFILES:
        raise KeyError(f"Requested user ID {requested_user_id} does not exist.")

    actor_role = USERS[actor_user_id]["role"]

    # Admins can view any profile
    if actor_role == "admin":
        return USER_PROFILES[requested_user_id]

    # Non-admins can only view their own profile
    if actor_user_id == requested_user_id:
        return USER_PROFILES[requested_user_id]

    # All other cases are unauthorized
    return "Unauthorized"