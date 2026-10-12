# change_user_privileges.py

"""
This module provides a secure implementation of changing user privileges.
It performs explicit authorization checks to prevent CWE-862: Missing Authorization.
"""

from typing import Dict

# Example USERS dictionary structure
USERS: Dict[int, Dict[str, str]] = {
    # user_id: { "role": "<role>", "privilege": "<level>" }
    1: {"role": "admin", "privilege": "admin"},
    2: {"role": "moderator", "privilege": "moderator"},
    3: {"role": "user", "privilege": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def change_user_privileges(
    requesting_user_id: int,
    user_to_change_id: int,
    desired_privilege: str
) -> bool:
    """
    Change the privilege level of a target user if the requester is authorized.

    Parameters
    ----------
    requesting_user_id : int
        ID of the user making the request.
    user_to_change_id : int
        ID of the user whose privilege is being changed.
    desired_privilege : str
        Desired privilege level for the target user.

    Returns
    -------
    bool
        True if the change succeeded, False otherwise.
    """
    # Validate desired privilege
    if desired_privilege not in ALLOWED_PRIVILEGES:
        return False

    # Fetch requester and target user records
    requester = USERS.get(requesting_user_id)
    target = USERS.get(user_to_change_id)

    # If either user does not exist, deny
    if requester is None or target is None:
        return False

    # Authorization check: only admins can change privileges
    if requester.get("role") != "admin":
        return False

    # Prevent privilege escalation: admin cannot demote another admin to a lower role
    if (
        target.get("role") == "admin"
        and desired_privilege != "admin"
    ):
        return False

    # Apply the privilege change
    target["privilege"] = desired_privilege
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(change_user_privileges(1, 3, "moderator"))  # Expected: True
    print(change_user_privileges(2, 3, "admin"))      # Expected: False (not admin)
    print(change_user_privileges(1, 2, "admin"))      # Expected: False (demoting admin)