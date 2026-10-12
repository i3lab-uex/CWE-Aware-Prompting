# -*- coding: utf-8 -*-
"""
Project membership handler.

This module provides a single function, `handle_project_membership`, which
allows project owners to add or remove members from their projects,
while administrators can modify any project's membership.

The data structures used are simple dictionaries for demonstration purposes.
In a real application these would be replaced with database models or
ORM objects.

Author: OpenAI ChatGPT
"""

from typing import Dict, Set

# Example data structures. In production these would be populated from a DB.
USERS: Dict[int, Set[str]] = {
    # user_id : set of roles
    1: {"admin"},
    2: {"user"},
    3: {"user"},
    4: {"user"},
}

PROJECTS: Dict[int, Dict[str, object]] = {
    # project_id : {"owner_id": int, "members": set of user_ids}
    101: {"owner_id": 2, "members": {3}},
    102: {"owner_id": 4, "members": set()},
}

def handle_project_membership(
    req_user_id: int,
    proj_id: int,
    mod: str,
    mod_user_id: int
) -> bool:
    """
    Modify membership of a project.

    Parameters
    ----------
    req_user_id : int
        ID of the user performing the operation.
    proj_id : int
        Target project identifier.
    mod : str
        Either 'add' or 'remove'.
    mod_user_id : int
        User ID to be added or removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate project existence
    project = PROJECTS.get(proj_id)
    if not project:
        return False

    # Validate requesting user existence
    req_user_roles = USERS.get(req_user_id)
    if req_user_roles is None:
        return False

    # Validate target user existence
    if mod_user_id not in USERS:
        return False

    # Permission check: admin or owner
    is_admin = "admin" in req_user_roles
    is_owner = project["owner_id"] == req_user_id

    if not (is_admin or is_owner):
        return False

    members: Set[int] = project["members"]

    # Perform the requested modification
    if mod == "add":
        members.add(mod_user_id)
    elif mod == "remove":
        members.discard(mod_user_id)  # discard does nothing if not present
    else:
        return False

    return True


# Example usage (for manual testing only)
if __name__ == "__main__":
    # Admin adds user 4 to project 101
    print(handle_project_membership(1, 101, "add", 4))   # True
    print(PROJECTS[101]["members"])                      # {3, 4}

    # Owner removes user 3 from their project
    print(handle_project_membership(2, 101, "remove", 3))# True
    print(PROJECTS[101]["members"])                      # {4}

    # Unauthorized user tries to add a member
    print(handle_project_membership(3, 101, "add", 2))   # False