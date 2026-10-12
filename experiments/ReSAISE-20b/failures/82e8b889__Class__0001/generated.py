#!/usr/bin/env python3
"""
Module: project_team_management

Provides a function to safely add or remove members from projects,
ensuring proper authorization and basic validation.
"""

from __future__ import annotations

import typing as _t
from dataclasses import dataclass, field


# ----------------------------------------------------------------------
# Mock data structures (replace with real persistence in production)
# ----------------------------------------------------------------------
@dataclass
class Project:
    project_id: int
    owner_id: int
    members: set[int] = field(default_factory=set)


@dataclass
class User:
    user_id: int
    role: str  # "user" or "admin"


# Example in-memory data stores
PROJECTS: dict[int, Project] = {}
USERS: dict[int, User] = {}


# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def adjust_team_membership(
    operator_id: int,
    team_project_id: int,
    operation_type: str,
    member_id: int,
) -> bool:
    """
    Add or remove a user from a project's membership list.

    Parameters
    ----------
    operator_id : int
        The ID of the user performing the action.
    team_project_id : int
        The ID of the project to modify.
    operation_type : str
        Either 'add' or 'remove'.
    member_id : int
        The ID of the user to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate operation type
    if operation_type not in {"add", "remove"}:
        return False

    # Fetch operator, project, and target member
    operator = USERS.get(operator_id)
    if not operator:
        return False

    project = PROJECTS.get(team_project_id)
    if not project:
        return False

    # Authorization: operator must be admin or owner
    if operator.role != "admin" and project.owner_id != operator_id:
        return False

    # Prevent self-removal of owner by non-admin
    if operation_type == "remove" and member_id == project.owner_id:
        # Only admin can remove the owner from their own project
        if operator.role != "admin":
            return False

    # Perform operation
    try:
        if operation_type == "add":
            project.members.add(member_id)
        else:  # remove
            project.members.discard(member_id)
    except Exception:
        return False

    return True


# ----------------------------------------------------------------------
# Example usage (for testing only)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Setup sample data
    USERS[1] = User(user_id=1, role="admin")
    USERS[2] = User(user_id=2, role="user")
    USERS[3] = User(user_id=3, role="user")

    PROJECTS[100] = Project(project_id=100, owner_id=2)

    # Admin adds member 3
    assert adjust_team_membership(1, 100, "add", 3) is True
    assert 3 in PROJECTS[100].members

    # Owner removes member 3
    assert adjust_team_membership(2, 100, "remove", 3) is True
    assert 3 not in PROJECTS[100].members

    # Non-owner, non-admin attempts to add member
    assert adjust_team_membership(3, 100, "add", 2) is False