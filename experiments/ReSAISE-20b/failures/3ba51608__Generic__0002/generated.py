# -*- coding: utf-8 -*-

from typing import Dict

# Example USERS dictionary. In a real application this would be replaced by a database.
USERS: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "privilege": "admin"},
    2: {"name": "Bob",   "privilege": "moderator"},
    3: {"name": "Carol", "privilege": "normal"},
}

# Allowed privilege levels in order of increasing power
PRIVILEGE_LEVELS = ["normal", "moderator", "admin"]


def alter_user_permissions(
    acting_user_id: int,
    targeted_user_id: int,
    new_privilege_level: str
) -> bool:
    """
    Modify the privilege level of a user.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to change privileges.
    targeted_user_id : int
        ID of the user whose privilege is being altered.
    new_privilege_level : str
        The new privilege level to assign ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege modification succeeded, False otherwise.
    """
    # Basic input validation
    if not isinstance(acting_user_id, int) or not isinstance(targeted_user_id, int):
        return False
    if new_privilege_level not in PRIVILEGE_LEVELS:
        return False

    # Check that both users exist
    acting_user = USERS.get(acting_user_id)
    targeted_user = USERS.get(targeted_user_id)

    if acting_user is None or targeted_user is None:
        return False

    # Only admins may change privileges
    if acting_user["privilege"] != "admin":
        return False

    # Prevent accidental removal of the last admin
    if (
        targeted_user["privilege"] == "admin"
        and new_privilege_level != "admin"
    ):
        # Count current admins
        admin_count = sum(
            1 for u in USERS.values() if u["privilege"] == "admin"
        )
        if admin_count <= 1:
            # Do not allow demoting the sole remaining admin
            return False

    # Perform the update
    targeted_user["privilege"] = new_privilege_level
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(alter_user_permissions(1, 3, "moderator"))  # True
    print(USERS[3]["privilege"])                      # moderator