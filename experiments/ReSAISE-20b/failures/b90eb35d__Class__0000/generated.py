from typing import Dict

# Sample USERS dictionary; in a real system this would be loaded from a database
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin",     "privilege": "admin"},
    2: {"username": "bob",     "role": "moderator","privilege": "moderator"},
    3: {"username": "charlie", "role": "normal",   "privilege": "normal"},
    # ... more users ...
}

ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def modify_user_privileges(
    current_user_id: int,
    target_user_id: int,
    new_privilege: str
) -> bool:
    """
    Modify the privilege level of a target user.

    Args:
        current_user_id: ID of the actor attempting to modify privileges.
        target_user_id:  ID of the user whose privileges are being modified.
        new_privilege:   Desired privilege level ('normal', 'moderator', or 'admin').

    Returns:
        True if the privilege was successfully modified, otherwise False.
    """
    # 1. Validate that both users exist
    current_user = USERS.get(current_user_id)
    target_user = USERS.get(target_user_id)

    if current_user is None or target_user is None:
        return False

    # 2. Authorization check: only admins may modify privileges
    if current_user.get("role") != "admin":
        return False

    # 3. Prevent self-modification of admin privileges
    if current_user_id == target_user_id and new_privilege != "admin":
        return False

    # 4. Validate the requested privilege level
    if new_privilege not in ALLOWED_PRIVILEGES:
        return False

    # 5. Apply the change
    target_user["privilege"] = new_privilege
    # Optionally update the role to match privilege (if desired)
    target_user["role"] = new_privilege

    return True