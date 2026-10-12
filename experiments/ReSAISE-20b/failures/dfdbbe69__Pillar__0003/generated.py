#!/usr/bin/env python3
"""
Project membership handler.

This module defines `handle_project_membership`, which allows project owners to add or remove
members from their projects. Administrators may modify any project.
"""

from typing import Dict, Set

# Example data structures (replace with actual data sources in production)
USERS: Dict[int, str] = {
    # user_id : role ('admin' or 'user')
}

PROJECTS: Dict[int, Dict[str, Set[int]]] = {
    # project_id : {'owner_id': int, 'members': set(user_ids)}
}


def handle_project_membership(req_user_id: int,
                              proj_id: int,
                              mod: str,
                              mod_user_id: int) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    req_user_id : int
        ID of the user performing the operation.
    proj_id : int
        ID of the target project.
    mod : str
        Either 'add' or 'remove'.
    mod_user_id : int
        ID of the user to be added or removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate input parameters
    if mod not in {"add", "remove"}:
        return False

    # Ensure the project exists
    project = PROJECTS.get(proj_id)
    if not project:
        return False

    # Ensure the requestor exists
    req_role = USERS.get(req_user_id)
    if req_role is None:
        return False

    # Permission check: admin or project owner
    if req_role != "admin" and req_user_id != project["owner_id"]:
        return False

    # Ensure the target user exists
    if mod_user_id not in USERS:
        return False

    members: Set[int] = project["members"]

    if mod == "add":
        # Prevent adding the owner as a member (optional)
        if mod_user_id == project["owner_id"]:
            return False
        members.add(mod_user_id)
    else:  # mod == "remove"
        if mod_user_id in members:
            members.remove(mod_user_id)
        else:
            # Trying to remove a user who is not a member
            return False

    # Successful operation
    return True


# Example usage (remove or comment out before deploying)
if __name__ == "__main__":
    # Populate dummy data
    USERS.update({1: "admin", 2: "user", 3: "user"})
    PROJECTS.update({100: {"owner_id": 2, "members": {3}}})

    # Admin adds user 1 to project 100
    print(handle_project_membership(1, 100, "add", 1))  # True

    # Owner removes user 3
    print(handle_project_membership(2, 100, "remove", 3))  # True

    # Unauthorized user tries to add
    print(handle_project_membership(3, 100, "add", 2))  # False