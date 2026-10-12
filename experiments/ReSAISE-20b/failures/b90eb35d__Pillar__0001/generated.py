# -*- coding: utf-8 -*-
"""
User privilege modification module.

This module provides a single function, `modify_user_privileges`, which
allows an administrator to change the privilege level of another user.
The function implements strict access control checks (CWE-284) to
prevent unauthorized privilege escalation.

USERS: A global dictionary mapping user_id (int) -> dict with keys:
    - "role": str   # e.g., "user", "moderator", "admin"
    - "privilege": str  # one of "normal", "moderator", "admin"

Example USERS structure:
    {
        1: {"role": "admin",      "privilege": "admin"},
        2: {"role": "moderator",  "privilege": "moderator"},
        3: {"role": "user",       "privilege": "normal"},
    }
"""

from typing import Dict

# Example USERS dictionary; replace with real data source in production
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin",      "privilege": "admin"},
    2: {"role": "moderator",  "privilege": "moderator"},
    3: {"role": "user",       "privilege": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def modify_user_privileges(current_user_id: int,
                           target_user_id: int,
                           new_privilege: str) -> bool:
    """
    Modify the privilege level of a target user.

    Parameters
    ----------
    current_user_id : int
        ID of the actor attempting the modification.
    target_user_id : int
        ID of the user whose privilege is to be changed.
    new_privilege : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was successfully updated, False otherwise.

    Notes
    -----
    - Only users with role 'admin' may modify privileges.
    - The target user must exist in USERS.
    - The new privilege must be one of the allowed values.
    - Admins cannot demote themselves to a lower privilege level.
    """
    # Validate presence of actors in USERS
    current_user = USERS.get(current_user_id)
    target_user = USERS.get(target_user_id)

    if current_user is None:
        # Current user does not exist; deny action
        return False

    if target_user is None:
        # Target user does not exist; deny action
        return False

    # Only admins may modify privileges
    if current_user.get("role") != "admin":
        return False

    # Ensure new privilege is valid
    if new_privilege not in ALLOWED_PRIVILEGES:
        return False

    # Prevent admin from lowering their own privilege
    if current_user_id == target_user_id and new_privilege != "admin":
        return False

    # Perform the update
    target_user["privilege"] = new_privilege

    # Optionally, keep role in sync with privilege for consistency
    target_user["role"] = new_privilege

    return True


# Example usage (for testing purposes only; remove or guard in production)
if __name__ == "__main__":
    print(modify_user_privileges(1, 3, "moderator"))  # Expected: True
    print(USERS[3])                                   # Updated user data