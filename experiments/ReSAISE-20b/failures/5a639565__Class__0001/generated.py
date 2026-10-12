# -*- coding: utf-8 -*-

from typing import Dict, Set

# Example data structures (these would normally come from a database or external source)
PROJECTS: Dict[int, Dict[str, Set[int] | int]] = {
    # project_id : { "owner_id": int, "members": set of user_ids }
}

USERS: Dict[int, str] = {
    # user_id : "admin" or "user"
}


def manage_team_access(
    executor_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int,
) -> bool:
    """
    Allow project owners or administrators to add or remove a member from a project.

    Parameters
    ----------
    executor_user_id : int
        The user performing the action.
    proj_id : int
        The project being modified.
    operation : str
        Either 'add' or 'remove'.
    target_member_id : int
        The user to be added or removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """

    # Validate operation type
    if operation not in {"add", "remove"}:
        return False

    # Check that the project exists
    project = PROJECTS.get(proj_id)
    if not project:
        return False

    # Verify that the target member exists in the system
    if target_member_id not in USERS:
        return False

    # Authorization check: executor must be admin or the owner of the project
    if USERS.get(executor_user_id) != "admin" and executor_user_id != project["owner_id"]:
        return False

    members: Set[int] = project.get("members", set())

    if operation == "add":
        # Prevent duplicate addition
        if target_member_id in members:
            return False
        members.add(target_member_id)
    else:  # operation == "remove"
        if target_member_id not in members:
            return False
        members.remove(target_member_id)

    # Persist the updated member set back to the project dict
    project["members"] = members

    return True