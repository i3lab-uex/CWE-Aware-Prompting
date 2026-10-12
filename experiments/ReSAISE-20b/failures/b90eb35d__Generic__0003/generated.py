# -*- coding: utf-8 -*-

"""
User privilege modification module.

Provides a single function `modify_user_privileges` that allows an
administrator to change the privilege level of another user account.

The USERS dictionary is expected to be a global mapping from integer
user IDs to dictionaries containing at least the keys:
    - "role" (str): e.g. "user", "moderator", "admin"
    - "privilege" (str): one of "normal", "moderator", or "admin"

The function performs the following checks:

1. Verifies that `current_user_id` exists and has an admin role.
2. Verifies that `target_user_id` exists in the USERS dictionary.
3. Validates that `new_privilege` is one of the allowed privilege strings.
4. Updates the target user's privilege if all checks pass.

It returns `True` on success and `False` otherwise.  No exceptions are
raised for normal failure cases; only a `ValueError` is raised if the
new privilege string is invalid, to signal programmer error.

Author: ChatGPT
"""

from typing import Dict

# Example USERS dictionary for illustration purposes.
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "privilege": "admin"},
    2: {"role": "moderator", "privilege": "moderator"},
    3: {"role": "user", "privilege": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def modify_user_privileges(
    current_user_id: int,
    target_user_id: int,
    new_privilege: str,
) -> bool:
    """
    Modify the privilege level of a target user.

    Parameters
    ----------
    current_user_id : int
        The ID of the user attempting to make the change.
    target_user_id : int
        The ID of the user whose privileges are to be changed.
    new_privilege : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was successfully changed, False otherwise.
    """
    # Ensure current user exists and is an admin
    current_user = USERS.get(current_user_id)
    if not current_user:
        return False

    if current_user.get("role") != "admin":
        # Only admins can change privileges
        return False

    # Ensure target user exists
    target_user = USERS.get(target_user_id)
    if not target_user:
        return False

    # Validate new privilege
    if new_privilege not in ALLOWED_PRIVILEGES:
        raise ValueError(
            f"Invalid privilege '{new_privilege}'. "
            f"Allowed values: {sorted(ALLOWED_PRIVILEGES)}"
        )

    # Update privilege
    target_user["privilege"] = new_privilege
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Successful change
    assert modify_user_privileges(1, 3, "moderator") is True
    assert USERS[3]["privilege"] == "moderator"

    # Failure: non-admin attempting change
    assert modify_user_privileges(2, 3, "admin") is False

    # Failure: invalid privilege string
    try:
        modify_user_privileges(1, 3, "superuser")
    except ValueError as e:
        print(e)