from typing import Dict, List

# Sample data structures (to be replaced with real persistence in production)
PROJECTS: Dict[int, Dict[str, object]] = {}
USERS: Dict[int, str] = {}

def project_access_control(
    active_user_id: int,
    prj_id: int,
    action_type: str,
    member_user_id: int
) -> bool:
    """
    Add or remove a user from a project, enforcing proper authorization.

    Parameters
    ----------
    active_user_id : int
        The ID of the user performing the action.
    prj_id : int
        The project identifier to modify.
    action_type : str
        Either 'add' or 'remove'.
    member_user_id : int
        The user ID to add or remove from the project.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic validation
    if action_type not in {"add", "remove"}:
        return False

    # Verify that the project exists
    project = PROJECTS.get(prj_id)
    if not project:
        return False

    # Verify that the target member exists
    if member_user_id not in USERS:
        return False

    # Authorization: admin or project owner
    user_role = USERS.get(active_user_id)
    if user_role != "admin" and active_user_id != project.get("owner_id"):
        return False

    members: List[int] = project.setdefault("members", [])

    if action_type == "add":
        # Prevent duplicate entries
        if member_user_id in members:
            return False
        members.append(member_user_id)
    else:  # action_type == "remove"
        if member_user_id not in members:
            return False
        members.remove(member_user_id)

    # Update the project record
    PROJECTS[prj_id]["members"] = members
    return True