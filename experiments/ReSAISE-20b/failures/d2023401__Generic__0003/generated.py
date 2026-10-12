# change_user_privileges.py

"""
Utility function to modify user privilege levels.

The USERS dictionary is assumed to be a global mapping of user IDs to
user data dictionaries, e.g.:

USERS = {
    1: {"name": "Alice", "privilege": "admin"},
    2: {"name": "Bob",   "privilege": "normal"},
    ...
}
"""

from typing import Dict

# Example USERS dictionary; replace with the actual data source in production
USERS: Dict[int, Dict[str, str]] = {}


def change_user_privileges(active_user_id: int,
                           affected_user_id: int,
                           updated_privilege: str) -> bool:
    """
    Change the privilege level of a user account.

    Parameters
    ----------
    active_user_id : int
        ID of the administrator attempting the change.
    affected_user_id : int
        ID of the user whose privilege will be modified.
    updated_privilege : str
        New privilege level to assign ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was successfully updated, False otherwise.
    """
    # Validate privilege string
    valid_privileges = {"normal", "moderator", "admin"}
    if updated_privilege not in valid_privileges:
        return False

    # Ensure both users exist
    active_user = USERS.get(active_user_id)
    affected_user = USERS.get(affected_user_id)

    if not active_user or not affected_user:
        return False

    # Only admins may change privileges
    if active_user.get("privilege") != "admin":
        return False

    # Prevent self-modification of admin privileges
    if active_user_id == affected_user_id and updated_privilege != "admin":
        return False

    # Update the privilege
    try:
        affected_user["privilege"] = updated_privilege
        return True
    except Exception:
        # Any unexpected error results in failure
        return False


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    # Populate sample USERS
    USERS[1] = {"name": "Alice", "privilege": "admin"}
    USERS[2] = {"name": "Bob",   "privilege": "normal"}

    print(change_user_privileges(1, 2, "moderator"))  # Expected: True
    print(USERS[2]["privilege"])                     # Expected: "moderator"