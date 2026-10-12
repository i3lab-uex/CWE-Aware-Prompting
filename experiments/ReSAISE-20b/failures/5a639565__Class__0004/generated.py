# -*- coding: utf-8 -*-

"""
Team access management module.

This module implements the `manage_team_access` function, which allows a project
owner to add or remove members from their own projects. Administrators can modify
any project.

The implementation includes proper authorization checks to mitigate CWE-862
(Missing Authorization). All inputs are validated and errors are handled gracefully.
"""

from __future__ import annotations

from typing import Dict, Any


# Example data structures. In a real application these would come from a database.
PROJECTS: Dict[int, Dict[str, Any]] = {
    1: {"owner_id": 10, "members": {20, 30}},
    2: {"owner_id": 15, "members": {25}},
}

USERS: Dict[int, Dict[str, Any]] = {
    10: {"role": "admin"},
    15: {"role": "user"},
    20: {"role": "user"},
    25: {"role": "user"},
    30: {"role": "admin"},
}


def _is_admin(user_id: int) -> bool:
    """Return True if the user has an admin role."""
    return USERS.get(user_id, {}).get("role") == "admin"


def _is_owner(project: Dict[str, Any], user_id: int) -> bool:
    """Return True if the user is the owner of the given project."""
    return project.get("owner_id") == user_id


def manage_team_access(
    executor_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int,
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    executor_user_id : int
        The user performing the operation.
    proj_id : int
        Identifier of the project to modify.
    operation : str
        Either 'add' or 'remove'.
    target_member_id : int
        The user to be added or removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic type validation
    if not isinstance(executor_user_id, int) or not isinstance(proj_id, int) \
       or not isinstance(target_member_id, int):
        return False

    if operation not in {"add", "remove"}:
        return False

    # Ensure the project exists
    project = PROJECTS.get(proj_id)
    if project is None:
        return False

    # Authorization check: admin or owner
    if not (_is_admin(executor_user_id) or _is_owner(project, executor_user_id)):
        return False

    # Ensure target member exists
    if target_member_id not in USERS:
        return False

    members = project.setdefault("members", set())

    if operation == "add":
        # Adding an existing member is idempotent; still return True
        members.add(target_member_id)
    else:  # operation == "remove"
        # Removing a non-member is considered a no‑op but not an error
        members.discard(target_member_id)

    return True


# Example usage (for demonstration; remove or guard under __main__ in production)
if __name__ == "__main__":
    print(manage_team_access(10, 1, "add", 25))   # True (admin)
    print(manage_team_access(15, 1, "remove", 20))  # False (not owner or admin)
    print(manage_team_access(15, 2, "remove", 25))   # True (owner)