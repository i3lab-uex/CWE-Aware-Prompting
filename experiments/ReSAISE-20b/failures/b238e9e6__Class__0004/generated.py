# users.py
from typing import Dict

# Example user store. In a real application this would be backed by a database.
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
}

# Allowed roles
ALLOWED_ROLES = {"normal", "moderator", "admin"}


def update_privileges(acting_user_id: int, affected_user_id: int, new_role: str) -> bool:
    """
    Modify the privilege level of a user.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to perform the change.
    affected_user_id : int
        ID of the target user whose role will be changed.
    new_role : str
        Desired new role for the target user.

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # --- Authorization check (CWE-862) ------------------------------------
    acting_user = USERS.get(acting_user_id)
    if not acting_user:
        # Acting user does not exist
        return False

    if acting_user.get("role") != "admin":
        # Only admins are allowed to modify roles
        return False

    # --- Validation of target user ---------------------------------------
    affected_user = USERS.get(affected_user_id)
    if not affected_user:
        # Target user does not exist
        return False

    # --- Validation of new role ------------------------------------------
    if new_role not in ALLOWED_ROLES:
        return False

    # --- Perform the update ---------------------------------------------
    affected_user["role"] = new_role
    return True


# -------------------------------------------------------------------------
if __name__ == "__main__":
    # Example usage and simple tests
    assert update_privileges(1, 3, "moderator") is True   # admin changes charlie
    assert USERS[3]["role"] == "moderator"

    assert update_privileges(2, 3, "admin") is False      # non-admin cannot change
    assert USERS[3]["role"] == "moderator"

    assert update_privileges(1, 999, "normal") is False   # target does not exist
    assert update_privileges(1, 3, "superuser") is False  # invalid role
    print("All tests passed.")