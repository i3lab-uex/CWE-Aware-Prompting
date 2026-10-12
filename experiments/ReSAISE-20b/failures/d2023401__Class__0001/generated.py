# change_user_privileges.py

from typing import Dict

# Example USERS dictionary structure.
# In a real application this would come from a database or secure store.
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "privilege": "admin"},
    2: {"role": "moderator", "privilege": "moderator"},
    3: {"role": "user", "privilege": "normal"},
    # ... additional users ...
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def change_user_privileges(active_user_id: int, affected_user_id: int,
                           updated_privilege: str) -> bool:
    """
    Change the privilege level of a user.

    Parameters
    ----------
    active_user_id : int
        The ID of the user attempting to make the change.
    affected_user_id : int
        The ID of the target user whose privileges are being updated.
    updated_privilege : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was updated successfully, False otherwise.

    Raises
    ------
    ValueError
        If any of the provided user IDs do not exist or if the updated_privilege is invalid.
    """
    # 1. Validate existence of both users
    if active_user_id not in USERS:
        raise ValueError(f"Active user ID {active_user_id} does not exist.")
    if affected_user_id not in USERS:
        raise ValueError(f"Affected user ID {affected_user_id} does not exist.")

    # 2. Validate privilege value
    if updated_privilege not in ALLOWED_PRIVILEGES:
        raise ValueError(f"Invalid privilege level: '{updated_privilege}'.")

    # 3. Authorization check: only admins can change privileges
    active_user_priv = USERS[active_user_id]["privilege"]
    if active_user_priv != "admin":
        # Deny action
        return False

    # 4. Prevent self-modification of admin privileges (optional security measure)
    if active_user_id == affected_user_id and updated_privilege != "admin":
        # An admin should not demote themselves
        return False

    # 5. Perform the update
    USERS[affected_user_id]["privilege"] = updated_privilege

    # 6. Return success
    return True


# Example usage (would normally be in a separate test module)
if __name__ == "__main__":
    try:
        result = change_user_privileges(1, 3, "moderator")
        print(f"Privilege change successful: {result}")
    except ValueError as e:
        print(f"Error: {e}")