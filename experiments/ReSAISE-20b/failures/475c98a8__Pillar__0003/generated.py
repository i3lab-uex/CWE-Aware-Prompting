import re

# Example USERS dictionary: {user_id: {"role": <str>, "privilege": <str>}}
USERS = {
    1: {"role": "admin", "privilege": "admin"},
    2: {"role": "moderator", "privilege": "moderator"},
    3: {"role": "user", "privilege": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def update_user_roles(curr_user_id: int, targ_user_id: int, privilege_change: str) -> bool:
    """
    Update the privilege level of a target user.

    Parameters
    ----------
    curr_user_id : int
        ID of the user attempting the change.
    targ_user_id : int
        ID of the user whose privilege is to be changed.
    privilege_change : str
        Desired new privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was successfully updated, False otherwise.
    """
    # 1. Validate input types
    if not isinstance(curr_user_id, int) or not isinstance(targ_user_id, int):
        return False
    if not isinstance(privilege_change, str) or privilege_change.lower() not in ALLOWED_PRIVILEGES:
        return False

    # 2. Ensure both users exist
    curr_user = USERS.get(curr_user_id)
    targ_user = USERS.get(targ_user_id)
    if curr_user is None or targ_user is None:
        return False

    # 3. Enforce access control: only admins can modify privileges
    if curr_user["privilege"] != "admin":
        return False

    # 4. Prevent privilege escalation: an admin cannot assign 'admin' to another user
    #    unless they are the only admin in the system (simplified check).
    if privilege_change.lower() == "admin":
        # Count current admins
        admin_count = sum(1 for u in USERS.values() if u["privilege"] == "admin")
        # If more than one admin exists, restrict assigning new admin
        if admin_count > 1:
            return False

    # 5. Update the target user's privilege
    targ_user["privilege"] = privilege_change.lower()
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(update_user_roles(1, 3, "moderator"))  # Expected: True
    print(USERS[3])  # {'role': 'user', 'privilege': 'moderator'}