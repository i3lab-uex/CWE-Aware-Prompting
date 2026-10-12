# Define a sample USERS dictionary for demonstration purposes.
# In real applications this would come from a database or secure storage.
USERS = {
    1: {"username": "alice",   "role": "admin",     "privilege_level": "admin"},
    2: {"username": "bob",     "role": "moderator","privilege_level": "moderator"},
    3: {"username": "charlie", "role": "user",     "privilege_level": "normal"},
    # ... more users ...
}

def modify_privilege_level(acting_user_id: int, user_id_to_change: int, new_level: str) -> bool:
    """
    Allows an admin user to change the privilege level of another user.

    Args:
        acting_user_id (int): ID of the user performing the action.
        user_id_to_change (int): ID of the target user whose privilege is to be changed.
        new_level (str): Desired privilege level ('normal', 'moderator', or 'admin').

    Returns:
        bool: True if the privilege was changed successfully, False otherwise.
    """
    # Validate input types
    if not all(isinstance(arg, int) for arg in (acting_user_id, user_id_to_change)):
        return False
    if not isinstance(new_level, str):
        return False

    # Normalise privilege level string
    new_level = new_level.strip().lower()

    # Define allowed levels
    ALLOWED_LEVELS = {"normal", "moderator", "admin"}

    if new_level not in ALLOWED_LEVELS:
        return False

    # Retrieve acting user and target user
    acting_user = USERS.get(acting_user_id)
    target_user = USERS.get(user_id_to_change)

    # Ensure both users exist
    if acting_user is None or target_user is None:
        return False

    # Ensure the acting user has admin privileges
    if acting_user.get("role") != "admin":
        return False

    # Prevent privilege escalation or downgrade of the acting user themselves
    if acting_user_id == user_id_to_change:
        # Admins may not alter their own privilege level
        return False

    # Update the target user's privilege level
    target_user["privilege_level"] = new_level

    # Optionally, update the role field to reflect the new privilege
    target_user["role"] = new_level

    return True