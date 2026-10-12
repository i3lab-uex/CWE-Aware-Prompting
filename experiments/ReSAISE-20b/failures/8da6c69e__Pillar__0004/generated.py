# handle_project_membership.py

from typing import Dict, List

# Example data structures (replace with actual data sources in production)
PROJECTS: Dict[int, Dict] = {
    # project_id: {"owner_id": int, "members": List[int]}
}

USERS: Dict[int, str] = {
    # user_id: "admin" or "user"
}


def handle_project_membership(
    acting_user_id: int,
    prjt_id: int,
    member_action: str,
    target_member_id: int
) -> bool:
    """
    Allows project owners to add or remove members from their projects.
    Admin users can perform these actions on any project.

    Args:
        acting_user_id (int): ID of the user performing the action.
        prjt_id (int): ID of the project being updated.
        member_action (str): 'add' or 'remove'.
        target_member_id (int): ID of the member to add/remove.

    Returns:
        bool: True if operation succeeded, False otherwise.
    """
    # Validate acting user exists
    if acting_user_id not in USERS:
        return False

    # Retrieve project details; fail if project does not exist
    project = PROJECTS.get(prjt_id)
    if not project:
        return False

    # Check permission: admin or owner
    user_role = USERS[acting_user_id]
    if user_role != "admin" and project.get("owner_id") != acting_user_id:
        return False

    # Validate action type
    if member_action not in {"add", "remove"}:
        return False

    members: List[int] = project.setdefault("members", [])

    if member_action == "add":
        # Avoid duplicate entries
        if target_member_id in members:
            return False
        members.append(target_member_id)
    else:  # remove
        if target_member_id not in members:
            return False
        members.remove(target_member_id)

    # If we reach here, the operation succeeded
    return True