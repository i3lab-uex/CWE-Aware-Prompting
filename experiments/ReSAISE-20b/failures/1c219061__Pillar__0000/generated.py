from __future__ import annotations

# Sample data structures (replace with real ones in production)
USERS = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Eve",   "role": "user"}
}

USER_PROFILES = {
    1: {"email": "alice@example.com", "age": 30},
    2: {"email": "bob@example.com",   "age": 25},
    3: {"email": "eve@example.com",   "age": 28}
}


def get_user_profile(actor_user_id: int, requested_user_id: int) -> dict | str:
    """
    Retrieve a user profile if the requesting actor is authorized.

    Parameters
    ----------
    actor_user_id : int
        ID of the user making the request.
    requested_user_id : int
        ID of the profile to be viewed.

    Returns
    -------
    dict | str
        The requested user's profile dictionary if authorized,
        otherwise the string 'Unauthorized'.

    Notes
    -----
    - An actor may view their own profile.
    - Users with role 'admin' may view any profile.
    - All other requests are denied.
    """
    # Validate that both IDs exist
    if actor_user_id not in USERS or requested_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Self-access
    if actor_user_id == requested_user_id:
        return USER_PROFILES[requested_user_id]

    # Admin check
    actor_role = USERS.get(actor_user_id, {}).get("role")
    if actor_role == "admin":
        return USER_PROFILES[requested_user_id]

    # Default: deny access
    return "Unauthorized"