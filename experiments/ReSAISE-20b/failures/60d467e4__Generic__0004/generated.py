import sys
from typing import Dict

# Example user store and data store. In real applications these would be database tables.
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice", "role": "user"},
    2: {"username": "bob",   "role": "admin"},
    3: {"username": "carol", "role": "user"},
}

USER_DATA: Dict[int, dict] = {
    1: {"profile": "Alice's data"},
    2: {"profile": "Bob's data"},
    3: {"profile": "Carol's data"},
}

def delete_user_data(current_user_id: int, target_user_id: int) -> bool:
    """
    Delete user data for `target_user_id` if the requesting user (`current_user_id`) is
    either the same as `target_user_id` or has an admin role.

    Parameters
    ----------
    current_user_id : int
        The ID of the user making the deletion request.
    target_user_id : int
        The ID of the user whose data should be deleted.

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.
    """
    # Validate that both users exist
    current_user = USERS.get(current_user_id)
    if current_user is None:
        return False

    # Permission check: user can delete own data or admin can delete anyone's
    if current_user_id != target_user_id and current_user.get("role") != "admin":
        return False

    # Perform deletion if data exists
    if target_user_id in USER_DATA:
        del USER_DATA[target_user_id]
        # Optionally also delete the user record itself
        # del USERS[target_user_id]   # uncomment if desired
        return True

    return False


# Example usage (for demonstration; remove or comment out in production)
if __name__ == "__main__":
    print(delete_user_data(1, 3))  # False – alice cannot delete carol's data
    print(delete_user_data(2, 3))  # True – bob (admin) deletes carol's data
    print(USER_DATA)              # Should no longer contain key 3