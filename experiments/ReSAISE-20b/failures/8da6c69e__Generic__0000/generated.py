# Project membership management module

from typing import Dict, List

# Example data structures (replace with actual application data)
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
        The ID of the user performing the action.
    prjt_id : int
        The project whose membership is being modified.
    member_action : str
        Either 'add' or 'remove'.
    target_member_id : int
        The user ID of the member to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic validation of inputs
    if member_action not in {"add", "remove"}:
        return False

    # Check that the project exists
    project = PROJECTS.get(prjt_id)
    if not project:
        return False

    # Verify that the target member exists in USERS
    if target_member_id not in USERS:
        return False

    # Determine permission: admin can modify any project
    acting_role = USERS.get(acting_user_id)
    if acting_role == "admin":
        has_permission = True
    else:
        # Non-admins can only modify projects they own
        has_permission = project.get("owner_id") == acting_user_id

    if not has_permission:
        return False

    members: List[int] = project.setdefault("members", [])

    if member_action == "add":
        # Add only if not already a member
        if target_member_id in members:
            return False  # Already a member
        members.append(target_member_id)
    else:  # remove
        if target_member_id not in members:
            return False  # Not a member to remove
        members.remove(target_member_id)

    return True