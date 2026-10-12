from typing import Dict, List

# Example data structures (replace with real data in production)
PROJECTS: Dict[int, Dict[str, List[int]]] = {
    # project_id: {"owner_id": int, "members": [int, ...]}
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
    Add or remove a member from a project.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the action.
    prjt_id : int
        ID of the project to modify.
    member_action : str
        'add' or 'remove'.
    target_member_id : int
        ID of the member to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate project existence
    project = PROJECTS.get(prjt_id)
    if not project:
        return False

    # Validate acting user role
    acting_role = USERS.get(acting_user_id)
    if not acting_role:
        return False

    # Only admins or the project owner can modify membership
    if acting_role != "admin" and acting_user_id != project["owner_id"]:
        return False

    members = project.get("members", [])

    if member_action == "add":
        # Avoid duplicates
        if target_member_id in members:
            return False
        members.append(target_member_id)
        project["members"] = members
        return True

    if member_action == "remove":
        # Ensure the member exists before removing
        if target_member_id not in members:
            return False
        members.remove(target_member_id)
        project["members"] = members
        return True

    # Invalid action string
    return False