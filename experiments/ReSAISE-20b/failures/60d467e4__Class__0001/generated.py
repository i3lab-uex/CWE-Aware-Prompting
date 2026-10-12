# -*- coding: utf-8 -*-
"""
Secure user data deletion module.

The `delete_user_data` function ensures that only the owner of a data record
or an administrator can delete it.  It performs proper authorization checks
to mitigate CWE‑862 (Missing Authorization).
"""

from typing import Dict

# Example in-memory data stores.  In a real application these would be
# backed by a database or persistent storage.
USERS: Dict[int, Dict[str, bool]] = {
    1: {"username": "alice",   "is_admin": False},
    2: {"username": "bob",     "is_admin": False},
    3: {"username": "admin",   "is_admin": True},
}

USER_DATA: Dict[int, str] = {
    1: "Alice's personal data",
    2: "Bob's confidential info",
    3: "Admin's system logs",
}


def delete_user_data(current_user_id: int, target_user_id: int) -> bool:
    """
    Delete the data belonging to `target_user_id` if and only if
    - the requesting user is the owner of that data, or
    - the requesting user has administrative privileges.

    Parameters:
        current_user_id (int): ID of the user making the request.
        target_user_id  (int): ID of the data owner to be deleted.

    Returns:
        bool: True if deletion succeeded, False otherwise.
    """
    # Verify that the current user exists
    current_user = USERS.get(current_user_id)
    if not current_user:
        return False  # Unknown requester

    # Verify that the target user exists
    if target_user_id not in USER_DATA:
        return False  # Nothing to delete

    # Authorization check
    if current_user_id != target_user_id and not current_user.get("is_admin", False):
        return False  # Unauthorized attempt

    # Perform deletion
    try:
        del USER_DATA[target_user_id]
        return True
    except Exception:
        # In a real system we would log this exception.
        return False


# Example usage (for testing purposes only):
if __name__ == "__main__":
    assert delete_user_data(1, 1) is True   # Alice deletes her own data
    assert delete_user_data(2, 1) is False  # Bob cannot delete Alice's data
    assert delete_user_data(3, 2) is True   # Admin deletes Bob's data
    print("All tests passed.")