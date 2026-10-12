from __future__ import annotations

# Sample data structures. In real usage these would be populated from a database or config.
USER_PROFILES = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Eve",   "email": "eve@example.com"},
}

USERS = {
    1: {"role": "admin"},   # Alice is an admin
    2: {"role": "user"},
    3: {"role": "user"},
}


def view_user_profile(current_user_id: int, target_user_id: int) -> dict | str:
    """
    Return the profile of *target_user_id* if the requester is authorized.

    Authorization rules:
        - The user can view their own profile.
        - An admin (role == 'admin') can view any profile.

    Parameters
    ----------
    current_user_id : int
        The ID of the user making the request.
    target_user_id : int
        The ID of the profile to retrieve.

    Returns
    -------
    dict | str
        The target user's profile data if authorized, otherwise the string
        'Unauthorized'.

    Notes
    -----
    - If either user ID does not exist in the system, the function returns
      'Unauthorized'.  This prevents leaking information about existing users.
    """
    # Basic existence checks – return 'Unauthorized' to avoid revealing
    # whether a user ID exists.
    if current_user_id not in USERS or target_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Retrieve roles
    current_role = USERS[current_user_id].get("role", "user")

    # Allow if same user or admin
    if current_user_id == target_user_id or current_role == "admin":
        return USER_PROFILES[target_user_id]

    # Otherwise deny access
    return "Unauthorized"