# -*- coding: utf-8 -*-

"""
Implementation of delete_user_data with proper authorization checks.

Author: OpenAI ChatGPT
"""

from typing import Dict

# Sample data structures (would normally come from a database or other persistent store)
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice", "role": "user"},
    2: {"username": "bob",   "role": "admin"},
    3: {"username": "carol", "role": "user"},
}

USER_DATA: Dict[int, Dict] = {
    1: {"preferences": {"theme": "dark"}, "posts": [101, 102]},
    2: {"preferences": {"theme": "light"}, "posts": [201, 202]},
    3: {"preferences": {"theme": "dark"}, "posts": [301, 302]},
}


def delete_user_data(current_user_id: int, target_user_id: int) -> bool:
    """
    Delete all data belonging to `target_user_id` if the requesting user is
    either the same user or an administrator.

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
    # Basic input validation
    if not isinstance(current_user_id, int) or not isinstance(target_user_id, int):
        return False

    # Ensure both users exist
    current_user = USERS.get(current_user_id)
    target_user_exists = target_user_id in USER_DATA
    if current_user is None or not target_user_exists:
        return False

    # Authorization check: allow if the current user is the target or an admin
    if current_user_id != target_user_id and current_user.get("role") != "admin":
        return False

    # Perform deletion
    try:
        del USER_DATA[target_user_id]
        return True
    except KeyError:
        # Data might have already been deleted or never existed
        return False


# Example usage (for demonstration; remove or comment out in production)
if __name__ == "__main__":
    print(delete_user_data(1, 3))   # False – alice cannot delete carol's data
    print(delete_user_data(2, 3))   # True – admin bob deletes carol's data
    print(USER_DATA)                # Should no longer contain key 3