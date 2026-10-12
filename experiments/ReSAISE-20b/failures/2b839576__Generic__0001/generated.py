# project_access_control.py

from typing import Dict, List

# Sample data structures (in real use these would be populated elsewhere)
PROJECTS: Dict[int, Dict[str, any]] = {
    # Example:
    # 1: {"owner_id": 10, "members": [20, 30]},
}
USERS: Dict[int, str] = {
    # Example:
    # 10: "admin",
    # 20: "user",
}

def project_access_control(
    active_user_id: int,
    prj_id: int,
    action_type: str,
    member_user_id: int
) -> bool:
    """
    Allow project owners to add/remove members from their projects.
    Admins can manage any project without restrictions.

    Parameters
    ----------
    active_user_id : int
        The ID of the user performing the action.
    prj_id : int
        The project to modify.
    action_type : str
        Either 'add' or 'remove'.
    member_user_id : int
        The user ID of the target member.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Validate action_type
    if action_type not in {"add", "remove"}:
        return False

    # Verify project exists
    project = PROJECTS.get(prj_id)
    if not project:
        return False

    # Check permissions
    active_role = USERS.get(active_user_id)
    if active_role is None:
        return False  # Unknown user

    if active_role != "admin" and active_user_id != project.get("owner_id"):
        return False  # Not allowed

    members: List[int] = project.setdefault("members", [])

    if action_type == "add":
        # Prevent duplicate membership
        if member_user_id in members:
            return False
        members.append(member_user_id)
    else:  # remove
        if member_user_id not in members:
            return False
        members.remove(member_user_id)

    # Update the project record
    PROJECTS[prj_id]["members"] = members
    return True