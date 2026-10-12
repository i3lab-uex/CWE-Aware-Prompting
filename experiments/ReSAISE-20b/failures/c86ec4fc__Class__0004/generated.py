# -*- coding: utf-8 -*-
"""
Project participant control module.

This module provides the `control_project_participants` function which
allows a project owner or an administrator to add or remove members from
a project. It performs strict authorization checks to prevent
unauthorized modifications.

Author: ChatGPT
"""

from typing import Dict, Any

# Example data structures (replace with actual database calls in production)
PROJECTS: Dict[int, Dict[str, Any]] = {
    # project_id : { 'owner_id': int, 'members': set[int] }
}

USERS: Dict[int, Dict[str, Any]] = {
    # user_id : { 'role': str }  # role can be 'admin' or 'user'
}


def control_project_participants(
    acting_user_id: int,
    prj_id: int,
    action_type: str,
    target_id: int
) -> bool:
    """
    Add or remove a user from a project's member list.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user performing the action.
    prj_id : int
        The ID of the project to modify.
    action_type : str
        Either 'add' or 'remove'.
    target_id : int
        The ID of the user to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.

    Raises
    ------
    ValueError
        If `action_type` is not one of 'add' or 'remove'.
    KeyError
        If the project, acting user, or target user does not exist.
    """
    # Validate action_type
    if action_type not in {"add", "remove"}:
        raise ValueError("action_type must be 'add' or 'remove'")

    # Retrieve project, acting user and target user
    try:
        project = PROJECTS[prj_id]
        acting_user = USERS[acting_user_id]
        target_user = USERS[target_id]  # existence check only
    except KeyError as exc:
        # Missing project or user
        return False

    # Authorization check: admin or owner
    if acting_user_id != project["owner_id"] and acting_user.get("role") != "admin":
        return False

    members = project.setdefault("members", set())

    if action_type == "add":
        # Prevent adding the owner again or duplicate entries
        if target_id == project["owner_id"]:
            return False
        if target_id in members:
            # Already a member; treat as success
            return True
        members.add(target_id)
    else:  # action_type == "remove"
        if target_id in members:
            members.remove(target_id)
        else:
            # Not a member; treat as success
            return True

    return True


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    # Setup dummy data
    USERS.update({
        1: {"role": "admin"},
        2: {"role": "user"},
        3: {"role": "user"},
    })
    PROJECTS.update({
        100: {"owner_id": 2, "members": {3}},
    })

    # Admin adds user 1 to project 100
    print(control_project_participants(1, 100, "add", 1))  # True

    # Owner removes user 3
    print(control_project_participants(2, 100, "remove", 3))  # True

    # Unauthorized user attempts to add
    print(control_project_participants(3, 100, "add", 2))  # False