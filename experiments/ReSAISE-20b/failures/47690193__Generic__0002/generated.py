# -*- coding: utf-8 -*-

from typing import Dict, List

# Example data structures; in real usage these would be populated elsewhere
PROJECTS: Dict[int, Dict[str, object]] = {}
USERS: Dict[int, str] = {}

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
        ID of the user performing the operation.
    prjct_id : int
        ID of the target project.
    act_type : str
        Either 'add' or 'remove'.
    tgt_user_id : int
        ID of the user to be added/removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate act_type
    if act_type not in {"add", "remove"}:
        return False

    # Retrieve project; fail if it doesn't exist
    project = PROJECTS.get(prjct_id)
    if not project:
        return False

    # Retrieve role of executing user; fail if unknown
    role = USERS.get(executing_user_id)
    if role is None:
        return False

    # Determine permission
    if role == "admin":
        has_permission = True
    else:
        # For normal users, only the owner may modify membership
        has_permission = (project.get("owner_id") == executing_user_id)

    if not has_permission:
        return False

    # Perform the action
    members: List[int] = project.setdefault("members", [])

    if act_type == "add":
        # Avoid duplicates
        if tgt_user_id not in members:
            members.append(tgt_user_id)
    else:  # act_type == "remove"
        if tgt_user_id in members:
            members.remove(tgt_user_id)

    return True