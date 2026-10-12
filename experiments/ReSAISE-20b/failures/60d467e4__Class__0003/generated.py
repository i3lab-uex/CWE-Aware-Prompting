# -*- coding: utf-8 -*-
"""
Utility for deleting user data with proper authorization checks.
"""

from typing import Dict

# Sample data structures (to be replaced with actual application data)
USERS: Dict[int, dict] = {
    # user_id : { 'username': str, 'role': str ('admin' or 'user') }
}

USER_DATA: Dict[int, dict] = {
    # user_id : { ... arbitrary user data ... }
}


def delete_user_data(current_user_id: int, target_user_id: int) -> bool:
    """
    Delete the data belonging to `target_user_id` if the requesting user
    (`current_user_id`) is either the same as the target or has an admin role.

    Parameters
    ----------
    current_user_id : int
        ID of the user making the deletion request.
    target_user_id : int
        ID of the user whose data is to be deleted.

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise (e.g., not authorized,
        user or data does not exist).
    """
    # Basic sanity checks
    if current_user_id is None or target_user_id is None:
        return False

    # Ensure both users exist in the USERS dict
    current_user = USERS.get(current_user_id)
    target_user = USERS.get(target_user_id)

    if current_user is None or target_user is None:
        # Either the requester or the target does not exist
        return False

    # Authorization: user can delete own data; admin can delete any
    if current_user_id != target_user_id and current_user.get('role') != 'admin':
        # Unauthorized attempt
        return False

    # Check if target data exists before attempting deletion
    if target_user_id not in USER_DATA:
        return False

    # Perform the deletion
    try:
        del USER_DATA[target_user_id]
        return True
    except Exception:
        # In a real-world scenario we might log this exception.
        return False