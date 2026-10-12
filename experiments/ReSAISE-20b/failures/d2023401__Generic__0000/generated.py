# -*- coding: utf-8 -*-
"""
User privilege management module.

This module provides a single function `change_user_privileges` that
allows an administrator to modify the privilege level of another user.
"""

from typing import Dict

# Example USERS dictionary. In a real application this would be loaded
# from persistent storage or an authentication backend.
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice", "role": "admin"},
    2: {"username": "bob",   "role": "moderator"},
    3: {"username": "carol", "role": "normal"},
}

# Valid privilege levels
_VALID_PRIVILEGES = {"normal", "moderator", "admin"}


def change_user_privileges(
    active_user_id: int,
    affected_user_id: int,
    updated_privilege: str
) -> bool:
    """
    Change the privilege level of a user account.

    Parameters
    ----------
    active_user_id : int
        The ID of the user attempting to perform the change.
    affected_user_id : int
        The ID of the user whose privileges are to be updated.
    updated_privilege : str
        The new privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        ``True`` if the privilege was updated successfully, otherwise ``False``.

    Notes
    -----
    * Only users with the 'admin' role can modify other users.
    * The function silently returns ``False`` if any validation fails
      (e.g., non‑existent user IDs, invalid privilege string,
      or insufficient permissions).
    """
    # Basic validation
    if not isinstance(active_user_id, int) or not isinstance(affected_user_id, int):
        return False

    if updated_privilege not in _VALID_PRIVILEGES:
        return False

    active_user = USERS.get(active_user_id)
    affected_user = USERS.get(affected_user_id)

    # Ensure both users exist
    if active_user is None or affected_user is None:
        return False

    # Only admins can change privileges
    if active_user.get("role") != "admin":
        return False

    # Prevent admins from demoting themselves to a lower role
    if active_user_id == affected_user_id and updated_privilege != "admin":
        return False

    # Perform the update
    try:
        affected_user["role"] = updated_privilege
        return True
    except Exception:
        # In case the USERS dict is immutable or another unforeseen error occurs.
        return False


# Example usage (commented out):
# if change_user_privileges(1, 3, "moderator"):
#     print("Privilege updated.")