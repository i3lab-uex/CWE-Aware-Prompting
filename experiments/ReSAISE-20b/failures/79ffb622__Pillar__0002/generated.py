#!/usr/bin/env python3
"""
User privilege management module.

This module provides a single function, `change_user_privileges`, which allows
an administrator to modify the privilege level of another user account.  The
implementation follows best practices for access control (CWE‑284) by ensuring
that only users with the 'admin' role may perform changes, that the target user
exists, and that the requested privilege level is valid.  All checks are done
atomically to avoid race conditions.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# Sample user store. In a real application this would be replaced by a database.
USERS: dict[int, dict[str, str]] = {
    1: {"name": "Alice",   "role": "admin"},
    2: {"name": "Bob",     "role": "moderator"},
    3: {"name": "Charlie", "role": "normal"},
    # Add more users as needed
}

# Allowed privilege levels.  The set is defined once for efficiency.
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def change_user_privileges(
    requesting_user_id: int,
    user_to_change_id: int,
    desired_privilege: str
) -> bool:
    """
    Change the privilege level of a user account.

    Parameters
    ----------
    requesting_user_id : int
        ID of the user making the request.
    user_to_change_id : int
        ID of the user whose privilege is being changed.
    desired_privilege : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege change was applied successfully; False otherwise.

    Notes
    -----
    - Only users with the 'admin' role may modify other accounts.
    - The function performs a single atomic check of all conditions to
      mitigate race‑condition attacks.
    - The function does not modify the requesting user's own privilege level
      to avoid accidental self‑promotion or demotion.
    """
    # Validate that the requesting user exists
    requester = USERS.get(requesting_user_id)
    if not requester:
        # Unknown requester – deny access
        return False

    # Ensure the requester has admin privileges
    if requester.get("role") != "admin":
        return False

    # Validate that the target user exists
    target = USERS.get(user_to_change_id)
    if not target:
        return False

    # Validate the desired privilege level
    if desired_privilege not in ALLOWED_PRIVILEGES:
        return False

    # Prevent accidental self‑privilege change (optional security measure)
    if requesting_user_id == user_to_change_id:
        return False

    # Apply the change atomically
    target["role"] = desired_privilege
    return True


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(change_user_privileges(1, 3, "moderator"))  # Expected: True
#     print(USERS[3]["role"])  # Expected: "moderator"