from typing import Dict, List

# Example data structures (replace with actual persistence in production)
PROJECTS: Dict[int, Dict[str, object]] = {
    # proj_id : {"owner_id": int, "members": List[int]}
}

USERS: Dict[int, str] = {
    # user_id : "admin" or "user"
}

def handle_project_membership(
    active_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    active_user_id : int
        The ID of the user performing the action.
    proj_id : int
        The ID of the project to modify.
    operation : str
        Either 'add' or 'remove'.
    target_member_id : int
        The ID of the user to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate project existence
    proj = PROJECTS.get(proj_id)
    if not proj:
        return False

    # Validate operation
    if operation not in {"add", "remove"}:
        return False

    # Access control: admin or project owner
    user_role = USERS.get(active_user_id)
    if user_role != "admin" and active_user_id != proj["owner_id"]:
        return False

    members: List[int] = proj.get("members", [])

    if operation == "add":
        # Avoid duplicate membership
        if target_member_id in members:
            return False
        members.append(target_member_id)
    else:  # operation == "remove"
        if target_member_id not in members:
            return False
        members.remove(target_member_id)

    # Persist changes (in this simple example we just modify the dict)
    proj["members"] = members
    return True