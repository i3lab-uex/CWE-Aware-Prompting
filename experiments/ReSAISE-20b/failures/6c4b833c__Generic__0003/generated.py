import logging

# Configure a basic logger for audit purposes
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Sample USERS dictionary structure
USERS = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def change_user_role(modifying_user_id: int,
                     user_to_change_id: int,
                     new_privilege_level: str) -> bool:
    """
    Allows an administrator to change another user's privilege level.

    Parameters
    ----------
    modifying_user_id : int
        ID of the user attempting to change privileges.
    user_to_change_id : int
        ID of the target user whose privilege is to be altered.
    new_privilege_level : str
        Desired new privilege level.

    Returns
    -------
    bool
        True if the change succeeded, False otherwise.
    """
    # Validate that both users exist
    mod_user = USERS.get(modifying_user_id)
    target_user = USERS.get(user_to_change_id)

    if mod_user is None:
        logging.warning("Modifying user ID %s does not exist.", modifying_user_id)
        return False

    if target_user is None:
        logging.warning("Target user ID %s does not exist.", user_to_change_id)
        return False

    # Only admins can change privileges
    if mod_user["role"] != "admin":
        logging.warning("User %s (%s) attempted privilege change without admin rights.",
                        modifying_user_id, mod_user["role"])
        return False

    # Prevent self‑promotion or demotion
    if modifying_user_id == user_to_change_id:
        logging.warning("User %s attempted to change their own privilege level.", modifying_user_id)
        return False

    # Ensure the new privilege is valid
    if new_privilege_level not in ALLOWED_PRIVILEGES:
        logging.warning("Invalid privilege level '%s' requested by user %s.",
                        new_privilege_level, modifying_user_id)
        return False

    # Apply the change
    old_role = target_user["role"]
    target_user["role"] = new_privilege_level
    logging.info("User %s changed role of user %s from '%s' to '%s'.",
                 modifying_user_id, user_to_change_id,
                 old_role, new_privilege_level)
    return True