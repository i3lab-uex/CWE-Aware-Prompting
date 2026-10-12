# -*- coding: utf-8 -*-
"""
User privilege modification module.

This module implements a secure function to change the privilege level of
a user account.  It performs strict checks against improper access
control (CWE‑284) by ensuring that only an account with the 'admin'
role may alter privileges and that the target privilege is valid.
"""

from typing import Dict

# Example USERS dictionary. In a real application this would come from
# a database or secure persistence layer.
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
}

# Allowed privilege values
_ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def modify_user_privileges(
    current_user_id: int,
    target_user_id: int,
    new_privilege: str
) -> bool:
    """
    Modify the privilege level of a target user account.

    Parameters
    ----------
    current_user_id : int
        ID of the actor attempting to modify privileges.
    target_user_id : int
        ID of the user whose privileges are being modified.
    new_privilege : str
        New privilege level to assign ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was successfully modified, False otherwise.
    """
    # Quick sanity checks
    if new_privilege not in _ALLOWED_PRIVILEGES:
        return False

    # Ensure both users exist
    current_user = USERS.get(current_user_id)
    target_user = USERS.get(target_user_id)

    if current_user is None or target_user is None:
        return False

    # Only an admin can modify privileges
    if current_user.get("role") != "admin":
        return False

    # Prevent self‑promotion or demotion of the admin account
    if current_user_id == target_user_id:
        return False

    # Apply the new privilege
    target_user["role"] = new_privilege
    return True


# Example usage (for demonstration only; remove or guard with if __name__ == "__main__": in real code)
if __name__ == "__main__":
    # Successful modification
    print(modify_user_privileges(1, 2, "admin"))   # True

    # Unauthorized attempt
    print(modify_user_privileges(2, 3, "moderator"))  # False

    # Invalid privilege level
    print(modify_user_privileges(1, 3, "superuser"))   # False