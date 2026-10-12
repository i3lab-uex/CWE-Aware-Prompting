import re

# Sample USERS dictionary for illustration; in real usage this would be a persistent store.
USERS = {
    1: {"username": "alice", "role": "admin", "privilege": "admin"},
    2: {"username": "bob",   "role": "user",  "privilege": "normal"},
    3: {"username": "carol", "role": "moderator", "privilege": "moderator"},
    # ... more users
}

# Allowed privilege levels
ALLOWED_LEVELS = {"normal", "moderator", "admin"}

def _is_admin(user_id: int) -> bool:
    """
    Helper to check if a user is an admin.
    """
    user = USERS.get(user_id)
    return bool(user and user.get("role") == "admin")

def modify_privilege_level(acting_user_id: int, user_id_to_change: int, new_level: str) -> bool:
    """
    Allow an admin user to change the privilege level of another user.

    Parameters
    ----------
    acting_user_id : int
        ID of the user making the request.
    user_id_to_change : int
        ID of the target user whose privilege is being changed.
    new_level : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was successfully updated, False otherwise.
    """
    # 1. Verify that acting user exists and is an admin
    if not _is_admin(acting_user_id):
        return False

    # 2. Verify that target user exists
    target_user = USERS.get(user_id_to_change)
    if not target_user:
        return False

    # 3. Validate new_level
    if new_level not in ALLOWED_LEVELS:
        return False

    # 4. Prevent privilege escalation by non-admins (already checked above)

    # 5. Apply the change
    try:
        target_user["privilege"] = new_level
        # Optionally update role to match privilege level for consistency
        if new_level == "admin":
            target_user["role"] = "admin"
        elif new_level == "moderator":
            target_user["role"] = "moderator"
        else:
            target_user["role"] = "user"
    except Exception:
        # Log exception in real implementation
        return False

    return True