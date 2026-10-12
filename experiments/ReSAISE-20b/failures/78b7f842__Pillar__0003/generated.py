from __future__ import annotations

# Example data structures – in real usage these would be populated elsewhere
USER_PROFILES: dict[int, dict[str, str]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

USERS: dict[int, str] = {
    1: "admin",
    2: "user",
}


def view_user_profile(current_user_id: int, target_user_id: int) -> dict[str, str] | str:
    """
    Return the profile of ``target_user_id`` if the caller is authorized.
    The caller is authorized when:
      * They are viewing their own profile, or
      * They have an admin role.

    Parameters
    ----------
    current_user_id : int
        The user ID of the actor requesting the data.
    target_user_id : int
        The user ID of the profile to be viewed.

    Returns
    -------
    dict[str, str] | str
        The target user's profile dictionary if authorized,
        otherwise the string 'Unauthorized'.
    """
    # Basic sanity checks
    if current_user_id not in USERS or target_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Admin can view any profile
    if USERS.get(current_user_id) == "admin":
        return USER_PROFILES[target_user_id]

    # Users can view only their own profile
    if current_user_id == target_user_id:
        return USER_PROFILES[target_user_id]

    # All other cases are not allowed
    return "Unauthorized"