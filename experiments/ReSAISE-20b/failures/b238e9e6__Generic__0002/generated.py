from typing import Dict

# Example USERS dictionary; in real usage this would be imported or passed in.
USERS: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "moderator"},
    3: {"name": "Carol", "role": "normal"},
}

ALLOWED_ROLES = {"normal", "moderator", "admin"}

def update_privileges(acting_user_id: int, affected_user_id: int, new_role: str) -> bool:
    """
    Update the role of a user if the acting user has admin privileges.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to change privileges.
    affected_user_id : int
        ID of the user whose privilege is being altered.
    new_role : str
        The new privilege level to assign.

    Returns
    -------
    bool
        True if the role was updated successfully, False otherwise.
    """
    # Validate new_role
    if new_role not in ALLOWED_ROLES:
        return False

    # Ensure acting user exists and is admin
    acting_user = USERS.get(acting_user_id)
    if not acting_user or acting_user.get("role") != "admin":
        return False

    # Ensure affected user exists
    affected_user = USERS.get(affected_user_id)
    if not affected_user:
        return False

    # Perform the update
    affected_user["role"] = new_role
    return True