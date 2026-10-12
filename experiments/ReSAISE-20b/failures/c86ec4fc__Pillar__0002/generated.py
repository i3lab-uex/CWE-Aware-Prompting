# -*- coding: utf-8 -*-
"""
Module implementing project participant management with proper access control.
"""

from __future__ import annotations

# Example data structures – in a real system these would come from a database.
PROJECTS: dict[int, dict[str, any]] = {
    # project_id : { "owner_id": int, "members": set[int] }
}

USERS: dict[int, dict[str, any]] = {
    # user_id : { "role": str }  # role can be 'admin' or 'user'
}


def control_project_participants(
    acting_user_id: int,
    prj_id: int,
    action_type: str,
    target_id: int
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the action.
    prj_id : int
        ID of the project to modify.
    action_type : str
        Either 'add' or 'remove'.
    target_id : int
        ID of the user to add or remove.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Validate input types
    if not isinstance(acting_user_id, int) or not isinstance(prj_id, int) \
       or not isinstance(action_type, str) or not isinstance(target_id, int):
        return False

    # Check that the project exists
    project = PROJECTS.get(prj_id)
    if not project:
        return False

    # Check that the target user exists
    if target_id not in USERS:
        return False

    # Determine acting user's role
    actor_role = USERS.get(acting_user_id, {}).get("role")
    if not actor_role:
        return False

    # Only admins or the project owner can modify participants
    if actor_role != "admin" and acting_user_id != project["owner_id"]:
        return False

    # Ensure members is a set for efficient lookup
    members = project.get("members")
    if not isinstance(members, (set, list)):
        return False
    if isinstance(members, list):
        members = set(members)
        project["members"] = members

    # Perform the requested action
    if action_type == "add":
        if target_id in members:
            # Already a member; consider this a no-op but still success
            return True
        members.add(target_id)
    elif action_type == "remove":
        if target_id not in members:
            # Not a member; consider this a no-op but still success
            return True
        members.remove(target_id)
    else:
        # Unsupported action_type
        return False

    return True