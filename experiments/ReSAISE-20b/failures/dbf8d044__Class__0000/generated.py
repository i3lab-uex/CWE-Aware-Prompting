# -*- coding: utf-8 -*-
"""
Module implementing user privilege update with proper authorization checks.
"""

from typing import Dict

# Example USERS dictionary. In a real system this would come from a database.
USERS: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "moderator"},
    3: {"name": "Carol", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def update_user_privilege(actor_id: int, recipient_id: int, updated_privilege: str) -> bool:
    """
    Update the privilege level of a user account.

    Parameters
    ----------
    actor_id : int
        ID of the user performing the operation.
    recipient_id : int
        ID of the target user whose privilege is to be changed.
    updated_privilege : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege change was applied, False otherwise.
    """
    # 1. Validate existence of actor and recipient
    actor = USERS.get(actor_id)
    recipient = USERS.get(recipient_id)

    if actor is None or recipient is None:
        return False

    # 2. Only admins can change privileges
    if actor.get("role") != "admin":
        return False

    # 3. Prevent admins from demoting themselves
    if actor_id == recipient_id and updated_privilege != "admin":
        return False

    # 4. Validate the requested privilege level
    if updated_privilege not in ALLOWED_PRIVILEGES:
        return False

    # 5. Apply the change
    recipient["role"] = updated_privilege
    return True


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(update_user_privilege(1, 3, "moderator"))  # Expected: True
#     print(update_user_privilege(2, 3, "admin"))      # Expected: False (Bob is not admin)
#     print(update_user_privilege(1, 1, "normal"))     # Expected: False (cannot demote self)