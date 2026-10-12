# -*- coding: utf-8 -*-
"""
User privilege update module.

The `update_privileges` function performs an authorization check
to ensure that only administrators can modify other users' roles.
It validates the new role against an allowed set and updates
the global USERS dictionary safely.

CWE-862 (Missing Authorization) is mitigated by verifying the
acting user's role before any modification occurs.
"""

from typing import Dict

# Example USERS dictionary structure.
# In a real application this would come from a database or secure store.
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
}

# Allowed roles
ALLOWED_ROLES = {"normal", "moderator", "admin"}


def update_privileges(acting_user_id: int, affected_user_id: int, new_role: str) -> bool:
    """
    Update the role of a user.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to change privileges.
    affected_user_id : int
        ID of the target user whose role will be updated.
    new_role : str
        Desired new role ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # Basic input validation
    if not isinstance(acting_user_id, int) or not isinstance(affected_user_id, int):
        return False

    if new_role not in ALLOWED_ROLES:
        return False

    # Ensure both users exist
    acting_user = USERS.get(acting_user_id)
    affected_user = USERS.get(affected_user_id)

    if acting_user is None or affected_user is None:
        return False

    # Authorization check: only admins can modify roles
    if acting_user.get("role") != "admin":
        return False

    # Optional: prevent admins from demoting themselves
    if acting_user_id == affected_user_id and new_role != "admin":
        return False

    # Perform the update
    try:
        affected_user["role"] = new_role
        return True
    except Exception:
        # Log exception in real-world scenario; here we simply fail gracefully.
        return False