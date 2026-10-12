# -*- coding: utf-8 -*-
"""
Module providing privileged user role updates.
"""

from typing import Dict

# Example USERS dictionary
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
}

# Valid privilege levels
VALID_ROLES = {"normal", "moderator", "admin"}


def update_privileges(acting_user_id: int,
                      affected_user_id: int,
                      new_role: str) -> bool:
    """
    Modify the role of a user if the acting user is an administrator.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to change privileges.
    affected_user_id : int
        ID of the user whose privilege is being altered.
    new_role : str
        New role to assign. Must be one of ``VALID_ROLES``.

    Returns
    -------
    bool
        ``True`` if the role was updated successfully, otherwise ``False``.

    Notes
    -----
    * Only users with the 'admin' role may modify other users' roles.
    * The function does **not** allow a user to change their own role.
    * Input validation ensures that only legitimate roles are accepted.

    Raises
    ------
    None

    Security considerations
    -----------------------
    This function mitigates CWE-284 by enforcing strict access control:
        - It checks that the acting user exists and has an 'admin' role.
        - It prevents self‑modification of roles.
    """

    # Validate input types
    if not all(isinstance(x, int) for x in (acting_user_id, affected_user_id)):
        return False
    if not isinstance(new_role, str):
        return False

    # Normalize role string
    new_role = new_role.lower()

    # Ensure the requested role is valid
    if new_role not in VALID_ROLES:
        return False

    # Retrieve acting user data
    acting_user = USERS.get(acting_user_id)
    if not acting_user:
        return False

    # Only admins may modify roles
    if acting_user.get("role") != "admin":
        return False

    # Prevent self‑modification
    if acting_user_id == affected_user_id:
        return False

    # Retrieve affected user data
    affected_user = USERS.get(affected_user_id)
    if not affected_user:
        return False

    # Update role
    affected_user["role"] = new_role
    return True


# Example usage (for testing only)
if __name__ == "__main__":
    # Successful update
    print(update_privileges(1, 3, "moderator"))  # True

    # Attempt by non‑admin
    print(update_privileges(2, 3, "admin"))      # False

    # Self‑modification attempt
    print(update_privileges(1, 1, "normal"))     # False

    # Invalid role
    print(update_privileges(1, 2, "superuser"))  # False