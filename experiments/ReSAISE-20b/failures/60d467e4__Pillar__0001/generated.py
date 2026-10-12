# -*- coding: utf-8 -*-
"""
User data deletion module.

This module provides a single function `delete_user_data` that deletes
user-specific data from the in-memory store `USER_DATA`.  The function
ensures that only the target user themselves or an administrator can
perform the deletion, preventing CWE‑284 (Improper Access Control).
"""

from typing import Dict

# Sample data structures. In a real application these would be
# persisted in a database or external storage.
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice", "role": "user"},
    2: {"username": "bob",   "role": "admin"},
    3: {"username": "carol", "role": "user"},
}

USER_DATA: Dict[int, str] = {
    1: "Alice's personal data",
    2: "Bob's administrative logs",
    3: "Carol's confidential info",
}


def delete_user_data(current_user_id: int, target_user_id: int) -> bool:
    """
    Delete the data associated with `target_user_id`.

    Only the user themselves or an administrator can delete the data.
    Returns True if deletion succeeded, False otherwise.

    Parameters
    ----------
    current_user_id : int
        ID of the user making the deletion request.
    target_user_id : int
        ID of the user whose data is to be deleted.

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.
    """
    # Validate that both users exist in the system
    current_user = USERS.get(current_user_id)
    target_user = USERS.get(target_user_id)

    if current_user is None or target_user is None:
        # Either the requester or the target does not exist
        return False

    # Check permissions: self-deletion or admin privilege
    is_admin = current_user.get("role") == "admin"
    if not (current_user_id == target_user_id or is_admin):
        # Not authorized to delete this data
        return False

    # Perform the deletion if the target has data
    try:
        USER_DATA.pop(target_user_id)
        return True
    except KeyError:
        # No data to delete; treat as successful (idempotent)
        return True