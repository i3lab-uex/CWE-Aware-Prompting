# -*- coding: utf-8 -*-
"""
Module: user_privileges

Provides a function to safely update user privileges while enforcing
proper authorization checks.
"""

from typing import Dict

# Example USERS dictionary. In a real system this would be
# retrieved from persistent storage (e.g., database, ORM).
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
}

# Allowed privilege levels in ascending order of authority.
ROLE_HIERARCHY = ("normal", "moderator", "admin")
ALLOWED_ROLES = set(ROLE_HIERARCHY)


def _get_role_rank(role: str) -> int:
    """
    Return the numeric rank of a role. Lower numbers indicate lower authority.
    Raises ValueError if the role is not recognized.
    """
    try:
        return ROLE_HIERARCHY.index(role)
    except ValueError as exc:
        raise ValueError(f"Unknown role: {role}") from exc


def update_privileges(
    acting_user_id: int,
    affected_user_id: int,
    new_role: str
) -> bool:
    """
    Safely change the privilege level of a user.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to change privileges.
    affected_user_id : int
        ID of the target user whose role will be modified.
    new_role : str
        Desired role for the target user.

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # Basic validation of inputs
    if new_role not in ALLOWED_ROLES:
        return False

    # Ensure both users exist
    acting_user = USERS.get(acting_user_id)
    affected_user = USERS.get(affected_user_id)

    if acting_user is None or affected_user is None:
        return False

    # Authorization: Acting user must be admin
    if acting_user["role"] != "admin":
        return False

    # Optional: Prevent lowering admin privileges of another admin
    if affected_user["role"] == "admin" and new_role != "admin":
        return False

    # Update the role
    affected_user["role"] = new_role
    return True


# Example usage (for demonstration; remove or guard in production)
if __name__ == "__main__":
    # Admin changing Bob's role to normal
    success = update_privileges(1, 2, "normal")
    print(f"Update succeeded: {success}")
    print(USERS[2])  # {'username': 'bob', 'role': 'normal'}