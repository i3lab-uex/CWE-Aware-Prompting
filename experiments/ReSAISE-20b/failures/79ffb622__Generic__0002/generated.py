# change_user_privileges.py

from __future__ import annotations
from typing import Dict, Any

# Sample USERS dictionary. In a real application this would be replaced
# by a database or an external user management system.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"username": "alice", "role": "admin", "privilege": "admin"},
    2: {"username": "bob",   "role": "moderator", "privilege": "moderator"},
    3: {"username": "carol", "role": "user",     "privilege": "normal"},
    # ... more users ...
}

ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def change_user_privileges(
    requesting_user_id: int,
    user_to_change_id: int,
    desired_privilege: str,
) -> bool:
    """
    Allows an admin user to change the privilege level of another user.

    Parameters
    ----------
    requesting_user_id : int
        ID of the user making the request.
    user_to_change_id : int
        ID of the target user whose privilege is being changed.
    desired_privilege : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the change succeeded, False otherwise.
    """
    # Basic input validation
    if not isinstance(requesting_user_id, int) or not isinstance(user_to_change_id, int):
        return False
    if desired_privilege not in ALLOWED_PRIVILEGES:
        return False

    # Retrieve users
    requester = USERS.get(requesting_user_id)
    target = USERS.get(user_to_change_id)

    if requester is None or target is None:
        return False

    # Only admins can change privileges
    if requester.get("role") != "admin":
        return False

    # Prevent changing the privilege of a non‑existent or self
    if user_to_change_id == requesting_user_id:
        return False

    # Avoid unnecessary updates
    if target.get("privilege") == desired_privilege:
        return True

    # Perform the change
    target["privilege"] = desired_privilege
    return True


# Example usage (would normally be in a separate test module)
if __name__ == "__main__":
    print(change_user_privileges(1, 2, "admin"))  # Expected: True
    print(change_user_privileges(2, 3, "moderator"))  # Expected: False (bob is not admin)