# -*- coding: utf-8 -*-
"""
Implementation of project membership control with proper authorization checks.
"""

from typing import Dict, List

# Example data structures. In a real application these would be populated from
# persistent storage or an ORM.
PROJECTS: Dict[int, Dict[str, any]] = {
    # project_id : { "owner_id": int, "members": List[int] }
}

USERS: Dict[int, str] = {
    # user_id : "admin" | "user"
}


def control_project_permissions(
    executing_user_id: int,
    prjct_id: int,
    act_type: str,
    tgt_user_id: int,
) -> bool:
    """
    Add or remove a user from a project, respecting authorization rules.

    Parameters
    ----------
    executing_user_id : int
        The ID of the user performing the action.
    prjct_id : int
        The ID of the project to modify.
    act_type : str
        Either 'add' or 'remove'.
    tgt_user_id : int
        The ID of the target user to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic validation of act_type
    if act_type not in {"add", "remove"}:
        return False

    # Verify that the project exists
    project = PROJECTS.get(prjct_id)
    if not project:
        return False

    # Authorization: admins can act on any project; owners can act only on their own
    user_role = USERS.get(executing_user_id)
    if not user_role:
        return False

    is_admin = user_role == "admin"
    is_owner = project.get("owner_id") == executing_user_id

    if not (is_admin or is_owner):
        return False  # CWE-862 mitigation: missing authorization

    members = project.get("members")
    if members is None:
        return False  # corrupted data

    if act_type == "add":
        # Avoid duplicate entries
        if tgt_user_id in members:
            return False
        members.append(tgt_user_id)
    else:  # act_type == "remove"
        if tgt_user_id not in members:
            return False
        members.remove(tgt_user_id)

    # If we reach here, the operation succeeded
    return True