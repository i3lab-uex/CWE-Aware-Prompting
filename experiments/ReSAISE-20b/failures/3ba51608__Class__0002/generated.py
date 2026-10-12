# -*- coding: utf-8 -*-

from typing import Dict

# Example user database structure.
# In a real system this would be replaced by persistent storage (DB, LDAP, etc.).
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
}

# Allowed privilege levels.
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def alter_user_permissions(
    acting_user_id: int,
    targeted_user_id: int,
    new_privilege_level: str
) -> bool:
    """
    Modify the privilege level of a target user.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to change privileges.
    targeted_user_id : int
        ID of the user whose privilege is being altered.
    new_privilege_level : str
        Desired privilege level for the target user.

    Returns
    -------
    bool
        True if the modification succeeded, False otherwise.
    """
    # Validate that both users exist.
    acting_user = USERS.get(acting_user_id)
    target_user = USERS.get(targeted_user_id)

    if acting_user is None or target_user is None:
        # Either the actor or the target does not exist.
        return False

    # Authorization check: only admins may alter privileges.
    if acting_user.get("role") != "admin":
        return False

    # Validate the requested privilege level.
    if new_privilege_level not in ALLOWED_PRIVILEGES:
        return False

    # Perform the update.
    target_user["role"] = new_privilege_level
    return True


# Example usage (for testing purposes only):
if __name__ == "__main__":
    print(alter_user_permissions(1, 3, "moderator"))  # True
    print(alter_user_permissions(2, 3, "admin"))      # False (bob is not admin)
    print(alter_user_permissions(1, 3, "superuser")) # False (invalid privilege)