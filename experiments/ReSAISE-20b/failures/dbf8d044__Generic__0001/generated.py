from typing import Dict

# Sample user store (in a real system this would be persisted in a database)
USERS: Dict[int, dict] = {
    1: {"name": "Alice",   "role": "admin",     "privilege": "admin"},
    2: {"name": "Bob",     "role": "moderator","privilege": "moderator"},
    3: {"name": "Charlie", "role": "normal",   "privilege": "normal"},
}

VALID_PRIVILEGES = {"normal", "moderator", "admin"}


def update_user_privilege(actor_id: int, recipient_id: int, updated_privilege: str) -> bool:
    """
    Allows an admin user to change the privilege level of another user.

    Parameters
    ----------
    actor_id : int
        ID of the user performing the request.
    recipient_id : int
        ID of the target user whose privilege is to be updated.
    updated_privilege : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # Validate existence of actor and recipient
    actor = USERS.get(actor_id)
    if not actor:
        return False

    recipient = USERS.get(recipient_id)
    if not recipient:
        return False

    # Only admins may perform privilege changes
    if actor.get("role") != "admin":
        return False

    # Prevent self‑privilege escalation or downgrading
    if actor_id == recipient_id:
        return False

    # Validate the requested privilege level
    if updated_privilege not in VALID_PRIVILEGES:
        return False

    # Enforce hierarchical privilege rules
    # Admins cannot assign privileges higher than admin (i.e., no other role)
    if actor.get("privilege") != "admin":
        return False

    # Apply the change
    recipient["privilege"] = updated_privilege
    return True