import re

# Example USERS dictionary structure.
USERS = {
    1: {"name": "Alice",   "role": "admin",     "privilege": "admin"},
    2: {"name": "Bob",     "role": "moderator", "privilege": "moderator"},
    3: {"name": "Charlie", "role": "normal",   "privilege": "normal"},
    # ... additional users
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def update_user_privilege(actor_id: int, recipient_id: int, updated_privilege: str) -> bool:
    """
    Allows an admin user to change the privilege level of another user.

    Parameters
    ----------
    actor_id : int
        ID of the user performing the operation.
    recipient_id : int
        ID of the target user whose privilege will be updated.
    updated_privilege : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was updated successfully, False otherwise.
    """

    # Validate input types
    if not isinstance(actor_id, int) or not isinstance(recipient_id, int):
        return False
    if not isinstance(updated_privilege, str):
        return False

    # Ensure the privilege value is valid
    if updated_privilege not in ALLOWED_PRIVILEGES:
        return False

    # Ensure both users exist
    actor = USERS.get(actor_id)
    recipient = USERS.get(recipient_id)

    if not actor or not recipient:
        return False

    # Authorization check: only admins can modify privileges
    if actor.get("role") != "admin":
        return False

    # Prevent self-modification of privilege to avoid accidental lockout
    if actor_id == recipient_id:
        return False

    # Apply the privilege change
    try:
        recipient["privilege"] = updated_privilege
        # Optionally sync role with privilege if needed:
        recipient["role"] = updated_privilege
    except Exception:
        return False

    return True