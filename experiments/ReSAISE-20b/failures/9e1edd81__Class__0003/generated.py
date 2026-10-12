# handle_project_membership.py

from typing import Dict, List


# Example data structures (replace with real ones in production)
PROJECTS: Dict[int, Dict[str, List[int]]] = {
    # project_id : {"owner_id": int, "members": [int, ...]}
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
        ID of the user performing the operation.
    proj_id : int
        Project to be modified.
    operation : str
        Either 'add' or 'remove'.
    target_member_id : int
        ID of the user to add/remove.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Validate operation
    if operation not in {"add", "remove"}:
        return False

    # Check that the active user exists
    role = USERS.get(active_user_id)
    if role is None:
        return False

    # Retrieve the project
    project = PROJECTS.get(proj_id)
    if project is None:
        return False

    # Authorization: only admins or the owner can modify membership
    if role != "admin" and project["owner_id"] != active_user_id:
        return False

    members: List[int] = project.get("members", [])

    if operation == "add":
        # Avoid duplicate members
        if target_member_id in members:
            return False
        members.append(target_member_id)
    else:  # operation == "remove"
        if target_member_id not in members:
            return False
        members.remove(target_member_id)

    # Update the project's member list
    project["members"] = members
    return True