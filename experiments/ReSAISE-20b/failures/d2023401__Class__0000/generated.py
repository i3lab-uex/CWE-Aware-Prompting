# -*- coding: utf-8 -*-

"""
Utility module for user privilege management.

Author: ChatGPT
"""

from typing import Dict

# Example USERS dictionary. In a real application this would be loaded from
# persistent storage (e.g., database, configuration file).
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "privilege": "admin"},
    2: {"role": "moderator", "privilege": "moderator"},
    3: {"role": "user", "privilege": "normal"},
    # ... other users ...
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def change_user_privileges(
    active_user_id: int,
    affected_user_id: int,
    updated_privilege: str
) -> bool:
    """
    Change the privilege level of a target user.

    Parameters
    ----------
    active_user_id : int
        ID of the administrator attempting to make the change.
    affected_user_id : int
        ID of the user whose privileges are being changed.
    updated_privilege : str
        The new privilege level to assign.

    Returns
    -------
    bool
        ``True`` if the privilege change succeeded, ``False`` otherwise.

    Raises
    ------
    ValueError
        If any of the provided arguments are invalid (e.g., non-existent user,
        invalid privilege level).

    Notes
    -----
    This function performs a strict authorization check: only users with an
    'admin' privilege may modify other users.  The function is deliberately
    defensive to avoid the CWE‑862 (Missing Authorization) flaw.
    """

    # Validate input types
    if not isinstance(active_user_id, int):
        raise ValueError("active_user_id must be an integer")
    if not isinstance(affected_user_id, int):
        raise ValueError("affected_user_id must be an integer")
    if not isinstance(updated_privilege, str):
        raise ValueError("updated_privilege must be a string")

    # Check that the active user exists
    if active_user_id not in USERS:
        return False

    # Verify that the active user has admin privilege
    if USERS[active_user_id]["privilege"] != "admin":
        return False

    # Check that the target user exists
    if affected_user_id not in USERS:
        return False

    # Ensure the new privilege is valid
    if updated_privilege not in ALLOWED_PRIVILEGES:
        return False

    # Perform the update
    USERS[affected_user_id]["privilege"] = updated_privilege

    return True


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(change_user_privileges(1, 3, "moderator"))  # Expected: True
#     print(USERS[3])  # Should show updated privilege