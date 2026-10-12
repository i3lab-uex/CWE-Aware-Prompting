# -*- coding: utf-8 -*-
"""
Team access management module.

This module defines a single function `manage_team_access` that allows
project owners to add or remove members from their own projects, while
administrators can modify any project.  The function performs strict
access‑control checks to prevent privilege escalation (CWE‑284).

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample data structures. In a real application these would be loaded from
# a database or an external service.
# --------------------------------------------------------------------------- #
PROJECTS: dict[int, dict[str, object]] = {
    # project_id : { 'owner_id': int, 'members': set[int] }
}

USERS: dict[int, str] = {
    # user_id : 'admin' | 'user'
}


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _is_admin(user_id: int) -> bool:
    """Return True if the user has an admin role."""
    return USERS.get(user_id) == "admin"


def _get_project(proj_id: int) -> dict[str, object] | None:
    """Retrieve the project dictionary or None if it does not exist."""
    return PROJECTS.get(proj_id)


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def manage_team_access(
    executor_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int,
) -> bool:
    """
    Modify the membership of a project.

    Parameters
    ----------
    executor_user_id : int
        ID of the user performing the operation.
    proj_id : int
        Project identifier whose membership is to be modified.
    operation : str
        Either 'add' or 'remove'.
    target_member_id : int
        User ID to be added or removed from the project's members.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.

    Raises
    ------
    ValueError
        If `operation` is not one of 'add' or 'remove'.
    """
    # Validate operation type
    if operation not in {"add", "remove"}:
        raise ValueError("operation must be 'add' or 'remove'")

    # Retrieve the project
    project = _get_project(proj_id)
    if not project:
        # Project does not exist
        return False

    # Access control: executor must be admin or owner of the project
    if not (_is_admin(executor_user_id) or executor_user_id == project["owner_id"]):
        return False

    # Ensure the target member exists in the system
    if target_member_id not in USERS:
        return False

    members: set[int] = project.setdefault("members", set())

    if operation == "add":
        # Adding a member that is already present is harmless
        members.add(target_member_id)
    else:  # operation == "remove"
        # Removing a member that is not present should still succeed
        members.discard(target_member_id)

    # Persist the updated members set back to the project (in place)
    project["members"] = members
    return True


# --------------------------------------------------------------------------- #
# Example usage (commented out)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     # Setup sample data
#     USERS.update({1: "admin", 2: "user", 3: "user"})
#     PROJECTS[100] = {"owner_id": 2, "members": {3}}
#
#     # Admin adds user 1 to project 100
#     print(manage_team_access(1, 100, "add", 1))   # True
#     # Owner removes user 3 from project 100
#     print(manage_team_access(2, 100, "remove", 3)) # True
#     # Unauthorized user tries to add someone
#     print(manage_team_access(3, 100, "add", 2))   # False