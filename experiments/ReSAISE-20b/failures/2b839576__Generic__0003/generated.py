# Project access control implementation

from typing import Dict, List

# Example data structures (should be defined elsewhere in the application)
PROJECTS: Dict[int, Dict] = {
    # project_id: {"owner_id": int, "members": List[int]}
}
USERS: Dict[int, str] = {
    # user_id: "admin" or "user"
}


def project_access_control(
    active_user_id: int,
    prj_id: int,
    action_type: str,
    member_user_id: int
) -> bool:
    """
    Adds or removes a user from a project's member list.

    Parameters
    ----------
    active_user_id : int
        ID of the user performing the operation.
    prj_id : int
        ID of the project to be updated.
    action_type : str
        Either 'add' or 'remove'.
    member_user_id : int
        ID of the user to add or remove.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Validate action_type
    if action_type not in {"add", "remove"}:
        return False

    # Ensure project exists
    project = PROJECTS.get(prj_id)
    if not project:
        return False

    # Ensure target member exists in USERS
    if member_user_id not in USERS:
        return False

    # Permission check: admins can always modify, users only if they own the project
    user_role = USERS.get(active_user_id)
    if user_role != "admin" and active_user_id != project["owner_id"]:
        return False

    members: List[int] = project.get("members", [])

    if action_type == "add":
        # Avoid duplicate additions
        if member_user_id in members:
            return False  # already a member
        members.append(member_user_id)
    else:  # action_type == "remove"
        if member_user_id not in members:
            return False  # cannot remove non-member
        members.remove(member_user_id)

    # Update the project's member list
    project["members"] = members
    return True