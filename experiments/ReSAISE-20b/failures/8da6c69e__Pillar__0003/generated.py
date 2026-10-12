# SPDX-License-Identifier: MIT
"""
Project membership management module.

This module implements the `handle_project_membership` function which allows a user
to add or remove members from a project.  Admin users can modify any project,
while regular users may only modify projects they own.

Security Note:
- The function explicitly checks that the acting user is authorized before
  performing any modifications, mitigating CWE‑284 (Improper Access Control).
- All inputs are validated for type and value before use.
"""

from typing import Dict, List

# Example data structures. In a real application these would be
# backed by a database or another persistent store.
PROJECTS: Dict[int, Dict[str, object]] = {
    # project_id: { 'owner_id': int, 'members': List[int] }
}

USERS: Dict[int, str] = {
    # user_id: 'admin' | 'user'
}


def handle_project_membership(
    acting_user_id: int,
    prjt_id: int,
    member_action: str,
    target_member_id: int
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the action.
    prjt_id : int
        ID of the project to modify.
    member_action : str
        Either 'add' or 'remove'.
    target_member_id : int
        ID of the user to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate acting_user_id exists and has a role
    if not isinstance(acting_user_id, int):
        return False
    acting_role = USERS.get(acting_user_id)
    if acting_role not in {"admin", "user"}:
        return False

    # Validate project exists
    if not isinstance(prjt_id, int):
        return False
    project = PROJECTS.get(prjt_id)
    if project is None:
        return False

    # Validate target_member_id exists
    if not isinstance(target_member_id, int):
        return False
    if target_member_id not in USERS:
        return False

    # Validate member_action
    if member_action not in {"add", "remove"}:
        return False

    # Authorization check
    if acting_role != "admin":
        # Regular users may only modify projects they own
        if project.get("owner_id") != acting_user_id:
            return False

    members: List[int] = project.setdefault("members", [])

    if member_action == "add":
        # Avoid duplicate entries
        if target_member_id in members:
            return False
        members.append(target_member_id)
    else:  # member_action == "remove"
        if target_member_id not in members:
            return False
        members.remove(target_member_id)

    # Operation succeeded
    return True