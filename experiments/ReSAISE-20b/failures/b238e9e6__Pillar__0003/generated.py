# -*- coding: utf-8 -*-
"""
User privilege update module.

This module provides the `update_privileges` function, which allows an
administrator to change another user's role in the system.
The implementation guards against improper access control by ensuring
that only users with the 'admin' role can perform this operation.
"""

import logging

# Configure basic logger for audit purposes
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(module)s] %(message)s",
)

# Example in-memory user store.
# In a real application this would be replaced with database access.
USERS = {
    1: {"username": "alice", "role": "admin"},
    2: {"username": "bob",   "role": "moderator"},
    3: {"username": "carol", "role": "normal"},
}

# Allowed roles
ALLOWED_ROLES = {"normal", "moderator", "admin"}


def update_privileges(acting_user_id: int, affected_user_id: int, new_role: str) -> bool:
    """
    Update the role of a user in the system.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to change privileges.
    affected_user_id : int
        ID of the user whose privilege is being altered.
    new_role : str
        New role to assign. Must be one of 'normal', 'moderator', or 'admin'.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.

    Raises
    ------
    ValueError
        If `new_role` is not a recognized role.
    """
    # Validate new role
    if new_role not in ALLOWED_ROLES:
        raise ValueError(f"Invalid role '{new_role}'. Must be one of {ALLOWED_ROLES}")

    # Check existence of acting user
    acting_user = USERS.get(acting_user_id)
    if not acting_user:
        logging.warning("Attempt to modify privileges by non-existent user ID %s", acting_user_id)
        return False

    # Enforce access control: only admins can modify roles
    if acting_user["role"] != "admin":
        logging.warning(
            "User ID %s (%s) attempted to modify privileges without admin rights.",
            acting_user_id,
            acting_user["role"],
        )
        return False

    # Check existence of affected user
    affected_user = USERS.get(affected_user_id)
    if not affected_user:
        logging.warning("Attempt to modify privileges for non-existent user ID %s", affected_user_id)
        return False

    # Perform the role update
    old_role = affected_user["role"]
    affected_user["role"] = new_role

    logging.info(
        "User ID %s (%s) changed role of user ID %s from '%s' to '%s'.",
        acting_user_id,
        acting_user["role"],
        affected_user_id,
        old_role,
        new_role,
    )
    return True