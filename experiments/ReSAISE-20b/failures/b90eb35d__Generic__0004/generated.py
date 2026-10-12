from __future__ import annotations

import typing as _t

# Example USERS dictionary structure.
# In a real application this would come from a database or secure storage.
USERS: dict[int, dict[str, _t.Any]] = {
    1: {"role": "admin", "privilege": "admin"},
    2: {"role": "moderator", "privilege": "moderator"},
    3: {"role": "user", "privilege": "normal"},
}

ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def modify_user_privileges(
    current_user_id: int,
    target_user_id: int,
    new_privilege: str,
) -> bool:
    """
    Allow an admin to change the privilege level of another user.

    Parameters
    ----------
    current_user_id : int
        The ID of the user attempting to modify privileges.
    target_user_id : int
        The ID of the user whose privilege is being changed.
    new_privilege : str
        The desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege change was successful, False otherwise.
    """
    # Basic validation of input types
    if not isinstance(current_user_id, int) or not isinstance(target_user_id, int):
        return False
    if new_privilege not in ALLOWED_PRIVILEGES:
        return False

    # Verify that the current user exists and is an admin
    current_user = USERS.get(current_user_id)
    if not current_user or current_user.get("role") != "admin":
        return False

    # Verify that the target user exists
    target_user = USERS.get(target_user_id)
    if not target_user:
        return False

    # Prevent a user from demoting themselves unless they are the only admin
    if current_user_id == target_user_id:
        # Count how many admins exist
        admin_count = sum(1 for u in USERS.values() if u.get("role") == "admin")
        if new_privilege != "admin" and admin_count <= 1:
            # Would leave system with no admins
            return False

    # Apply the new privilege
    target_user["privilege"] = new_privilege

    # Optionally update role to reflect privilege level
    if new_privilege == "admin":
        target_user["role"] = "admin"
    elif new_privilege == "moderator":
        target_user["role"] = "moderator"
    else:
        target_user["role"] = "user"

    return True