# -*- coding: utf-8 -*-

"""
User permission alteration module.

Provides a single function `alter_user_permissions` that allows an
administrator to change the privilege level of another user.
"""

from typing import Dict

# Example USERS dictionary. In a real application this would be
# retrieved from a database or an external service.
USERS: Dict[int, dict] = {
    1: {"name": "Alice",   "role": "admin"},
    2: {"name": "Bob",     "role": "moderator"},
    3: {"name": "Charlie", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def alter_user_permissions(
    acting_user_id: int,
    targeted_user_id: int,
    new_privilege_level: str
) -> bool:
    """
    Modify the privilege level of a user.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user attempting to change privileges.
    targeted_user_id : int
        The ID of the user whose privilege is being altered.
    new_privilege_level : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        ``True`` if the operation succeeded, otherwise ``False``.

    Raises
    ------
    ValueError
        If `new_privilege_level` is not a recognized privilege level.
    """
    # Validate new privilege
    if new_privilege_level not in ALLOWED_PRIVILEGES:
        raise ValueError(
            f"Invalid privilege level: {new_privilege_level!r}. "
            f"Allowed values are {sorted(ALLOWED_PRIVILEGES)}."
        )

    # Ensure both users exist
    acting_user = USERS.get(acting_user_id)
    targeted_user = USERS.get(targeted_user_id)

    if acting_user is None or targeted_user is None:
        return False

    # Only admins can modify privileges
    if acting_user.get("role") != "admin":
        return False

    # Prevent self‑privilege escalation
    if acting_user_id == targeted_user_id:
        return False

    # Apply the new privilege
    targeted_user["role"] = new_privilege_level
    return True