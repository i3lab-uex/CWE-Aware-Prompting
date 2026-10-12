# project_access_control.py

from typing import Dict, List

# Sample data structures. In real usage these would be populated elsewhere.
PROJECTS: Dict[int, Dict[str, object]] = {
    # project_id : {'owner_id': int, 'members': List[int]}
}

USERS: Dict[int, str] = {
    # user_id : 'admin' or 'user'
}


def project_access_control(
    active_user_id: int,
    prj_id: int,
    action_type: str,
    member_user_id: int
) -> bool:
    """
    Add or remove a user from a project's member list.

    Args:
        active_user_id: The ID of the user performing the operation.
        prj_id: The project to modify.
        action_type: Either 'add' or 'remove'.
        member_user_id: The target user to add or remove.

    Returns:
        True if the operation succeeded, False otherwise.
    """
    # Validate input
    if action_type not in {"add", "remove"}:
        return False

    # Ensure the target project exists
    project = PROJECTS.get(prj_id)
    if not project:
        return False

    # Ensure the target member exists
    if member_user_id not in USERS:
        return False

    # Determine permissions
    active_role = USERS.get(active_user_id)
    if not active_role:
        return False

    is_admin = active_role == "admin"
    is_owner = project.get("owner_id") == active_user_id

    # Only admins or the owner can modify members
    if not (is_admin or is_owner):
        return False

    members: List[int] = project.setdefault("members", [])

    if action_type == "add":
        # Avoid duplicate entries
        if member_user_id in members:
            return False
        members.append(member_user_id)
    else:  # action_type == "remove"
        if member_user_id not in members:
            return False
        members.remove(member_user_id)

    return True