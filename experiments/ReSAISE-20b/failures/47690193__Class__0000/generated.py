from typing import Dict, List

# Sample data structures (replace with real ones in production)
PROJECTS: Dict[int, Dict[str, object]] = {
    # Example project structure
    1: {"owner_id": 10, "members": [20, 30]},
    2: {"owner_id": 11, "members": [21]}
}

USERS: Dict[int, str] = {
    # Example user roles
    10: "user",
    11: "admin",
    20: "user",
    21: "user",
    30: "admin"
}


def control_project_permissions(
    executing_user_id: int,
    prjct_id: int,
    act_type: str,
    tgt_user_id: int
) -> bool:
    """
    Allows a project owner to add or remove members from their project.
    Admins can perform the operation on any project.

    Parameters
    ----------
    executing_user_id : int
        The ID of the user performing the action.
    prjct_id : int
        The project whose membership is to be updated.
    act_type : str
        Either 'add' or 'remove'.
    tgt_user_id : int
        The user ID to be added or removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic input validation
    if act_type not in {"add", "remove"}:
        return False

    # Verify that the executing user exists
    exec_role = USERS.get(executing_user_id)
    if exec_role is None:
        return False

    # Verify that the target user exists
    if tgt_user_id not in USERS:
        return False

    # Verify that the project exists
    project = PROJECTS.get(prjct_id)
    if project is None:
        return False

    # Authorization check
    if exec_role != "admin":
        if project.get("owner_id") != executing_user_id:
            # Not the owner, and not an admin → deny
            return False

    members: List[int] = project.get("members", [])
    if act_type == "add":
        # Avoid duplicate entries
        if tgt_user_id in members:
            return False
        members.append(tgt_user_id)
    else:  # act_type == "remove"
        if tgt_user_id not in members:
            return False
        members.remove(tgt_user_id)

    # Update the project's member list
    project["members"] = members
    return True