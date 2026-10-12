from __future__ import annotations

# Sample USERS dictionary for context.
# In a real system this would be fetched from a database or secure store.
USERS: dict[int, dict[str, str]] = {
    1: {"name": "Alice",   "privilege": "admin"},
    2: {"name": "Bob",     "privilege": "moderator"},
    3: {"name": "Charlie", "privilege": "normal"},
    # ... additional users
}

VALID_PRIVILEGES = {"normal", "moderator", "admin"}


def change_user_privileges(
    active_user_id: int,
    affected_user_id: int,
    updated_privilege: str
) -> bool:
    """
    Change the privilege level of a user account.

    Parameters
    ----------
    active_user_id : int
        ID of the administrator attempting the change.
    affected_user_id : int
        ID of the user whose privilege is to be modified.
    updated_privilege : str
        Desired new privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was successfully updated; False otherwise.
    """
    # Ensure both users exist
    active_user = USERS.get(active_user_id)
    affected_user = USERS.get(affected_user_id)

    if not active_user or not affected_user:
        return False

    # Only an admin can change privileges
    if active_user.get("privilege") != "admin":
        return False

    # Validate the requested privilege level
    if updated_privilege not in VALID_PRIVILEGES:
        return False

    # Perform the update
    try:
        affected_user["privilege"] = updated_privilege
        return True
    except Exception:
        # Log exception in real application
        return False