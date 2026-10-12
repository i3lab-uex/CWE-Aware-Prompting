import logging

# Example USERS dictionary structure.
# In a real application this would be loaded from a database or secure store.
USERS = {
    1: {"name": "alice", "role": "admin"},
    2: {"name": "bob",   "role": "moderator"},
    3: {"name": "carol", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}

# Configure logging for audit purposes
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

def update_user_roles(curr_user_id: int, targ_user_id: int, privilege_change: str) -> bool:
    """
    Update the role of a target user.

    Parameters
    ----------
    curr_user_id : int
        ID of the user performing the operation.
    targ_user_id : int
        ID of the target user whose role is to be changed.
    privilege_change : str
        New privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # Validate input types
    if not isinstance(curr_user_id, int) or not isinstance(targ_user_id, int):
        logging.warning("Invalid user ID types provided.")
        return False

    # Validate privilege level
    if privilege_change not in ALLOWED_PRIVILEGES:
        logging.warning(f"Attempted to set invalid privilege level: {privilege_change}")
        return False

    # Retrieve current user and target user info
    curr_user = USERS.get(curr_user_id)
    targ_user = USERS.get(targ_user_id)

    if curr_user is None:
        logging.warning(f"Current user ID {curr_user_id} not found.")
        return False
    if targ_user is None:
        logging.warning(f"Target user ID {targ_user_id} not found.")
        return False

    # Only admins can change roles
    if curr_user["role"] != "admin":
        logging.warning(f"User {curr_user_id} lacks permission to change roles.")
        return False

    # Prevent self-demotion from admin
    if curr_user_id == targ_user_id and privilege_change != "admin":
        logging.warning(f"Admin {curr_user_id} attempted to demote themselves.")
        return False

    # Perform the update
    old_role = targ_user["role"]
    targ_user["role"] = privilege_change

    logging.info(
        f"User {curr_user_id} changed role of user {targ_user_id} "
        f"from '{old_role}' to '{privilege_change}'."
    )
    return True