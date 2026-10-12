# change_user_role.py

from typing import Dict, Any

# Example USERS dictionary structure.
# In a real application this would be loaded from a database or persistent store.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice",   "role": "admin"},
    2: {"name": "Bob",     "role": "moderator"},
    3: {"name": "Charlie", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_ROLES = {"normal", "moderator", "admin"}


def change_user_role(
    modifying_user_id: int,
    user_to_change_id: int,
    new_privilege_level: str
) -> bool:
    """
    Modify the privilege level of a user.

    Parameters
    ----------
    modifying_user_id : int
        ID of the user attempting to change privileges.
    user_to_change_id : int
        ID of the user whose privilege is being altered.
    new_privilege_level : str
        New privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege modification succeeded, False otherwise.

    Raises
    ------
    TypeError
        If any argument is of an unexpected type.
    ValueError
        If the new privilege level is not one of the allowed values.
    PermissionError
        If the modifying user does not have admin rights.
    KeyError
        If either user ID is not present in USERS.
    """
    # Basic type checks
    if not isinstance(modifying_user_id, int):
        raise TypeError("modifying_user_id must be an integer")
    if not isinstance(user_to_change_id, int):
        raise TypeError("user_to_change_id must be an integer")
    if not isinstance(new_privilege_level, str):
        raise TypeError("new_privilege_level must be a string")

    # Validate privilege level
    if new_privilege_level not in ALLOWED_ROLES:
        raise ValueError(f"Invalid privilege level: {new_privilege_level}")

    # Ensure both users exist
    if modifying_user_id not in USERS:
        raise KeyError(f"Modifying user ID {modifying_user_id} does not exist")
    if user_to_change_id not in USERS:
        raise KeyError(f"Target user ID {user_to_change_id} does not exist")

    # Only admins may change privileges
    if USERS[modifying_user_id]["role"] != "admin":
        raise PermissionError("Only admins can change user privileges")

    # Perform the update
    USERS[user_to_change_id]["role"] = new_privilege_level

    return True


# Example usage (would normally be in a separate test or application module)
if __name__ == "__main__":
    try:
        success = change_user_role(1, 3, "moderator")
        print(f"Privilege change successful: {success}")
        print(USERS[3])  # Should now show role 'moderator'
    except Exception as e:
        print(f"Error: {e}")