# -*- coding: utf-8 -*-
"""
Project access management module.

This module provides the `manage_project_access` function which allows
project owners to add or remove members from their project, while users
with the 'admin' role can modify any project. The function guards against
improper access control by ensuring that only authorized users can
perform the requested actions.
"""

from typing import Dict, Any

# Example data structures. In a real application these would be loaded
# from a database or external service.
PROJECTS: Dict[int, Dict[str, Any]] = {
    1: {"owner_id": 10, "members": {20, 30}},
    2: {"owner_id": 11, "members": {21}},
}

USERS: Dict[int, Dict[str, Any]] = {
    10: {"role": "owner"},
    11: {"role": "owner"},
    20: {"role": "member"},
    30: {"role": "member"},
    21: {"role": "member"},
    99: {"role": "admin"},   # admin user
}


def manage_project_access(
    current_user_id: int,
    project_id: int,
    action: str,
    target_user_id: int
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    current_user_id : int
        The ID of the user invoking this function.
    project_id : int
        The ID of the project to modify.
    action : str
        Either 'add' or 'remove'.
    target_user_id : int
        The ID of the user to add or remove.

    Returns
    -------
    bool
        True if the action succeeded, False otherwise.

    Raises
    ------
    ValueError
        If `action` is not one of 'add' or 'remove'.
    KeyError
        If the project or user does not exist.

    Notes
    -----
    - Only a project owner or an admin can perform the operation.
    - Admins can modify any project; owners can only modify their own.
    - The function is idempotent: adding an existing member or removing a
      non‑member returns True without error.
    """
    # Validate action
    if action not in {"add", "remove"}:
        raise ValueError(f"Invalid action: {action!r}. Must be 'add' or 'remove'.")

    # Fetch project and user data
    try:
        project = PROJECTS[project_id]
    except KeyError as exc:
        raise KeyError(f"Project {project_id} not found.") from exc

    try:
        current_user = USERS[current_user_id]
    except KeyError as exc:
        raise KeyError(f"User {current_user_id} not found.") from exc

    # Access control check
    is_admin = current_user.get("role") == "admin"
    is_owner = project["owner_id"] == current_user_id

    if not (is_admin or is_owner):
        # Unauthorized attempt; do not reveal sensitive info
        return False

    # Ensure target user exists to avoid dangling references
    if target_user_id not in USERS:
        raise KeyError(f"Target user {target_user_id} does not exist.")

    members = project.setdefault("members", set())

    if action == "add":
        # Add member id to the set; idempotent
        members.add(target_user_id)
    else:  # action == "remove"
        # Remove member if present; idempotent
        members.discard(target_user_id)

    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    assert manage_project_access(10, 1, "add", 99) is True   # owner adding admin
    assert manage_project_access(99, 1, "remove", 20) is True # admin removing member
    assert manage_project_access(20, 1, "add", 30) is False   # non‑owner/non‑admin
    print("All tests passed.")