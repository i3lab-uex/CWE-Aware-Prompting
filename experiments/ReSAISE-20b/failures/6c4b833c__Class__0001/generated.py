# change_user_role.py

"""
This module provides a single function, `change_user_role`, which allows
administrators to modify the privilege level of other users.
The function performs a strict authorization check to prevent
CWE‑862 (Missing Authorization) and includes basic input validation.
"""

# Example USERS dictionary. In a real application this would come from
# persistent storage (e.g., database, file, etc.).
USERS = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
}

# Define the set of valid privilege levels.
VALID_PRIVILEGES = {"normal", "moderator", "admin"}


def change_user_role(modifying_user_id: int,
                     user_to_change_id: int,
                     new_privilege_level: str) -> bool:
    """
    Modify the privilege level of a user.

    Parameters
    ----------
    modifying_user_id : int
        ID of the user attempting to change privileges.
    user_to_change_id : int
        ID of the user whose privilege is being altered.
    new_privilege_level : str
        The new privilege level to assign.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.

    Raises
    ------
    ValueError
        If any of the arguments are invalid or if the new privilege level is not allowed.
    """
    # ---- Input validation ----
    if not isinstance(modifying_user_id, int):
        raise ValueError("modifying_user_id must be an integer")
    if not isinstance(user_to_change_id, int):
        raise ValueError("user_to_change_id must be an integer")
    if not isinstance(new_privilege_level, str):
        raise ValueError("new_privilege_level must be a string")

    # ---- Check that both users exist in the system ----
    if modifying_user_id not in USERS:
        return False  # unknown modifier user
    if user_to_change_id not in USERS:
        return False  # target user does not exist

    # ---- Authorization check: only admins may change privileges ----
    if USERS[modifying_user_id]["role"] != "admin":
        return False  # insufficient privileges

    # ---- Prevent privilege escalation by non-admins ----
    if new_privilege_level not in VALID_PRIVILEGES:
        raise ValueError(f"Invalid privilege level: {new_privilege_level}")

    # Optional: disallow an admin from demoting themselves to non-admin
    if (modifying_user_id == user_to_change_id and new_privilege_level != "admin"):
        # Allow demotion but warn about potential lockout; here we just permit
        pass

    # ---- Perform the privilege change ----
    USERS[user_to_change_id]["role"] = new_privilege_level

    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    print("Before change:", USERS[3])
    success = change_user_role(1, 3, "moderator")
    print("Change succeeded:", success)
    print("After change :", USERS[3])