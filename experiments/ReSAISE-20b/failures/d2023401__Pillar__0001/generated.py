# change_user_privileges.py

from typing import Dict, Any

# Example USERS dictionary; in real use this would be imported from a secure module
USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin", "privilege": "admin"},
    2: {"role": "moderator", "privilege": "moderator"},
    3: {"role": "user", "privilege": "normal"},
}

# Valid privilege levels
VALID_PRIVILEGES = {"normal", "moderator", "admin"}


def change_user_privileges(
    active_user_id: int, affected_user_id: int, updated_privilege: str
) -> bool:
    """
    Change the privilege level of a user account.

    Parameters
    ----------
    active_user_id : int
        ID of the administrator attempting to make the change.
    affected_user_id : int
        ID of the target user whose privileges are being changed.
    updated_privilege : str
        New privilege level to assign ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was successfully updated, False otherwise.
    """
    # Validate that both users exist
    if active_user_id not in USERS or affected_user_id not in USERS:
        return False

    # Only admins may modify privileges
    if USERS[active_user_id]["privilege"] != "admin":
        return False

    # Prevent privilege escalation by non-admins
    if updated_privilege not in VALID_PRIVILEGES:
        return False

    # Optionally prevent an admin from demoting themselves
    if active_user_id == affected_user_id and updated_privilege != "admin":
        return False

    # Perform the update
    USERS[affected_user_id]["privilege"] = updated_privilege
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(change_user_privileges(1, 3, "moderator"))  # Expected: True
    print(USERS[3]["privilege"])                      # Expected: 'moderator'