# change_user_role.py

from typing import Dict, Any

# Example USERS dictionary. In a real application this would come from a database.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
    # ... more users ...
}

# Valid privilege levels
VALID_ROLES = {"normal", "moderator", "admin"}


def change_user_role(modifying_user_id: int,
                     user_to_change_id: int,
                     new_privilege_level: str) -> bool:
    """
    Change the privilege level of a user.

    Parameters
    ----------
    modifying_user_id : int
        The ID of the user attempting to change privileges.
    user_to_change_id : int
        The ID of the user whose privilege is being altered.
    new_privilege_level : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic type checks to avoid accidental misuse
    if not isinstance(modifying_user_id, int) or not isinstance(user_to_change_id, int):
        return False
    if not isinstance(new_privilege_level, str):
        return False

    # Normalise role string
    new_role = new_privilege_level.strip().lower()
    if new_role not in VALID_ROLES:
        return False

    # Ensure both users exist
    mod_user = USERS.get(modifying_user_id)
    target_user = USERS.get(user_to_change_id)

    if mod_user is None or target_user is None:
        return False

    # Only admins may modify privileges
    if mod_user.get("role") != "admin":
        return False

    # Prevent an admin from demoting themselves to a lower privilege
    if modifying_user_id == user_to_change_id and new_role != "admin":
        return False

    # Apply the change
    target_user["role"] = new_role
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(change_user_role(1, 2, "admin"))   # True
    print(USERS[2]["role"])                  # 'admin'
    print(change_user_role(2, 3, "moderator"))  # False (not an admin)