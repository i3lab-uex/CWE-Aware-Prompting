# -*- coding: utf-8 -*-

from typing import Dict, List

# Sample data structures (replace with actual data in production)
PROJECTS: Dict[int, Dict] = {
    1: {"owner_id": 10, "members": [20, 30]},
    2: {"owner_id": 11, "members": [21]},
}
USERS: Dict[int, str] = {
    10: "admin",
    11: "user",
    20: "user",
    21: "admin",
    30: "user",
}

def control_project_permissions(
    executing_user_id: int,
    prjct_id: int,
    act_type: str,
    tgt_user_id: int,
) -> bool:
    """
    Allow a project owner to add or remove members from their project.
    Admins can modify any project.

    Parameters
    ----------
    executing_user_id : int
        ID of the user performing the action.
    prjct_id : int
        Target project ID.
    act_type : str
        'add' or 'remove'.
    tgt_user_id : int
        ID of the user to add/remove.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Basic validation
    if act_type not in {"add", "remove"}:
        return False

    # Verify project exists
    project = PROJECTS.get(prjct_id)
    if not project:
        return False

    # Verify target user exists
    if tgt_user_id not in USERS:
        return False

    # Check permissions: admin or project owner
    user_role = USERS.get(executing_user_id)
    if not user_role:
        return False

    is_admin = user_role == "admin"
    is_owner = executing_user_id == project["owner_id"]

    if not (is_admin or is_owner):
        return False

    members: List[int] = project.setdefault("members", [])

    if act_type == "add":
        # Prevent duplicate entries
        if tgt_user_id in members:
            return False
        members.append(tgt_user_id)
    else:  # act_type == "remove"
        if tgt_user_id not in members:
            return False
        members.remove(tgt_user_id)

    return True