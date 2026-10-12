# -*- coding: utf-8 -*-
"""
Module providing user role management functionality.

Author: ChatGPT
"""

# --------------------------------------------------------------------------- #
# Imports
# --------------------------------------------------------------------------- #

from typing import Dict

# --------------------------------------------------------------------------- #
# Sample data store (replace with real persistence layer in production)
# --------------------------------------------------------------------------- #

USERS: Dict[int, Dict[str, str]] = {
    # user_id : {"role": <role_name>, "privilege": <level>}
    1: {"role": "Alice", "privilege": "admin"},
    2: {"role": "Bob",   "privilege": "moderator"},
    3: {"role": "Carol", "privilege": "normal"},
}

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def _is_valid_privilege(level: str) -> bool:
    """Check if the privilege level is one of the allowed values."""
    return level in {"normal", "moderator", "admin"}

def _get_user_privilege(user_id: int) -> str | None:
    """Return the privilege level of a user, or None if not found."""
    return USERS.get(user_id, {}).get("privilege")

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def update_user_roles(curr_user_id: int, targ_user_id: int, privilege_change: str) -> bool:
    """
    Update the privilege level of a target user.

    Parameters
    ----------
    curr_user_id : int
        ID of the user attempting to perform the change.
    targ_user_id : int
        ID of the target user whose privileges will be changed.
    privilege_change : str
        The new privilege level to assign.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # 1. Verify that the current user exists
    curr_priv = _get_user_privilege(curr_user_id)
    if curr_priv is None:
        # Current user not found
        return False

    # 2. Authorization check: only admins may change privileges
    if curr_priv != "admin":
        return False

    # 3. Verify that the target user exists
    if targ_user_id not in USERS:
        return False

    # 4. Validate the requested privilege level
    if not _is_valid_privilege(privilege_change):
        return False

    # 5. Prevent demoting an admin to a lower level if they are the only admin
    #    (optional safety measure)
    if privilege_change != "admin":
        admin_count = sum(1 for u in USERS.values() if u["privilege"] == "admin")
        # If the target is an admin and we would reduce them below admin,
        # ensure at least one other admin remains.
        if targ_user_id in USERS and USERS[targ_user_id]["privilege"] == "admin":
            if admin_count <= 1:
                return False

    # 6. Perform the update
    USERS[targ_user_id]["privilege"] = privilege_change
    return True

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    print("Before:", USERS[3]["privilege"])
    success = update_user_roles(1, 3, "moderator")
    print("Operation succeeded:", success)
    print("After:", USERS[3]["privilege"])