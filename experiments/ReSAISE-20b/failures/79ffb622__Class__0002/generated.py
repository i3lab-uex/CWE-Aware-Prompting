# change_user_privileges.py

from typing import Dict, Any

# Example USERS dictionary structure:
# USERS = {
#     1: {"name": "Alice", "role": "admin", "privilege": "admin"},
#     2: {"name": "Bob",   "role": "moderator", "privilege": "moderator"},
#     3: {"name": "Carol", "role": "normal",   "privilege": "normal"},
# }
USERS: Dict[int, Dict[str, Any]] = {}

VALID_PRIVILEGES = {"normal", "moderator", "admin"}


def change_user_privileges(
    requesting_user_id: int,
    user_to_change_id: int,
    desired_privilege: str
) -> bool:
    """
    Change the privilege level of a target user.

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
        True if the change was applied successfully, False otherwise.
    """
    # Basic validation of arguments
    if not isinstance(requesting_user_id, int) or not isinstance(user_to_change_id, int):
        return False

    if desired_privilege not in VALID_PRIVILEGES:
        return False

    # Ensure both users exist
    requester = USERS.get(requesting_user_id)
    target = USERS.get(user_to_change_id)

    if requester is None or target is None:
        return False

    # Authorization check: only admins may change privileges
    if requester.get("role") != "admin":
        return False

    # Prevent self‑privilege escalation: an admin cannot demote themselves
    if requesting_user_id == user_to_change_id and desired_privilege != "admin":
        return False

    # Apply the change
    target["privilege"] = desired_privilege
    # Optionally sync role with privilege if your system uses both
    target["role"] = desired_privilege

    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    USERS.update({
        1: {"name": "Alice", "role": "admin", "privilege": "admin"},
        2: {"name": "Bob",   "role": "moderator", "privilege": "moderator"},
        3: {"name": "Carol", "role": "normal",   "privilege": "normal"},
    })

    assert change_user_privileges(1, 2, "admin") is True
    assert USERS[2]["privilege"] == "admin"
    assert change_user_privileges(2, 3, "moderator") is False