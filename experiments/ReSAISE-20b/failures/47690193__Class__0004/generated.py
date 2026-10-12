# -*- coding: utf-8 -*-
"""
Project permission management module.

This module provides a single function `control_project_permissions` that
allows an executing user to add or remove members from a project.
Admins can perform any operation on any project, while regular users
may only modify projects they own.

The implementation follows the principle of least privilege and performs
explicit authorization checks to avoid CWE‑862: Missing Authorization.
"""

from typing import Dict, List

# Example data structures; in a real system these would be loaded from
# persistent storage or an ORM. They are kept simple for clarity.
PROJECTS: Dict[int, Dict] = {
    # project_id : { 'owner_id': int, 'members': List[int] }
}

USERS: Dict[int, str] = {
    # user_id : role ('admin' or 'user')
}

def control_project_permissions(
        executing_user_id: int,
        prjct_id: int,
        act_type: str,
        tgt_user_id: int
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    executing_user_id : int
        The ID of the user performing the action.
    prjct_id : int
        The project identifier to modify.
    act_type : str
        Either 'add' or 'remove'.
    tgt_user_id : int
        The user ID of the target member to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """

    # 1. Validate act_type
    if act_type not in {"add", "remove"}:
        return False

    # 2. Retrieve executing user role
    exec_role = USERS.get(executing_user_id)
    if exec_role is None:
        # Unknown user
        return False

    # 3. Retrieve project details
    project = PROJECTS.get(prjct_id)
    if project is None:
        # Project does not exist
        return False

    # 4. Authorization check
    if exec_role != "admin":
        # Non-admins can only modify projects they own
        if project.get("owner_id") != executing_user_id:
            return False

    # 5. Ensure target user exists
    if tgt_user_id not in USERS:
        return False

    members: List[int] = project.setdefault("members", [])

    if act_type == "add":
        if tgt_user_id in members:
            # Already a member; no change needed
            return True
        members.append(tgt_user_id)
    else:  # act_type == "remove"
        if tgt_user_id not in members:
            # User is not a member; nothing to remove
            return True
        members.remove(tgt_user_id)

    # 6. Persist changes (here we just modify the in-memory dict)
    PROJECTS[prjct_id]["members"] = members

    return True