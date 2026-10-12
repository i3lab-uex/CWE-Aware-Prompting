from typing import Dict, List

# Sample data structures (would normally be populated elsewhere)
PROJECTS: Dict[int, Dict[str, object]] = {}
USERS: Dict[int, str] = {}

def project_access_control(
    active_user_id: int,
    prj_id: int,
    action_type: str,
    member_user_id: int
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    active_user_id : int
        ID of the user performing the action.
    prj_id : int
        ID of the project to update.
    action_type : str
        Either 'add' or 'remove'.
    member_user_id : int
        ID of the user to add or remove.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Validate action_type early to avoid unintended operations
    if action_type not in {"add", "remove"}:
        return False

    # Ensure the project exists
    project = PROJECTS.get(prj_id)
    if not project:
        return False

    # Retrieve the role of the active user
    active_role = USERS.get(active_user_id)
    if not active_role:
        return False

    # Determine authorization
    is_admin = active_role == "admin"
    is_owner = project.get("owner_id") == active_user_id

    if not (is_admin or is_owner):
        return False  # Unauthorized user

    members: List[int] = project.get("members", [])

    if action_type == "add":
        # Avoid duplicate entries
        if member_user_id in members:
            return False  # Already a member
        members.append(member_user_id)
    else:  # action_type == "remove"
        if member_user_id not in members:
            return False  # Not a member
        members.remove(member_user_id)

    # Persist the updated list back to the project
    project["members"] = members
    return True