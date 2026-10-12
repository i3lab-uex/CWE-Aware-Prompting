# -*- coding: utf-8 -*-
"""
Module providing user data deletion functionality with proper access control.
"""

from typing import Dict, Any

# Example in‑memory data stores (replace with real persistence layer as needed)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"username": "alice",   "is_admin": False},
    2: {"username": "bob",     "is_admin": True},   # admin user
    3: {"username": "charlie", "is_admin": False},
}

USER_DATA: Dict[int, Any] = {
    1: {"profile": "Alice's data"},
    2: {"profile": "Bob's data"},
    3: {"profile": "Charlie's data"},
}


def delete_user_data(current_user_id: int, target_user_id: int) -> bool:
    """
    Delete a user's data if the requester is either the user themselves or an admin.

    Parameters
    ----------
    current_user_id : int
        ID of the user making the deletion request.
    target_user_id : int
        ID of the user whose data should be deleted.

    Returns
    -------
    bool
        ``True`` if deletion succeeded, ``False`` otherwise.

    Raises
    ------
    ValueError
        If either user ID is not present in the USERS database.
    """
    # Verify that both users exist
    if current_user_id not in USERS:
        raise ValueError(f"Requester user ID {current_user_id} does not exist.")
    if target_user_id not in USERS:
        raise ValueError(f"Target user ID {target_user_id} does not exist.")

    # Access control: only the target or an admin may delete data
    if current_user_id != target_user_id and not USERS[current_user_id].get("is_admin", False):
        # Unauthorized attempt
        return False

    # Perform deletion if data exists for the target user
    if target_user_id in USER_DATA:
        del USER_DATA[target_user_id]
        return True

    # No data to delete
    return False


# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     print(delete_user_data(1, 1))   # True – user deletes own data
#     print(delete_user_data(2, 3))   # True – admin deletes another user's data
#     print(delete_user_data(1, 3))   # False – unauthorized attempt