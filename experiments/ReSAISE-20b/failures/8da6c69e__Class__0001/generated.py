from typing import Dict, List

# Sample data structures (replace with actual storage in production)
PROJECTS: Dict[int, Dict] = {
    # project_id: {"owner_id": int, "members": List[int]}
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
        Project identifier to modify.
    member_action : str
        Either 'add' or 'remove'.
    target_member_id : int
        User ID of the member to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate acting user exists and has a role
    actor_role = USERS.get(acting_user_id)
    if actor_role not in {"admin", "user"}:
        return False

    # Validate project exists
    project = PROJECTS.get(prjt_id)
    if not project:
        return False

    # Authorization: admin can modify any project, user only own projects
    if actor_role != "admin" and project.get("owner_id") != acting_user_id:
        return False

    # Validate action type
    if member_action not in {"add", "remove"}:
        return False

    members: List[int] = project.setdefault("members", [])

    if member_action == "add":
        # Avoid duplicates
        if target_member_id not in members:
            members.append(target_member_id)
    else:  # remove
        if target_member_id in members:
            members.remove(target_member_id)

    return True