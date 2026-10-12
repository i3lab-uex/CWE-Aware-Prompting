# -*- coding: utf-8 -*-
"""
Project access control module.

The function `project_access_control` ensures that only authorized users
(either the project owner or an admin) can add or remove members from a
project. It performs comprehensive validation to guard against
CWE-862 (Missing Authorization) and other potential security issues.
"""

from typing import Dict, List

# Example data structures; in a real application these would come from
# a database or external service.
PROJECTS: Dict[int, Dict[str, object]] = {
    # project_id : { 'owner_id': int, 'members': List[int] }
}

USERS: Dict[int, str] = {
    # user_id : 'admin' | 'user'
}

def project_access_control(
    active_user_id: int,
    prj_id: int,
    action_type: str,
    member_user_id: int
) -> bool:
    """
    Add or remove a member from a project if the active user is authorized.

    Parameters
    ----------
    active_user_id : int
        ID of the user performing the action.
    prj_id : int
        Target project ID.
    action_type : str
        Either 'add' or 'remove'.
    member_user_id : int
        User ID of the member to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate input types early to avoid accidental injection of bad data
    if not isinstance(active_user_id, int) or not isinstance(prj_id, int) \
       or not isinstance(action_type, str) or not isinstance(member_user_id, int):
        return False

    # Normalise action_type to lower case for robustness
    action = action_type.strip().lower()
    if action not in {"add", "remove"}:
        return False

    # Ensure the active user exists
    role = USERS.get(active_user_id)
    if role is None:
        return False

    # Ensure the target project exists
    project = PROJECTS.get(prj_id)
    if project is None:
        return False

    # Authorization check: allow only admins or the owner
    if role != "admin" and active_user_id != project.get("owner_id"):
        return False

    # Ensure the member user exists (optional but good practice)
    if member_user_id not in USERS:
        return False

    members: List[int] = project.setdefault("members", [])

    if action == "add":
        # Avoid duplicates
        if member_user_id in members:
            return False
        members.append(member_user_id)
    else:  # action == "remove"
        if member_user_id not in members:
            return False
        members.remove(member_user_id)

    # Successful operation
    return True