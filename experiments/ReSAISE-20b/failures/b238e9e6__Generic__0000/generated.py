# -*- coding: utf-8 -*-
"""
User privilege update module.

This module provides a single function `update_privileges` that allows an
administrator to change the role of another user.  The function performs
basic validation, checks that the acting user has the required permissions,
and ensures that only valid roles are accepted.

Author: OpenAI ChatGPT
"""

from typing import Dict

# Example USERS dictionary. In a real application this would be loaded from
# persistent storage or an authentication service.
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
}

# Allowed roles
ALLOWED_ROLES = {"normal", "moderator", "admin"}


def update_privileges(acting_user_id: int, affected_user_id: int,
                      new_role: str) -> bool:
    """
    Update the role of a user.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to change privileges.
    affected_user_id : int
        ID of the user whose privilege is being altered.
    new_role : str
        New role to assign.

    Returns
    -------
    bool
        ``True`` if the operation succeeded, otherwise ``False``.

    Notes
    -----
    - Only users with the role 'admin' can change privileges.
    - The new role must be one of ``ALLOWED_ROLES``.
    - Both user IDs must exist in the USERS dictionary.
    """
    # Validate new_role
    if new_role not in ALLOWED_ROLES:
        return False

    # Check that both users exist
    acting_user = USERS.get(acting_user_id)
    affected_user = USERS.get(affected_user_id)

    if acting_user is None or affected_user is None:
        return False

    # Ensure the acting user has admin privileges
    if acting_user.get("role") != "admin":
        return False

    # Prevent admins from demoting themselves or others to admin without
    # an explicit check (optional security measure)
    if new_role == "admin" and acting_user_id != affected_user_id:
        # Only allow promotion to admin if the acting user is already an admin
        pass  # Already checked above; no further restriction

    # Perform the update
    try:
        affected_user["role"] = new_role
        return True
    except Exception:
        # Log exception in real application; here we simply fail silently.
        return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(update_privileges(1, 3, "moderator"))  # Should return True
    print(USERS[3]["role"])                      # Should output 'moderator'