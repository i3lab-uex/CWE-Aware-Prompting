# -*- coding: utf-8 -*-
"""
Implementation of a privilege update function with proper authorization checks.

The module defines an in‑memory `USERS` dictionary representing a simple user
store.  The function `update_privileges()` verifies that the acting user is an
administrator, validates the requested role and target user existence,
and then applies the change.

Security considerations:
- Only users with the 'admin' role are permitted to modify privileges
  (CWE‑862).
- Input is validated against a whitelist of allowed roles.
- The function returns a boolean indicating success or failure, avoiding
  accidental leakage of sensitive information.

The module can be extended to support persistent storage or more complex
authorization policies.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# In‑memory user store for demonstration purposes
# Each user entry contains at least a 'role' field.
USERS: dict[int, dict[str, str]] = {
    1: {"username": "alice", "role": "admin"},
    2: {"username": "bob",   "role": "moderator"},
    3: {"username": "carol", "role": "normal"},
}

# --------------------------------------------------------------------------- #
# Allowed privilege levels
ALLOWED_ROLES = {"normal", "moderator", "admin"}


def update_privileges(
    acting_user_id: int,
    affected_user_id: int,
    new_role: str,
) -> bool:
    """
    Modify the role of a user after performing necessary checks.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to change privileges.
    affected_user_id : int
        ID of the target user whose role is to be changed.
    new_role : str
        Desired role for the affected user.

    Returns
    -------
    bool
        True if the privilege change succeeded, False otherwise.
    """
    # Basic type checks (optional but defensive)
    if not isinstance(acting_user_id, int) or not isinstance(affected_user_id, int):
        return False
    if not isinstance(new_role, str):
        return False

    # 1. Verify that the acting user exists
    acting_user = USERS.get(acting_user_id)
    if not acting_user:
        return False

    # 2. Authorization: only admins may modify roles
    if acting_user.get("role") != "admin":
        return False

    # 3. Verify that the target user exists
    affected_user = USERS.get(affected_user_id)
    if not affected_user:
        return False

    # 4. Validate the new role
    if new_role not in ALLOWED_ROLES:
        return False

    # 5. Perform the update
    affected_user["role"] = new_role
    return True


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage
    print(update_privileges(1, 3, "moderator"))  # Expected: True
    print(USERS[3]["role"])                      # Expected: "moderator"

    print(update_privileges(2, 3, "admin"))      # Expected: False (bob is not admin)
    print(update_privileges(1, 4, "normal"))     # Expected: False (user 4 doesn't exist)