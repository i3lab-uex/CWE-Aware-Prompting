# -*- coding: utf-8 -*-
"""
Utility module for user privilege management.

The main entry point is :func:`alter_user_privileges`, which allows an
administrator to change the privilege level of another user account.

The module intentionally performs strict authorization checks and input
validation to mitigate CWE‑862 (Missing Authorization).
"""

from __future__ import annotations

from typing import Dict, Any

# Sample USERS dictionary for demonstration purposes.
# In a real system this would be replaced by persistent storage
# (e.g., a database or an external authentication service).
USERS: Dict[int, Dict[str, Any]] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "carol",   "role": "normal"},
    # ... more users
}

# Define the set of allowed privilege levels.
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def alter_user_privileges(cur_user_id: int, tar_user_id: int, priv_update: str) -> bool:
    """
    Change the privilege level of a target user account.

    Parameters
    ----------
    cur_user_id : int
        ID of the user attempting to perform the privilege change.
    tar_user_id : int
        ID of the user whose privileges are to be updated.
    priv_update : str
        New privilege level to assign ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        ``True`` if the operation succeeded, otherwise ``False``.

    Notes
    -----
    - Only users with the 'admin' role are allowed to modify privileges.
    - The target user must exist in ``USERS``.
    - ``priv_update`` is validated against :data:`ALLOWED_PRIVILEGES`.
    - The function does **not** raise exceptions for common failure modes;
      instead it returns ``False`` to keep the caller in control.
    """
    # ------------------------------------------------------------------
    # 1. Verify that the current user exists
    # ------------------------------------------------------------------
    cur_user = USERS.get(cur_user_id)
    if not cur_user:
        return False

    # ------------------------------------------------------------------
    # 2. Check that the current user has admin privileges
    # ------------------------------------------------------------------
    if cur_user.get("role") != "admin":
        return False

    # ------------------------------------------------------------------
    # 3. Verify that the target user exists
    # ------------------------------------------------------------------
    tar_user = USERS.get(tar_user_id)
    if not tar_user:
        return False

    # ------------------------------------------------------------------
    # 4. Validate the requested privilege level
    # ------------------------------------------------------------------
    if priv_update not in ALLOWED_PRIVILEGES:
        return False

    # ------------------------------------------------------------------
    # 5. Apply the change
    # ------------------------------------------------------------------
    tar_user["role"] = priv_update
    return True


# Example usage (would normally be in a separate test module)
if __name__ == "__main__":
    # Successful change
    assert alter_user_privileges(1, 3, "moderator") is True
    assert USERS[3]["role"] == "moderator"

    # Unauthorized user
    assert alter_user_privileges(2, 3, "admin") is False

    # Non‑existent target
    assert alter_user_privileges(1, 999, "normal") is False

    # Invalid privilege
    assert alter_user_privileges(1, 3, "superuser") is False

    print("All tests passed.")