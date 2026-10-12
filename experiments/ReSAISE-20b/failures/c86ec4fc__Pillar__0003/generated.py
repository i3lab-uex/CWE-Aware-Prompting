# -*- coding: utf-8 -*-
"""
Project participants control module.

Implements the `control_project_participants` function which allows a project owner
or an administrator to add or remove members from a project.
"""

from __future__ import annotations

# Sample data structures. In a real application these would be loaded from a database.
PROJECTS = {
    1: {"owner_id": 101, "members": {102, 103}},
    2: {"owner_id": 104, "members": {105}},
}

USERS = {
    101: {"role": "admin"},
    102: {"role": "user"},
    103: {"role": "user"},
    104: {"role": "admin"},
    105: {"role": "user"},
}

def control_project_participants(
    acting_user_id: int,
    prj_id: int,
    action_type: str,
    target_id: int,
) -> bool:
    """
    Add or remove a user from a project.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the action.
    prj_id : int
        Project ID whose membership is to be changed.
    action_type : str
        Either 'add' or 'remove'.
    target_id : int
        ID of the user to be added or removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate action type
    if action_type not in {"add", "remove"}:
        return False

    # Ensure project exists
    project = PROJECTS.get(prj_id)
    if not project:
        return False

    # Verify acting user exists
    acting_user = USERS.get(acting_user_id)
    if not acting_user:
        return False

    # Verify target user exists
    if target_id not in USERS:
        return False

    # Check permissions: admin or project owner
    if acting_user["role"] != "admin" and acting_user_id != project["owner_id"]:
        return False

    members = project["members"]

    if action_type == "add":
        # Avoid adding duplicates
        if target_id in members:
            return False
        members.add(target_id)
    else:  # action_type == "remove"
        if target_id not in members:
            return False
        # Prevent owner removal (unless acting user is admin)
        if target_id == project["owner_id"] and acting_user["role"] != "admin":
            return False
        members.remove(target_id)

    return True

# Example usage (uncomment to test):
# print(control_project_participants(101, 1, 'add', 104))  # True
# print(control_project_participants(102, 1, 'remove', 103))  # False