#!/usr/bin/env python3
"""
Implementation of manage_team_access that safely allows project owners or administrators
to add or remove members from projects.

CWE-284: Improper Access Control is mitigated by strict role checks and
validation of all inputs before performing any modifications.
"""

from typing import Dict, Any

# Example data structures – in a real system these would come from a database
PROJECTS: Dict[int, Dict[str, Any]] = {
    # project_id: { 'owner_id': int, 'members': set[int] }
}

USERS: Dict[int, Dict[str, str]] = {
    # user_id: { 'role': 'admin' | 'user' }
}

def _is_admin(user_id: int) -> bool:
    """Return True if the user has an admin role."""
    return USERS.get(user_id, {}).get("role") == "admin"

def _validate_int(value: Any, name: str) -> bool:
    """Validate that a value is an integer."""
    if not isinstance(value, int):
        return False
    if value < 0:
        return False
    return True

def manage_team_access(
    executor_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int
) -> bool:
    """
    Allow project owners to add/remove members from their own projects.
    Administrators may modify any project.

    Args:
        executor_user_id: ID of the user performing the action.
        proj_id: ID of the project to modify.
        operation: 'add' or 'remove'.
        target_member_id: ID of the member to add/remove.

    Returns:
        True if the operation succeeded, False otherwise.
    """
    # 1. Validate input types and ranges
    if not all(
        _validate_int(v, n)
        for v, n in [(executor_user_id, "executor_user_id"),
                     (proj_id, "proj_id"),
                     (target_member_id, "target_member_id")]
    ):
        return False

    if operation not in {"add", "remove"}:
        return False

    # 2. Ensure executor exists
    if executor_user_id not in USERS:
        return False

    # 3. Ensure project exists
    project = PROJECTS.get(proj_id)
    if not project:
        return False

    # 4. Permission check
    is_owner = executor_user_id == project.get("owner_id")
    if not (is_owner or _is_admin(executor_user_id)):
        return False

    # 5. Ensure target member exists in system
    if target_member_id not in USERS:
        return False

    members = project.setdefault("members", set())

    if operation == "add":
        # Prevent duplicate addition
        if target_member_id in members:
            return False
        members.add(target_member_id)
    else:  # operation == "remove"
        if target_member_id not in members:
            return False
        members.remove(target_member_id)

    # 6. Persist changes – in this example PROJECTS is already updated
    return True