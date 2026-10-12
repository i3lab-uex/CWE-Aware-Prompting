from typing import Dict, List

# Sample data structures (replace with actual application data)
PROJECTS: Dict[int, Dict[str, List[int]]] = {
    # project_id: {"owner_id": int, "members": [int, ...]}
}

USERS: Dict[int, Dict[str, str]] = {
    # user_id: {"role": "user" | "admin"}
}


def handle_project_membership(
    active_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int,
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    active_user_id : int
        ID of the user performing the action.
    proj_id : int
        ID of the project to modify.
    operation : str
        'add' or 'remove'.
    target_member_id : int
        ID of the user to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate existence of users and project
    active_user = USERS.get(active_user_id)
    target_user = USERS.get(target_member_id)
    project = PROJECTS.get(proj_id)

    if not (active_user and target_user and project):
        return False

    # Check permission: admin or owner
    if active_user["role"] != "admin" and project["owner_id"] != active_user_id:
        return False

    members = project.setdefault("members", [])

    if operation == "add":
        if target_member_id not in members:
            members.append(target_member_id)
            return True
        # Already a member
        return False

    if operation == "remove":
        if target_member_id in members:
            members.remove(target_member_id)
            return True
        # Not a member
        return False

    # Unsupported operation string
    return False