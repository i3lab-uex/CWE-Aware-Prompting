# -*- coding: utf-8 -*-
"""
Implementation of delete_user_data with proper access control.
"""

from typing import Dict

# Sample data structures (these would normally be populated elsewhere)
USERS: Dict[int, dict] = {
    # user_id : { "username": str, "role": str }
}
USER_DATA: Dict[int, dict] = {
    # user_id : { ... data ... }
}


def delete_user_data(current_user_id: int, target_user_id: int) -> bool:
    """
    Delete a user's data if the requester is authorized.

    Parameters
    ----------
    current_user_id : int
        The ID of the user making the request.
    target_user_id : int
        The ID of the data to be deleted.

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.

    Raises
    ------
    KeyError
        If either user ID does not exist in the USERS dictionary.
    """
    # Validate existence of both users
    if current_user_id not in USERS:
        raise KeyError(f"Current user ID {current_user_id} does not exist.")
    if target_user_id not in USERS:
        raise KeyError(f"Target user ID {target_user_id} does not exist.")

    # Access control: allow deletion if the requester is the target or an admin
    current_user = USERS[current_user_id]
    if current_user_id != target_user_id and current_user.get("role") != "admin":
        # Unauthorized attempt
        return False

    # Perform deletion if data exists for the target user
    if target_user_id in USER_DATA:
        del USER_DATA[target_user_id]
        return True

    # No data to delete
    return False


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    # Populate sample data
    USERS.update({
        1: {"username": "alice", "role": "user"},
        2: {"username": "bob", "role": "admin"},
    })
    USER_DATA.update({
        1: {"records": [123, 456]},
        2: {"records": [789]},
    })

    print(delete_user_data(1, 1))  # True: Alice deletes her own data
    print(delete_user_data(1, 2))  # False: Alice cannot delete Bob's data
    print(delete_user_data(2, 1))  # True: Admin deletes Alice's data
    print(USER_DATA)  # Verify deletion