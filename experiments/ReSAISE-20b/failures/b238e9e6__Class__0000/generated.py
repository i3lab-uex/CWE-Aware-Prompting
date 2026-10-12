# SPDX-License-Identifier: MIT
"""
Module providing privilege management utilities.

Author: OpenAI
"""

from typing import Dict

# Example in-memory user store. In a real application this would be replaced by a database.
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_ROLES = {"normal", "moderator", "admin"}


def update_privileges(acting_user_id: int, affected_user_id: int, new_role: str) -> bool:
    """
    Update the role of a user after performing necessary checks.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to change privileges.
    affected_user_id : int
        ID of the user whose role is being modified.
    new_role : str
        The desired new role for the affected user.

    Returns
    -------
    bool
        ``True`` if the operation succeeded, otherwise ``False``.

    Notes
    -----
    * Only users with an ``admin`` role may modify other users' roles.
    * The new role must be one of the predefined ``ALLOWED_ROLES``.
    * No changes are made if any check fails; the function returns ``False``.
    """
    # Verify that both users exist
    acting_user = USERS.get(acting_user_id)
    affected_user = USERS.get(affected_user_id)

    if acting_user is None:
        # Acting user does not exist
        return False

    if affected_user is None:
        # Target user does not exist
        return False

    # Authorization check: acting user must be an admin
    if acting_user.get("role") != "admin":
        # Acting user lacks sufficient privileges
        return False

    # Validate the new role
    if new_role not in ALLOWED_ROLES:
        return False

    # All checks passed; perform the update
    affected_user["role"] = new_role
    return True


# Example usage (for demonstration only; remove or guard in production)
if __name__ == "__main__":
    print("Before:", USERS[3]["role"])
    success = update_privileges(1, 3, "moderator")
    print("Success:", success)
    print("After:", USERS[3]["role"])