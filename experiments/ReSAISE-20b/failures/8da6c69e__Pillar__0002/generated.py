# SPDX-License-Identifier: MIT

from typing import Dict, List

# Example global dictionaries (in real code these would be loaded from a database)
PROJECTS: Dict[int, Dict[str, any]] = {
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
        'add' or 'remove'.
    target_member_id : int
        ID of the member to add/remove.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Validate action type
    if member_action not in {"add", "remove"}:
        return False

    # Retrieve project
    project = PROJECTS.get(prjt_id)
    if not project:
        return False

    # Retrieve acting user role
    role = USERS.get(acting_user_id)
    if not role:
        return False

    # Permission check: admin can modify any project; owner can modify own
    if role != "admin" and acting_user_id != project.get("owner_id"):
        return False

    # Ensure target member exists
    if target_member_id not in USERS:
        return False

    members: List[int] = project.get("members", [])

    if member_action == "add":
        # Avoid duplicate entries
        if target_member_id in members:
            return False
        members.append(target_member_id)
    else:  # remove
        if target_member_id not in members:
            return False
        members.remove(target_member_id)

    # Update project data (in a real system, persist changes to DB)
    project["members"] = members
    return True