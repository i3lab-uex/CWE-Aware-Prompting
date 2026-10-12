# -*- coding: utf-8 -*-

"""
Utility module for project membership management.

This module defines a single public function, `adjust_team_membership`, which
handles adding or removing users from a project while enforcing proper
authorization rules.

Author: ChatGPT
"""

from typing import Dict, List

# --------------------------------------------------------------------------- #
# Mock data structures (replace with real persistence in production)
# --------------------------------------------------------------------------- #

# Example project store: {project_id: {'owner_id': int, 'members': List[int]}}
PROJECTS: Dict[int, Dict[str, object]] = {
    1: {"owner_id": 10, "members": [20, 30]},
    2: {"owner_id": 11, "members": [31]},
}

# Example user store: {user_id: {'role': 'admin' | 'user'}}
USERS: Dict[int, Dict[str, str]] = {
    10: {"role": "user"},
    11: {"role": "user"},
    99: {"role": "admin"},   # admin user
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def adjust_team_membership(
    operator_id: int,
    team_project_id: int,
    operation_type: str,
    member_id: int
) -> bool:
    """
    Add or remove a user from the membership list of a project.

    Parameters
    ----------
    operator_id : int
        ID of the user performing the operation.
    team_project_id : int
        ID of the target project.
    operation_type : str
        Either 'add' or 'remove'.
    member_id : int
        ID of the user to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic validation of input types (type hints cover this but we guard against bad data)
    if not isinstance(operator_id, int) or not isinstance(team_project_id, int) \
       or not isinstance(operation_type, str) or not isinstance(member_id, int):
        return False

    # 1. Check that operator exists
    operator = USERS.get(operator_id)
    if operator is None:
        return False

    # 2. Check that the project exists
    project = PROJECTS.get(team_project_id)
    if project is None:
        return False

    # 3. Authorization check
    is_admin = operator.get("role") == "admin"
    is_owner = project.get("owner_id") == operator_id

    if not (is_admin or is_owner):
        # Operator does not have permission to modify this project
        return False

    # 4. Ensure the member exists in the system (optional but safer)
    if member_id not in USERS:
        return False

    # 5. Perform the requested operation
    members: List[int] = project.setdefault("members", [])

    if operation_type == "add":
        # Avoid duplicates
        if member_id in members:
            return False  # Already a member; consider this a failure
        members.append(member_id)
        return True

    elif operation_type == "remove":
        if member_id not in members:
            return False  # Member not present
        members.remove(member_id)
        return True

    else:
        # Unsupported operation type
        return False


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Successful add by owner
    assert adjust_team_membership(10, 1, "add", 40) is True
    # Duplicate add fails
    assert adjust_team_membership(10, 1, "add", 40) is False
    # Successful remove by owner
    assert adjust_team_membership(10, 1, "remove", 40) is True
    # Unauthorized remove by non-owner/non-admin fails
    assert adjust_team_membership(20, 1, "remove", 30) is False
    # Admin can remove anyone from any project
    assert adjust_team_membership(99, 2, "remove", 31) is True

    print("All tests passed.")