from typing import Dict, List

# Sample data structures; in a real application these would come from a database
PROJECTS: Dict[int, Dict[str, object]] = {
    # project_id: {"owner_id": int, "members": List[int]}
}

USERS: Dict[int, str] = {
    # user_id: "admin" or "user"
}


def update_project_members(
    acting_user_id: int,
    project_identifier: int,
    modification: str,
    user_to_update_id: int
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the operation.
    project_identifier : int
        ID of the target project.
    modification : str
        Either 'add' or 'remove'.
    user_to_update_id : int
        ID of the member to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate modification type
    if modification not in {"add", "remove"}:
        return False

    # Retrieve project
    project = PROJECTS.get(project_identifier)
    if not project:
        return False

    # Retrieve acting user role
    acting_role = USERS.get(acting_user_id)
    if not acting_role:
        return False

    # Authorization: only project owner or admin can modify
    if acting_user_id != project["owner_id"] and acting_role.lower() != "admin":
        return False

    # Ensure the target user exists
    if user_to_update_id not in USERS:
        return False

    members: List[int] = project.get("members", [])

    if modification == "add":
        # Avoid duplicate entries
        if user_to_update_id in members:
            return False
        members.append(user_to_update_id)
    else:  # modification == "remove"
        if user_to_update_id not in members:
            return False
        members.remove(user_to_update_id)

    # Persist changes back to the project dict
    project["members"] = members
    return True