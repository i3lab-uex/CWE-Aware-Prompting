import logging
from typing import Dict

# Example USERS dictionary structure.
# In a real application this would come from a database or secure store.
USERS: Dict[int, dict] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "moderator"},
    3: {"name": "Carol", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}

# Configure logging for audit trail
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [user:%(requester)d] %(message)s",
)


def change_user_privileges(
    requesting_user_id: int,
    user_to_change_id: int,
    desired_privilege: str,
) -> bool:
    """
    Allow an admin to change the privilege level of another user.

    Args:
        requesting_user_id: ID of the user making the request.
        user_to_change_id: ID of the target user whose privilege is to be changed.
        desired_privilege: Desired new privilege level ('normal', 'moderator', or 'admin').

    Returns:
        True if the change was successful, False otherwise.
    """
    # Validate presence of users
    requester = USERS.get(requesting_user_id)
    target = USERS.get(user_to_change_id)

    if requester is None:
        logging.warning("Requesting user ID %d not found.", requesting_user_id)
        return False
    if target is None:
        logging.warning("Target user ID %d not found.", user_to_change_id)
        return False

    # Only admins may change privileges
    if requester.get("role") != "admin":
        logging.warning(
            "User %d (%s) attempted privilege change without admin rights.",
            requesting_user_id,
            requester.get("name"),
        )
        return False

    # Validate desired privilege
    if desired_privilege not in ALLOWED_PRIVILEGES:
        logging.warning(
            "Invalid privilege '%s' requested by user %d.",
            desired_privilege,
            requesting_user_id,
        )
        return False

    # Prevent admin from demoting themselves inadvertently
    if user_to_change_id == requesting_user_id and desired_privilege != "admin":
        logging.warning(
            "Admin user %d attempted to demote themselves.", requesting_user_id
        )
        return False

    # Apply change
    old_role = target.get("role")
    target["role"] = desired_privilege

    logging.info(
        "User %d changed role of user %d from '%s' to '%s'.",
        requesting_user_id,
        user_to_change_id,
        old_role,
        desired_privilege,
    )
    return True