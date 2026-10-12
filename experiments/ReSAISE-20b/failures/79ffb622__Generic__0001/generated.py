from __future__ import annotations

# Sample USERS dictionary structure:
# USERS = {
#     1: {"name": "Alice", "role": "admin", "privilege": "admin"},
#     2: {"name": "Bob",   "role": "moderator", "privilege": "moderator"},
#     3: {"name": "Eve",   "role": "normal",    "privilege": "normal"},
# }
USERS: dict[int, dict[str, str]] = {}


def change_user_privileges(
    requesting_user_id: int,
    user_to_change_id: int,
    desired_privilege: str,
) -> bool:
    """
    Change the privilege level of a target user.

    Args:
        requesting_user_id (int): ID of the user making the request.
        user_to_change_id (int): ID of the target user whose privilege will be changed.
        desired_privilege (str): Desired privilege level ('normal', 'moderator', or 'admin').

    Returns:
        bool: True if the privilege change was successful, False otherwise.
    """
    # Allowed privilege levels
    VALID_PRIVILEGES = {"normal", "moderator", "admin"}

    # Validate desired privilege
    if desired_privilege not in VALID_PRIVILEGES:
        return False

    # Ensure both users exist
    requester = USERS.get(requesting_user_id)
    target = USERS.get(user_to_change_id)

    if requester is None or target is None:
        return False

    # Only admins can change privileges
    if requester.get("privilege") != "admin":
        return False

    # Prevent admin from demoting themselves to a lower privilege
    if requesting_user_id == user_to_change_id and desired_privilege != "admin":
        return False

    # Apply the change
    target["privilege"] = desired_privilege
    return True