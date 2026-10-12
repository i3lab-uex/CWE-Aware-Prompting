# -*- coding: utf-8 -*-
"""
Project membership management module.

This module provides a single public function `handle_project_membership`
which allows project owners or admins to add or remove members from a
project. The function performs all necessary validation and authorization
checks before modifying the global data structures.

The module assumes the existence of two dictionaries:

- PROJECTS: mapping project_id -> dict(owner_id: int, members: list[int])
- USERS:    mapping user_id   -> str role ('user' or 'admin')
"""

from typing import Dict, List

# Example data structures (to be replaced with real persistence in production)
PROJECTS: Dict[int, Dict[str, List[int]]] = {}
USERS: Dict[int, str] = {}


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
        Either 'add' or 'remove'.
    target_member_id : int
        ID of the user to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic input validation
    if operation not in {"add", "remove"}:
        return False

    # Verify that the active user exists
    if active_user_id not in USERS:
        return False

    # Verify that the target member exists
    if target_member_id not in USERS:
        return False

    # Verify that the project exists
    proj = PROJECTS.get(proj_id)
    if not proj:
        return False

    # Authorization: user must be the owner or an admin
    if active_user_id != proj["owner_id"] and USERS[active_user_id] != "admin":
        return False

    members = proj["members"]

    if operation == "add":
        # Prevent duplicate membership
        if target_member_id in members:
            return False
        members.append(target_member_id)
    else:  # operation == "remove"
        if target_member_id not in members:
            return False
        # Optionally prevent removing the owner (not required but safe)
        if target_member_id == proj["owner_id"]:
            return False
        members.remove(target_member_id)

    # If we reach here, the operation succeeded
    return True


# --------------------------------------------------------------------
# Example usage (for demonstration only; remove or comment out in production)
if __name__ == "__main__":
    # Setup demo data
    USERS.update(
        {
            1: "admin",
            2: "user",
            3: "user",
            4: "user",
        }
    )
    PROJECTS.update(
        {
            101: {"owner_id": 2, "members": [3]},
        }
    )

    # Admin adding member
    print(handle_project_membership(1, 101, "add", 4))  # True
    print(PROJECTS[101]["members"])  # [3, 4]

    # Owner removing member
    print(handle_project_membership(2, 101, "remove", 3))  # True
    print(PROJECTS[101]["members"])  # [4]