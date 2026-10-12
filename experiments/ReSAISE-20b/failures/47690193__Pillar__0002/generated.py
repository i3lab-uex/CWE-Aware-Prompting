# -*- coding: utf-8 -*-
"""
Implementation of control_project_permissions with proper access checks.
"""

from typing import Dict, List

# Example data structures (replace with real ones in production)
PROJECTS: Dict[int, Dict[str, object]] = {
    # project_id : { 'owner_id': int, 'members': List[int] }
}
USERS: Dict[int, str] = {
    # user_id : 'admin' | 'user'
}


def control_project_permissions(
    executing_user_id: int,
    prjct_id: int,
    act_type: str,
    tgt_user_id: int
) -> bool:
    """
    Add or remove a user from a project, respecting ownership and admin rights.

    Parameters
    ----------
    executing_user_id : int
        ID of the user performing the operation.
    prjct_id : int
        Project to modify.
    act_type : str
        Either 'add' or 'remove'.
    tgt_user_id : int
        Target user to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """

    # Validate input types and values
    if not isinstance(executing_user_id, int) or not isinstance(prjct_id, int) \
       or not isinstance(tgt_user_id, int):
        return False

    if act_type not in {"add", "remove"}:
        return False

    # Check that the executing user exists
    executor_role = USERS.get(executing_user_id)
    if executor_role not in {"admin", "user"}:
        return False

    # Retrieve project details
    project = PROJECTS.get(prjct_id)
    if not isinstance(project, dict):
        return False

    owner_id = project.get("owner_id")
    members: List[int] = project.get("members", [])

    # Verify that the target user exists
    if tgt_user_id not in USERS:
        return False

    # Access control: admins can act on any project
    if executor_role == "admin":
        authorized = True
    else:
        # Non-admins must be the owner of the project
        authorized = (executing_user_id == owner_id)

    if not authorized:
        return False

    # Perform the action
    if act_type == "add":
        if tgt_user_id not in members:
            members.append(tgt_user_id)
    else:  # act_type == "remove"
        if tgt_user_id in members:
            members.remove(tgt_user_id)

    # Update the project
    project["members"] = members
    PROJECTS[prjct_id] = project

    return True