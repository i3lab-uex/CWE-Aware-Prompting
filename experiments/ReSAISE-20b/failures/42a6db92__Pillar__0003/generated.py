# -*- coding: utf-8 -*-

"""
Secure privilege modification module.
"""

from typing import Dict

# Example USERS dictionary structure
USERS: Dict[int, Dict[str, str]] = {
    # user_id : {"role": "<admin|moderator|normal>", "privilege_level": "<admin|moderator|normal>"}
    1: {"role": "admin", "privilege_level": "admin"},
    2: {"role": "moderator", "privilege_level": "moderator"},
    3: {"role": "normal", "privilege_level": "normal"},
}

VALID_PRIVILEGE_LEVELS = {"admin", "moderator", "normal"}


def modify_privilege_level(
    acting_user_id: int,
    user_id_to_change: int,
    new_level: str
) -> bool:
    """
    Allow an admin user to change another user's privilege level.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to perform the change.
    user_id_to_change : int
        ID of the target user whose privilege is to be updated.
    new_level : str
        Desired privilege level for the target user.

    Returns
    -------
    bool
        True if the change succeeded, False otherwise.
    """
    # Verify both users exist
    acting_user = USERS.get(acting_user_id)
    target_user = USERS.get(user_id_to_change)

    if acting_user is None:
        # Acting user not found
        return False

    if target_user is None:
        # Target user does not exist
        return False

    # Only admins may modify privileges
    if acting_user.get("role") != "admin":
        return False

    # Validate the new privilege level
    if new_level not in VALID_PRIVILEGE_LEVELS:
        return False

    # Prevent privilege escalation via self-modification: admins can demote themselves
    # but not promote others to admin if they are not already admin.
    # Here we allow admins to change any level; adjust logic as needed.

    # Apply the new privilege level
    target_user["privilege_level"] = new_level

    # Update role to reflect the privilege level
    target_user["role"] = new_level

    return True


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(modify_privilege_level(1, 2, "admin"))  # True
#     print(USERS[2])  # {'role': 'admin', 'privilege_level': 'admin'}