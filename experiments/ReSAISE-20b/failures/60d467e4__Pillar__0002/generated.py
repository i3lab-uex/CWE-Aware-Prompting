from typing import Dict

# Sample data structures (would normally be defined elsewhere)
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice", "role": "user"},
    2: {"username": "bob",   "role": "admin"},
    3: {"username": "carol", "role": "user"},
}

USER_DATA: Dict[int, dict] = {
    1: {"preferences": {"theme": "dark"}, "history": ["page1", "page2"]},
    3: {"preferences": {"theme": "light"}, "history": ["page3"]},
}


def delete_user_data(current_user_id: int, target_user_id: int) -> bool:
    """
    Delete data belonging to `target_user_id` if the requesting user
    (`current_user_id`) is either an admin or the same user.

    Parameters:
        current_user_id (int): ID of the user making the request.
        target_user_id (int): ID of the data to be deleted.

    Returns:
        bool: True if deletion succeeded, False otherwise.
    """
    # Validate that both users exist
    current_user = USERS.get(current_user_id)
    if not current_user:
        return False  # requesting user does not exist

    # Check permission: admin or self
    if current_user.get("role") != "admin" and current_user_id != target_user_id:
        return False  # insufficient privileges

    # Ensure the target data exists before attempting deletion
    if target_user_id not in USER_DATA:
        return False  # nothing to delete

    try:
        del USER_DATA[target_user_id]
        return True
    except Exception:
        # In a real system we would log this exception.
        return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    assert delete_user_data(2, 1) is True   # admin deleting user 1
    assert delete_user_data(3, 3) is True   # user deleting own data
    assert delete_user_data(1, 3) is False  # user attempting to delete another user's data
    assert delete_user_data(4, 1) is False  # non‑existent requester