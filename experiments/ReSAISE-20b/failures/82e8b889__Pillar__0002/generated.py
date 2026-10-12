# -*- coding: utf-8 -*-
"""
Implementation of `adjust_team_membership` for secure project membership management.
"""

from typing import Dict, List

# Sample data structures; in a real application these would come from a database.
PROJECTS: Dict[int, Dict[str, List[int] | int]] = {
    1: {"owner_id": 10, "members": [20, 30]},
    2: {"owner_id": 15, "members": [25]},
}

USERS: Dict[int, str] = {
    10: "admin",
    15: "user",
    20: "user",
    25: "admin",
    30: "user",
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
        The ID of the project to be modified.
    operation_type : str
        Either 'add' or 'remove'.
    member_id : int
        The ID of the user to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate input types early to avoid accidental injection or mis-use
    if not isinstance(operator_id, int) or not isinstance(team_project_id, int) \
       or not isinstance(operation_type, str) or not isinstance(member_id, int):
        return False

    # Operation must be one of the allowed strings
    if operation_type not in {"add", "remove"}:
        return False

    # Check that the project exists
    project = PROJECTS.get(team_project_id)
    if not project:
        return False

    # Check that the operator exists and has a role
    operator_role = USERS.get(operator_id)
    if not operator_role:
        return False

    # Enforce access control: only admins or the project owner can modify membership
    if operator_role != "admin" and operator_id != project["owner_id"]:
        return False

    # Retrieve current members list
    members: List[int] = project.get("members", [])
    if operation_type == "add":
        # Prevent adding duplicates
        if member_id in members:
            return False
        members.append(member_id)
    else:  # operation_type == "remove"
        if member_id not in members:
            return False
        members.remove(member_id)

    # Update the project data structure (in a real system this would be persisted)
    PROJECTS[team_project_id]["members"] = members
    return True

# Example usage (commented out to keep the module import-friendly)
# if __name__ == "__main__":
#     print(adjust_team_membership(10, 1, "add", 40))   # True (admin)
#     print(adjust_team_membership(15, 1, "remove", 20)) # False (not owner/admin)