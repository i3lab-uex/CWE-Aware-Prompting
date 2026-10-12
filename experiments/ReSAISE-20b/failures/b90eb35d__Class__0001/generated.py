# modify_user_privileges.py

"""
This module provides a single function `modify_user_privileges` that allows
an administrator to change the privilege level of another user account.

The function performs a strict authorization check to ensure that only
users with the 'admin' privilege can modify privileges. It also validates
that both the acting user and target user exist, that the new privilege is
one of the allowed values, and that an admin cannot demote themselves.

Author: OpenAI ChatGPT
"""

from typing import Dict

# Sample USERS dictionary. In a real application this would be replaced
# by a database or persistent storage.
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def modify_user_privileges(
    current_user_id: int,
    target_user_id: int,
    new_privilege: str
) -> bool:
    """
    Modify the privilege level of a target user.

    Parameters
    ----------
    current_user_id : int
        The ID of the user attempting to perform the modification.
    target_user_id : int
        The ID of the user whose privileges are to be changed.
    new_privilege : str
        The desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was successfully updated; False otherwise.
    """
    # 1. Verify both users exist
    if current_user_id not in USERS:
        return False
    if target_user_id not in USERS:
        return False

    # 2. Verify the actor is an admin
    if USERS[current_user_id]["role"] != "admin":
        return False

    # 3. Validate the new privilege value
    if new_privilege not in ALLOWED_PRIVILEGES:
        return False

    # 4. Prevent an admin from demoting themselves
    if current_user_id == target_user_id and new_privilege != "admin":
        return False

    # 5. Apply the change
    USERS[target_user_id]["role"] = new_privilege
    return True


# Example usage (for testing purposes)
if __name__ == "__main__":
    # Successful change
    print(modify_user_privileges(1, 3, "moderator"))  # True
    print(USERS[3]["role"])                          # 'moderator'

    # Unauthorized attempt
    print(modify_user_privileges(2, 3, "admin"))      # False

    # Invalid privilege
    print(modify_user_privileges(1, 2, "superuser"))  # False

    # Admin demoting themselves
    print(modify_user_privileges(1, 1, "moderator"))  # False