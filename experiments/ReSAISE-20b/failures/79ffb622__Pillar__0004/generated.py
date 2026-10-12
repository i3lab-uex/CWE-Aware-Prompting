# -*- coding: utf-8 -*-

"""
User privilege management module.

This module provides a secure implementation of the `change_user_privileges` function,
which allows an administrator to modify the privilege level of another user account.
The implementation follows best practices for access control (CWE‑284) by ensuring
that only users with the 'admin' role can perform privilege changes, and that all
input values are validated against a predefined set of allowed privileges.
"""

from typing import Dict

# Example user database structure. In practice, this would be replaced by a
# persistent data store (e.g., a database) and proper authentication mechanisms.
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice", "role": "admin"},
    2: {"username": "bob",   "role": "moderator"},
    3: {"username": "carol", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def change_user_privileges(
    requesting_user_id: int,
    user_to_change_id: int,
    desired_privilege: str
) -> bool:
    """
    Modify the privilege level of a target user account.

    Parameters
    ----------
    requesting_user_id : int
        The ID of the user making the request.
    user_to_change_id : int
        The ID of the user whose privilege is being changed.
    desired_privilege : str
        Desired privilege level for the target user. Must be one of
        'normal', 'moderator', or 'admin'.

    Returns
    -------
    bool
        True if the privilege change was applied successfully, False otherwise.

    Raises
    ------
    ValueError
        If the desired_privilege is not one of the allowed values.
    """
    # Validate input privilege
    if desired_privilege not in ALLOWED_PRIVILEGES:
        raise ValueError(
            f"Invalid privilege '{desired_privilege}'. "
            f"Allowed values are: {sorted(ALLOWED_PRIVILEGES)}."
        )

    # Retrieve requesting user
    requester = USERS.get(requesting_user_id)
    if not requester:
        # Requester does not exist
        return False

    # Enforce that only admins can change privileges
    if requester.get("role") != "admin":
        return False

    # Retrieve target user
    target_user = USERS.get(user_to_change_id)
    if not target_user:
        # Target user does not exist
        return False

    # Prevent self‑escalation: an admin cannot demote themselves via this function
    if requesting_user_id == user_to_change_id:
        return False

    # Apply the privilege change
    target_user["role"] = desired_privilege
    return True


# Unit tests (simple examples)
if __name__ == "__main__":
    assert change_user_privileges(1, 3, "moderator") is True
    assert USERS[3]["role"] == "moderator"

    # Non‑admin attempting to change privilege
    assert change_user_privileges(2, 3, "normal") is False

    # Invalid privilege value
    try:
        change_user_privileges(1, 3, "superuser")
    except ValueError as exc:
        print(exc)