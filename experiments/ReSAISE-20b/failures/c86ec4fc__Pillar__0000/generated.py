from typing import Dict, List

# Example data structures (replace with real data in production)
USERS: Dict[int, str] = {
    1: "admin",
    2: "user",
    3: "user",
    4: "admin",
}

PROJECTS: Dict[int, Dict[str, List[int] | int]] = {
    101: {"owner_id": 2, "members": [3]},
    102: {"owner_id": 4, "members": []},
}


def control_project_participants(
    acting_user_id: int,
    prj_id: int,
    action_type: str,
    target_id: int,
) -> bool:
    """
    Allow a project owner or an administrator to add or remove members from a project.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the action.
    prj_id : int
        Project ID being modified.
    action_type : str
        Either 'add' or 'remove'.
    target_id : int
        ID of the user to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate action_type
    if action_type not in {"add", "remove"}:
        return False

    # Ensure project exists
    project = PROJECTS.get(prj_id)
    if not project:
        return False

    # Ensure target user exists
    if target_id not in USERS:
        return False

    # Determine privileges
    acting_role = USERS.get(acting_user_id)
    if acting_role == "admin":
        authorized = True
    elif acting_role == "user" and project["owner_id"] == acting_user_id:
        authorized = True
    else:
        authorized = False

    if not authorized:
        return False

    members: List[int] = project["members"]

    try:
        if action_type == "add":
            # Avoid duplicate entries
            if target_id not in members:
                members.append(target_id)
        else:  # action_type == "remove"
            if target_id in members:
                members.remove(target_id)
        return True
    except Exception:
        # Catch unforeseen errors (e.g., list mutation issues)
        return False