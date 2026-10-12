# -*- coding: utf-8 -*-
"""
Utility module for user privilege management.

The implementation protects against improper access control (CWE‑284) by ensuring that
only users with an `admin` role can modify the privilege of another user.
All inputs are validated and any attempt to bypass these checks results in a
`PermissionError`.  The function returns `True` on success and `False`
otherwise, without exposing sensitive information.
"""

from typing import Dict

# Sample USERS dictionary. In a real system this would be replaced by a database.
USERS: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice",   "role": "admin",     "privilege": "admin"},
    2: {"name": "Bob",     "role": "moderator","privilege": "moderator"},
    3: {"name": "Charlie", "role": "normal",   "privilege": "normal"},
    # ... more users ...
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def _get_user(user_id: int) -> Dict[str, str]:
    """
    Retrieve a user dictionary by ID.

    Raises:
        KeyError: If the user does not exist.
    """
    return USERS[user_id]


def _is_admin(user: Dict[str, str]) -> bool:
    """Check if the user has an admin role."""
    return user.get("role") == "admin"


def change_user_privileges(
    requesting_user_id: int,
    user_to_change_id: int,
    desired_privilege: str,
) -> bool:
    """
    Modify the privilege level of another user.

    Parameters
    ----------
    requesting_user_id : int
        ID of the user making the request.
    user_to_change_id : int
        ID of the target user whose privilege is to be changed.
    desired_privilege : str
        Desired privilege level (`"normal"`, `"moderator"`, or `"admin"`).

    Returns
    -------
    bool
        ``True`` if the privilege change succeeded, otherwise ``False``.

    Raises
    ------
    PermissionError
        If the requesting user is not an admin.
    ValueError
        If the desired privilege is invalid.
    KeyError
        If either user ID does not exist in :data:`USERS`.
    """
    # Validate desired privilege
    if desired_privilege not in ALLOWED_PRIVILEGES:
        raise ValueError(f"Invalid privilege level: {desired_privilege!r}")

    # Retrieve user records
    requester = _get_user(requesting_user_id)
    target = _get_user(user_to_change_id)

    # Enforce admin-only access
    if not _is_admin(requester):
        raise PermissionError("Only admins can change user privileges.")

    # Apply the privilege change
    target["privilege"] = desired_privilege

    # Optional: update role to match privilege for consistency
    target["role"] = desired_privilege

    return True


# Example usage (for demonstration only; remove or guard under __name__ == "__main__")
if __name__ == "__main__":
    try:
        result = change_user_privileges(1, 3, "moderator")
        print(f"Privilege change successful: {result}")
    except Exception as exc:
        print(f"Failed to change privilege: {exc}")