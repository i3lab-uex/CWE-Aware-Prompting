# -*- coding: utf-8 -*-
"""
User privilege modification module.

This module defines a single function `modify_user_privileges` that
allows an administrator to change the privilege level of another user.
The function performs a strict authorization check, validates input
values, and updates the global USERS dictionary in place.

CWE-862 (Missing Authorization) is mitigated by ensuring that only
users with the 'admin' privilege can perform this operation.
"""

from typing import Dict

# Example user store. In a real application this would be replaced
# by persistent storage (database, LDAP, etc.).
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice", "role": "admin"},
    2: {"username": "bob",   "role": "moderator"},
    3: {"username": "carol", "role": "normal"},
}


def modify_user_privileges(current_user_id: int, target_user_id: int, new_privilege: str) -> bool:
    """
    Modify the privilege level of a target user.

    Parameters
    ----------
    current_user_id : int
        The ID of the user attempting to modify privileges.
    target_user_id : int
        The ID of the user whose privileges are being modified.
    new_privilege : str
        The desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was successfully modified, False otherwise.
    """
    # --- Authorization ----------------------------------------------------
    current_user = USERS.get(current_user_id)
    if not current_user:
        # Current user does not exist
        return False

    if current_user.get("role") != "admin":
        # Only admins are allowed to change privileges
        return False

    # --- Validation --------------------------------------------------------
    if target_user_id not in USERS:
        # Target user does not exist
        return False

    if new_privilege not in {"normal", "moderator", "admin"}:
        # Invalid privilege level
        return False

    # Prevent an admin from demoting themselves to a non-admin role.
    if current_user_id == target_user_id and new_privilege != "admin":
        return False

    # --- Update ------------------------------------------------------------
    USERS[target_user_id]["role"] = new_privilege
    return True


# Example usage (for demonstration only; remove or comment out in production)
if __name__ == "__main__":
    print("Before:", USERS[2]["role"])
    success = modify_user_privileges(1, 2, "admin")
    print("Success:", success)
    print("After:", USERS[2]["role"])