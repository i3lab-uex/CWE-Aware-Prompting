# -*- coding: utf-8 -*-
"""
Module providing a secure user data deletion function.

The function enforces that only the target user themselves or an administrator
may delete a user's data.  It performs explicit authorization checks to avoid
CWE-862 (Missing Authorization) and guards against common pitfalls such as
missing keys or improper type handling.
"""

from typing import Dict

# Example user store.  In a real system these would be retrieved from a database.
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "user"},
    2: {"username": "bob",     "role": "admin"},
    3: {"username": "charlie", "role": "user"},
}

# Example user data store.
USER_DATA: Dict[int, Dict[str, str]] = {
    1: {"email": "alice@example.com", "preferences": "dark_mode"},
    2: {"email": "bob@example.com",   "preferences": "light_mode"},
    3: {"email": "charlie@example.com","preferences": "dark_mode"},
}


def delete_user_data(current_user_id: int, target_user_id: int) -> bool:
    """
    Delete the data belonging to ``target_user_id`` if and only if
    ``current_user_id`` is the same user or has an admin role.

    Parameters
    ----------
    current_user_id : int
        The ID of the user making the deletion request.
    target_user_id : int
        The ID of the user whose data should be deleted.

    Returns
    -------
    bool
        ``True`` if the deletion succeeded, ``False`` otherwise.

    Raises
    ------
    TypeError
        If either user ID is not an integer.
    KeyError
        If the requesting or target user does not exist in ``USERS``.
    """
    # Validate input types
    if not isinstance(current_user_id, int) or not isinstance(target_user_id, int):
        raise TypeError("User IDs must be integers")

    # Retrieve user records
    try:
        requester = USERS[current_user_id]
        target = USERS[target_user_id]  # not strictly needed, but ensures existence
    except KeyError as exc:
        # Either the requester or target does not exist
        raise KeyError(f"User ID {exc.args[0]} not found") from None

    # Authorization check
    if current_user_id != target_user_id and requester.get("role") != "admin":
        # Not authorized to delete another user's data
        return False

    # Perform the deletion if present
    if target_user_id in USER_DATA:
        del USER_DATA[target_user_id]
        return True

    # No data to delete
    return False


# Example usage (commented out)
if __name__ == "__main__":
    print(delete_user_data(1, 1))   # True
    print(delete_user_data(2, 3))   # True (admin deleting)
    print(delete_user_data(1, 2))   # False (non-admin attempting to delete)