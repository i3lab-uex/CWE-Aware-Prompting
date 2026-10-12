# adjust_team_membership.py

from typing import Dict, List

# Example data structures (to be replaced by real ones in production)
PROJECTS: Dict[int, Dict[str, List[int] | int]] = {
    # project_id : {"owner_id": int, "members": List[int]}
}

USERS: Dict[int, str] = {
    # user_id : "user" or "admin"
}

def adjust_team_membership(
    operator_id: int,
    team_project_id: int,
    operation_type: str,
    member_id: int
) -> bool:
    """
    Add or remove a user from a project's membership list.

    Parameters
    ----------
    operator_id : int
        The ID of the user performing the operation.
    team_project_id : int
        The project whose membership is being modified.
    operation_type : str
        Either 'add' or 'remove'.
    member_id : int
        The user ID to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.

    Raises
    ------
    ValueError
        If an invalid operation_type is supplied.
    KeyError
        If the project or user does not exist.

    Notes
    -----
    - Only the project owner or an admin can modify membership.
    - Adding a user who is already a member, or removing a user who
      is not a member (or the owner when trying to remove them), fails
      and returns False.
    """
    # Validate operation type
    if operation_type not in {"add", "remove"}:
        raise ValueError("operation_type must be 'add' or 'remove'")

    # Ensure project exists
    try:
        project = PROJECTS[team_project_id]
    except KeyError:
        return False

    # Ensure member exists
    if member_id not in USERS:
        return False

    # Permission check: owner or admin
    operator_role = USERS.get(operator_id)
    if operator_role != "admin" and project["owner_id"] != operator_id:
        return False

    members: List[int] = project.get("members", [])

    if operation_type == "add":
        if member_id in members:
            return False  # already a member
        members.append(member_id)
    else:  # remove
        if member_id not in members:
            return False  # nothing to remove
        # Prevent removing the owner from membership list if present
        if member_id == project["owner_id"]:
            return False
        members.remove(member_id)

    # Update the project's member list
    project["members"] = members
    return True