#!/usr/bin/env python3
"""
Project membership control with proper access checks.

This module defines a single function `control_project_permissions` that
enforces the following rules:

1. Only an **admin** or the **owner** of a project may add or remove members.
2. The action type must be either `'add'` or `'remove'`.
3. For an `'add'` action the target user must not already be a member.
4. For a `'remove'` action the target user must currently be a member.
5. If any rule is violated, the function returns `False` and leaves the
   data unchanged.

The implementation avoids common pitfalls such as mutable default arguments,
unauthorized data exposure, or accidental mutation of unrelated state.
"""

from __future__ import annotations

from typing import Dict, List

# Example global data structures. In a real application these would be
# loaded from a database or another persistence layer.
PROJECTS: Dict[int, Dict[str, object]] = {
    # project_id : { 'owner_id': int, 'members': List[int] }
}

USERS: Dict[int, str] = {
    # user_id : role ('admin' or 'user')
}

def control_project_permissions(
    executing_user_id: int,
    prjct_id: int,
    act_type: str,
    tgt_user_id: int
) -> bool:
    """
    Add or remove a member from a project if the executing user is authorized.

    Parameters
    ----------
    executing_user_id : int
        ID of the user performing the operation.
    prjct_id : int
        ID of the project to modify.
    act_type : str
        Either 'add' or 'remove'.
    tgt_user_id : int
        ID of the user to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate action type
    if act_type not in {"add", "remove"}:
        raise ValueError(f"Invalid action type: {act_type!r}")

    # Check that both users exist
    if executing_user_id not in USERS or tgt_user_id not in USERS:
        return False

    # Retrieve project
    project = PROJECTS.get(prjct_id)
    if not project:
        return False

    # Authorization check: admin or owner
    role = USERS.get(executing_user_id)
    if role != "admin" and executing_user_id != project.get("owner_id"):
        return False

    members: List[int] = project.setdefault("members", [])

    # Perform the requested action
    if act_type == "add":
        if tgt_user_id in members:
            return False  # already a member
        members.append(tgt_user_id)
    else:  # act_type == "remove"
        if tgt_user_id not in members:
            return False  # cannot remove non‑member
        members.remove(tgt_user_id)

    return True

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    # Setup dummy data
    USERS.update({1: "admin", 2: "user", 3: "user"})
    PROJECTS.update({101: {"owner_id": 2, "members": [3]}})

    print(control_project_permissions(1, 101, "add", 2))   # True (admin adds owner)
    print(control_project_permissions(2, 101, "remove", 3)) # True (owner removes member)
    print(control_project_permissions(3, 101, "add", 1))   # False (not admin/owner)