# SPDX-License-Identifier: MIT
"""
Utility module for user privilege management.

The `change_user_privileges` function allows an administrator to modify the
privilege level of another user.  It performs proper authorization checks and
validates inputs to prevent common security pitfalls such as CWE‑862
(Missing Authorization).

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# Example user database structure. In a real application this would be
# replaced by persistent storage (e.g., a database).
USERS = {
    1: {"username": "alice", "role": "admin", "privilege": "admin"},
    2: {"username": "bob",   "role": "moderator", "privilege": "moderator"},
    3: {"username": "charlie","role": "normal",   "privilege": "normal"},
    # Add more users as needed...
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def change_user_privileges(
    requesting_user_id: int,
    user_to_change_id: int,
    desired_privilege: str
) -> bool:
    """
    Modify the privilege level of a target user.

    Parameters
    ----------
    requesting_user_id : int
        ID of the user making the request.
    user_to_change_id : int
        ID of the target user whose privilege will be changed.
    desired_privilege : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege change was applied, False otherwise.

    Raises
    ------
    ValueError
        If the desired privilege is not one of the allowed values.
    KeyError
        If either user ID does not exist in USERS.

    Notes
    -----
    - Only users with the 'admin' role are authorized to change other users'
      privileges.
    - The function does not allow a user to elevate themselves; the target
      must be a different user.
    """
    # Validate input privilege value early
    if desired_privilege not in ALLOWED_PRIVILEGES:
        raise ValueError(f"Invalid privilege level: {desired_privilege!r}")

    # Retrieve requesting and target users; raise KeyError if not found
    requester = USERS[requesting_user_id]
    target = USERS[user_to_change_id]

    # Authorization check: requester must be an admin
    if requester["role"] != "admin":
        return False

    # Prevent self‑elevation: an admin cannot change their own privilege
    if requesting_user_id == user_to_change_id:
        return False

    # Apply the privilege change
    target["privilege"] = desired_privilege
    return True


# Example usage (commented out to keep module importable)
if __name__ == "__main__":
    print("Before change:", USERS[3]["privilege"])
    success = change_user_privileges(1, 3, "moderator")
    print("Change successful:", success)
    print("After change:", USERS[3]["privilege"])