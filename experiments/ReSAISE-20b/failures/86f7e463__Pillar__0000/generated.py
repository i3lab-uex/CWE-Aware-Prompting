#!/usr/bin/env python3
"""
Project membership management module.

This module provides a single public function:
    update_project_members(acting_user_id, project_identifier,
                           modification, user_to_update_id)

The function enforces access control so that only the project owner or an
admin can modify membership. It also validates input and handles edge cases.
"""

from __future__ import annotations

from typing import Dict, List

# --------------------------------------------------------------------------- #
# Example data structures. In a real application these would come from a
# database or persistent store.
# --------------------------------------------------------------------------- #
PROJECTS: Dict[int, Dict[str, List[int]]] = {
    1: {"owner_id": 10, "members": [20, 30]},
    2: {"owner_id": 11, "members": []},
}

USERS: Dict[int, str] = {
    10: "admin",
    11: "user",
    20: "user",
    30: "user",
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def update_project_members(
    acting_user_id: int,
    project_identifier: int,
    modification: str,
    user_to_update_id: int,
) -> bool:
    """
    Add or remove a user from a project's membership list.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the operation.
    project_identifier : int
        Target project's ID.
    modification : str
        Either 'add' or 'remove'.
    user_to_update_id : int
        ID of the user to add or remove.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Validate modification value
    if modification not in {"add", "remove"}:
        return False

    # Ensure both users exist
    if acting_user_id not in USERS or user_to_update_id not in USERS:
        return False

    # Retrieve the project
    project = PROJECTS.get(project_identifier)
    if not project:
        return False

    # Access control: only owner or admin can modify
    if acting_user_id != project["owner_id"] and USERS[acting_user_id] != "admin":
        return False

    members: List[int] = project["members"]

    if modification == "add":
        # Avoid duplicate entries
        if user_to_update_id in members:
            return False
        members.append(user_to_update_id)
    else:  # modification == "remove"
        if user_to_update_id not in members:
            return False
        members.remove(user_to_update_id)

    # Update the project (list is mutable; no need to reassign)
    return True

# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only; remove in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Should succeed: admin adding a member
    assert update_project_members(10, 1, "add", 40) is False  # user 40 doesn't exist
    USERS[40] = "user"
    assert update_project_members(10, 1, "add", 40) is True
    # Should fail: non-owner non-admin attempting to remove
    assert update_project_members(20, 1, "remove", 30) is False
    # Should succeed: owner removing a member
    assert update_project_members(10, 1, "remove", 30) is True

    print("All tests passed.")