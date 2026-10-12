# ------------------------------------------------------------
# User privilege management module
# ------------------------------------------------------------

from typing import Dict

# Sample USERS dictionary. In a real system this would be loaded from a database or secure storage.
USERS: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice",   "role": "admin"},
    2: {"name": "Bob",     "role": "moderator"},
    3: {"name": "Charlie", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}

def alter_user_permissions(acting_user_id: int,
                           targeted_user_id: int,
                           new_privilege_level: str) -> bool:
    """
    Change the privilege level of a user.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to change privileges.
    targeted_user_id : int
        ID of the user whose privilege is being altered.
    new_privilege_level : str
        Desired privilege level for the targeted user.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate privilege level
    if new_privilege_level not in ALLOWED_PRIVILEGES:
        return False

    # Ensure both users exist
    acting_user = USERS.get(acting_user_id)
    targeted_user = USERS.get(targeted_user_id)

    if not acting_user or not targeted_user:
        return False

    # Only admins can change privileges
    if acting_user.get("role") != "admin":
        return False

    # Prevent self‑downgrading (optional but recommended)
    if acting_user_id == targeted_user_id:
        return False

    # Apply the new privilege
    try:
        USERS[targeted_user_id]["role"] = new_privilege_level
        return True
    except Exception:
        # In case the USERS structure changes unexpectedly
        return False

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(alter_user_permissions(1, 3, "moderator"))  # Expected: True
#     print(USERS[3]["role"])                          # Expected: "moderator"