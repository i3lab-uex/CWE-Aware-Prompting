# -*- coding: utf-8 -*-
"""
Project access control module.

This module defines a function `manage_project_access` that allows project
owners to add or remove members from their projects, while administrators can
modify any project. The implementation follows the OWASP Top 10 recommendation
for CWE‑284 (Improper Access Control) by strictly validating the actor's
privileges before performing any modification.

Author: ChatGPT
"""

from typing import Dict, Set

# Example data structures (would normally be loaded from a database)
PROJECTS: Dict[int, Dict[str, Set[int]]] = {
    # project_id: { 'owner_id': int, 'members': set of user_ids }
}

USERS: Dict[int, str] = {
    # user_id: role ('admin', 'owner', 'member', etc.)
}


def manage_project_access(
    current_user_id: int,
    project_id: int,
    action: str,
    target_user_id: int
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    current_user_id : int
        The ID of the user invoking the function.
    project_id : int
        The ID of the project to modify.
    action : str
        Either 'add' or 'remove'.
    target_user_id : int
        The ID of the user to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate that the project exists
    project = PROJECTS.get(project_id)
    if not project:
        return False

    # Validate that the target user exists
    if target_user_id not in USERS:
        return False

    # Determine privileges
    current_role = USERS.get(current_user_id)
    if current_role is None:
        return False

    # Admins can modify any project
    if current_role.lower() == "admin":
        authorized = True
    else:
        # Only the owner of this specific project may modify it
        authorized = current_user_id == project.get("owner_id")

    if not authorized:
        return False

    # Ensure action is valid
    if action.lower() == "add":
        project["members"].add(target_user_id)
        return True
    elif action.lower() == "remove":
        project["members"].discard(target_user_id)
        return True
    else:
        # Invalid action string
        return False


# Example usage (commented out)
# if __name__ == "__main__":
#     # Populate sample data
#     USERS.update({1: "admin", 2: "owner", 3: "member"})
#     PROJECTS[101] = {"owner_id": 2, "members": {3}}
#     print(manage_project_access(1, 101, "add", 4))   # True (admin)
#     print(manage_project_access(2, 101, "remove", 3)) # True (owner)
#     print(manage_project_access(3, 101, "add", 5))   # False (not owner/admin)