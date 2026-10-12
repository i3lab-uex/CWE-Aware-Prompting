# ────────────────────── Imports ────────────────────── #
from typing import Dict

# ────────────────────── Global State ────────────────────── #
# Example USERS dictionary. In a real application this would
# likely be loaded from a database or persistent store.
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
}

# ────────────────────── Constants ────────────────────── #
ALLOWED_ROLES = {"normal", "moderator", "admin"}

# ────────────────────── Function Definition ────────────────────── #
def update_privileges(acting_user_id: int,
                      affected_user_id: int,
                      new_role: str) -> bool:
    """
    Update the role of `affected_user_id` to `new_role` if
    `acting_user_id` has sufficient privileges.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to make the change.
    affected_user_id : int
        ID of the target user whose role will be changed.
    new_role : str
        Desired new role ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the role was updated successfully, False otherwise.
    """

    # Basic validation: all IDs must exist
    if acting_user_id not in USERS:
        return False
    if affected_user_id not in USERS:
        return False

    # Validate new_role
    if new_role not in ALLOWED_ROLES:
        return False

    # Only admins may change roles
    if USERS[acting_user_id]["role"] != "admin":
        return False

    # Prevent non-admins from demoting themselves to admin
    if affected_user_id == acting_user_id and new_role != "admin":
        # Admins can change their own role, but not to a lower level
        return False

    # Apply the new role
    USERS[affected_user_id]["role"] = new_role
    return True

# ────────────────────── Example Usage ────────────────────── #
if __name__ == "__main__":
    # Successful change
    assert update_privileges(1, 3, "moderator") is True
    # Non-admin attempting change
    assert update_privileges(2, 3, "admin") is False
    # Invalid role
    assert update_privileges(1, 3, "superuser") is False
    # Self demotion attempt by admin (disallowed)
    assert update_privileges(1, 1, "normal") is False