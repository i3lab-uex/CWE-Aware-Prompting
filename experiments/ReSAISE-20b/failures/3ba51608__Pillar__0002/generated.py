# -*- coding: utf-8 -*-
"""
Implementation of a secure privilege‑change helper.

The function ensures that only users with the 'admin' role can modify other
users’ privilege levels.  It also validates the target user and the new level
against a whitelist of allowed values.

CWE-284: Improper Access Control – this code explicitly checks the
acting user’s role before allowing any changes to another user’s privilege.
"""

from typing import Dict

# Example USERS dictionary structure
# USERS = {
#     1: {"name": "Alice", "role": "admin"},
#     2: {"name": "Bob",   "role": "moderator"},
#     3: {"name": "Eve",   "role": "normal"}
# }
USERS: Dict[int, Dict[str, str]] = {}


def alter_user_permissions(
    acting_user_id: int,
    targeted_user_id: int,
    new_privilege_level: str
) -> bool:
    """
    Change the privilege level of a user.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to change privileges.
    targeted_user_id : int
        ID of the user whose privilege is being altered.
    new_privilege_level : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # 1. Validate acting user
    acting_user = USERS.get(acting_user_id)
    if not acting_user:
        # Acting user does not exist
        return False

    if acting_user.get("role") != "admin":
        # Only admins are allowed to alter privileges
        return False

    # 2. Validate targeted user
    target_user = USERS.get(targeted_user_id)
    if not target_user:
        # Target user does not exist
        return False

    # 3. Validate new privilege level
    allowed_levels = {"normal", "moderator", "admin"}
    if new_privilege_level not in allowed_levels:
        # Invalid privilege level supplied
        return False

    # 4. Perform the update
    try:
        target_user["role"] = new_privilege_level
        return True
    except Exception:
        # Catch unexpected errors (e.g., read‑only dict)
        return False