# -*- coding: utf-8 -*-
"""
Module providing project membership management with proper authorization checks.
"""

from typing import Dict, List

# Example data structures (replace or populate as needed in the real application)
PROJECTS: Dict[int, Dict[str, object]] = {
    # project_id: {"owner_id": int, "members": List[int]}
}

USERS: Dict[int, str] = {
    # user_id: "admin" or "user"
}


def handle_project_membership(
    acting_user_id: int,
    prjt_id: int,
    member_action: str,
    target_member_id: int,
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the action.
    prjt_id : int
        Project identifier to be updated.
    member_action : str
        Either 'add' or 'remove'.
    target_member_id : int
        ID of the user to be added or removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.

    Raises
    ------
    ValueError
        If `member_action` is not 'add' or 'remove'.
    KeyError
        If the acting user, target member, or project does not exist.
    """
    # Validate action
    if member_action not in {"add", "remove"}:
        raise ValueError("member_action must be 'add' or 'remove'")

    # Ensure acting user exists
    if acting_user_id not in USERS:
        return False

    # Ensure target member exists (optional: allow adding unknown users? here we enforce existence)
    if target_member_id not in USERS:
        return False

    # Ensure project exists
    try:
        project = PROJECTS[prjt_id]
    except KeyError:
        return False

    # Authorization: admins can always modify, otherwise only the owner may
    acting_role = USERS.get(acting_user_id)
    if acting_role != "admin" and project["owner_id"] != acting_user_id:
        return False

    members: List[int] = project.get("members", [])

    if member_action == "add":
        # Avoid duplicate entries
        if target_member_id in members:
            return False
        members.append(target_member_id)
    else:  # remove
        if target_member_id not in members:
            return False
        members.remove(target_member_id)

    # Update the project's member list
    project["members"] = members
    return True