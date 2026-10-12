# -*- coding: utf-8 -*-
"""
Implementation of project permission control with proper access checks.
"""

from typing import Dict, List

# Example data structures. In a real system these would be loaded from a database.
USERS: Dict[int, str] = {
    1: "admin",
    2: "user",
    3: "user",
}

PROJECTS: Dict[int, Dict[str, object]] = {
    101: {"owner_id": 2, "members": [2, 3]},
    102: {"owner_id": 3, "members": [3]},
}


def control_project_permissions(
    executing_user_id: int,
    prjct_id: int,
    act_type: str,
    tgt_user_id: int,
) -> bool:
    """
    Adds or removes a user from a project's member list.

    Parameters
    ----------
    executing_user_id : int
        ID of the user performing the operation.
    prjct_id : int
        ID of the target project.
    act_type : str
        Either 'add' or 'remove'.
    tgt_user_id : int
        ID of the user to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate act_type
    if act_type not in {"add", "remove"}:
        return False

    # Verify executing user exists
    exec_role = USERS.get(executing_user_id)
    if exec_role is None:
        return False

    # Verify target user exists
    if tgt_user_id not in USERS:
        return False

    # Verify project exists
    project = PROJECTS.get(prjct_id)
    if not project:
        return False

    # Access control: admins can modify any project
    if exec_role == "admin":
        has_permission = True
    else:
        # Regular users can modify only if they own the project
        has_permission = executing_user_id == project["owner_id"]

    if not has_permission:
        return False

    members: List[int] = project["members"]

    if act_type == "add":
        if tgt_user_id in members:
            # User already a member; nothing to do
            return True
        members.append(tgt_user_id)
    else:  # act_type == "remove"
        if tgt_user_id not in members:
            # User not a member; nothing to do
            return True
        members.remove(tgt_user_id)

    # Operation succeeded
    return True

# Example usage:
if __name__ == "__main__":
    # Admin adding a user
    print(control_project_permissions(1, 101, "add", 4))  # False, user 4 doesn't exist

    # Owner adding a member
    print(control_project_permissions(2, 101, "add", 3))  # True

    # Owner removing a member
    print(control_project_permissions(2, 101, "remove", 3))  # True

    # Unauthorized user attempting to modify
    print(control_project_permissions(3, 101, "add", 2))  # False