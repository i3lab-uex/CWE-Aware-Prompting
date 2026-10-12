#!/usr/bin/env python3
"""
Implementation of `manage_team_access` that allows project owners or administrators to add or remove members from projects.
"""

from typing import Dict, Set

# Sample data structures. In a real application these would be replaced by database access.
PROJECTS: Dict[int, Dict[str, Set[int]]] = {
    # project_id : {'owner_id': int, 'members': set(user_ids)}
    1: {"owner_id": 101, "members": {102, 103}},
    2: {"owner_id": 202, "members": {203}},
}

USERS: Dict[int, str] = {
    # user_id : role ('admin' or 'user')
    101: "admin",
    102: "user",
    103: "user",
    201: "admin",
    202: "user",
    203: "user",
}

def manage_team_access(
    executor_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int,
) -> bool:
    """
    Allows a project owner or an administrator to add or remove a member from a project.

    Parameters
    ----------
    executor_user_id : int
        The ID of the user performing the operation.
    proj_id : int
        The project ID being modified.
    operation : str
        Either 'add' or 'remove'.
    target_member_id : int
        The ID of the user to be added or removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate project existence
    project = PROJECTS.get(proj_id)
    if not project:
        return False

    # Validate executor role
    executor_role = USERS.get(executor_user_id)
    if not executor_role:
        return False

    # Only project owners or admins can modify the team
    if executor_role != "admin" and executor_user_id != project["owner_id"]:
        return False

    # Validate operation
    if operation not in {"add", "remove"}:
        return False

    # Ensure target member exists
    if target_member_id not in USERS:
        return False

    members: Set[int] = project["members"]

    if operation == "add":
        # Adding an existing member is harmless; still return True
        members.add(target_member_id)
    else:  # operation == "remove"
        if target_member_id not in members:
            return False
        # Prevent removing the project owner
        if target_member_id == project["owner_id"]:
            return False
        members.remove(target_member_id)

    # Update the project's member set (in-place, but explicit assignment for clarity)
    project["members"] = members
    return True


# Example usage (uncomment to test)
if __name__ == "__main__":
    print(manage_team_access(101, 1, "add", 104))   # True (admin adding)
    print(manage_team_access(102, 1, "remove", 103)) # False (non-owner non-admin)
    print(manage_team_access(101, 1, "remove", 102)) # True (owner removing member)