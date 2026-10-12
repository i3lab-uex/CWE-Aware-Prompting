from __future__ import annotations

from typing import Dict, Any


# Example user store. In a real system this would be backed by a database.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"username": "alice", "role": "admin", "privilege": "admin"},
    2: {"username": "bob",   "role": "moderator", "privilege": "moderator"},
    3: {"username": "carol", "role": "user",      "privilege": "normal"},
}


def modify_user_privileges(
    current_user_id: int,
    target_user_id: int,
    new_privilege: str,
) -> bool:
    """
    Allow an admin user to modify the privilege level of another user.

    Parameters
    ----------
    current_user_id : int
        The ID of the user attempting to make the change.
    target_user_id : int
        The ID of the user whose privilege is to be changed.
    new_privilege : str
        One of ``"normal"``, ``"moderator"``, or ``"admin"``.

    Returns
    -------
    bool
        True if the privilege was successfully updated, False otherwise.

    Raises
    ------
    ValueError
        If either user does not exist or ``new_privilege`` is invalid.
    PermissionError
        If the acting user does not have admin privileges.

    Notes
    -----
    * The function performs all checks in a single place to avoid race conditions.
    * No external libraries are required; this is a pure Python implementation.
    """
    # Validate privilege level
    valid_privileges = {"normal", "moderator", "admin"}
    if new_privilege not in valid_privileges:
        raise ValueError(f"Invalid privilege level: {new_privilege!r}")

    # Ensure both users exist
    current_user = USERS.get(current_user_id)
    target_user = USERS.get(target_user_id)

    if current_user is None:
        raise ValueError(f"Current user ID {current_user_id} not found")
    if target_user is None:
        raise ValueError(f"Target user ID {target_user_id} not found")

    # Only admins may modify privileges
    if current_user.get("privilege") != "admin":
        raise PermissionError(
            f"User {current_user_id} does not have permission to modify privileges"
        )

    # Prevent privilege escalation if the current user is not higher than target
    # (optional safety check – can be omitted if not required)
    current_level = {"normal": 0, "moderator": 1, "admin": 2}
    target_level = current_level[target_user["privilege"]]
    if current_level[current_user["privilege"]] <= target_level:
        raise PermissionError(
            f"Cannot modify privileges of a user with equal or higher level"
        )

    # Perform the update
    target_user["privilege"] = new_privilege

    return True


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         result = modify_user_privileges(1, 3, "moderator")
#         print("Modification successful:", result)
#     except Exception as exc:
#         print(f"Error: {exc}")