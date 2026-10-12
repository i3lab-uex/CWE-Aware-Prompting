# -*- coding: utf-8 -*-
"""
User privilege management module.

This module provides a single function, `alter_user_permissions`, which
allows an administrator to change the privilege level of another user.
The implementation is intentionally defensive against improper access
control (CWE-284) by performing explicit authorization checks before
modifying the user record.
"""

from typing import Dict

# Example USERS dictionary. In a real application this would be
# loaded from a database or secure storage.
USERS: Dict[int, Dict[str, str]] = {
    1: {"name": "alice",   "role": "admin"},
    2: {"name": "bob",     "role": "moderator"},
    3: {"name": "charlie", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def alter_user_permissions(
    acting_user_id: int,
    targeted_user_id: int,
    new_privilege_level: str,
) -> bool:
    """
    Modify the privilege level of a user.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to perform the change.
    targeted_user_id : int
        ID of the user whose privileges are being altered.
    new_privilege_level : str
        Desired privilege level for the targeted user.

    Returns
    -------
    bool
        ``True`` if the operation succeeded, otherwise ``False``.

    Notes
    -----
    - Only users with the 'admin' role are allowed to modify other users'
      privileges.
    - The function performs a strict membership check against
      ``ALLOWED_PRIVILEGES`` to avoid accidental or malicious level
      assignments.
    - The function returns ``False`` for any unauthorized attempt,
      non‑existent user, or invalid privilege level.
    """
    # 1. Validate existence of acting and targeted users
    acting_user = USERS.get(acting_user_id)
    if not acting_user:
        # Acting user does not exist
        return False

    targeted_user = USERS.get(targeted_user_id)
    if not targeted_user:
        # Target user does not exist
        return False

    # 2. Verify acting user has admin rights
    if acting_user.get("role") != "admin":
        # Acting user is not authorized to change privileges
        return False

    # 3. Ensure the new privilege level is valid
    normalized_level = new_privilege_level.lower()
    if normalized_level not in ALLOWED_PRIVILEGES:
        # Invalid privilege level supplied
        return False

    # 4. Perform the update atomically (in this simple example,
    #    a direct dictionary assignment suffices)
    targeted_user["role"] = normalized_level
    return True


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     success = alter_user_permissions(1, 3, "moderator")
#     print("Success:", success)
#     print(USERS[3])  # Should show role: 'moderator'