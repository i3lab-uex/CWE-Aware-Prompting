#!/usr/bin/env python3
"""
Project participant management module.

Provides a single function `control_project_participants` that allows a project
owner or an administrator to add or remove members from a project.

The module relies on two global dictionaries:

    PROJECTS: dict[int, dict[str, Any]]
        Maps a project ID to a dictionary containing:
            - 'owner_id': int   # user id of the owner
            - 'members' : set[int]  # set of member user ids

    USERS: dict[int, str]
        Maps a user ID to a role string. The role can be either
            - 'admin'   # privileged user
            - 'user'    # regular user

Both dictionaries are expected to be populated elsewhere in the application.
"""

from __future__ import annotations
import typing as _t

# Example data structures; replace or populate in your application.
PROJECTS: dict[int, dict[str, _t.Any]] = {}
USERS: dict[int, str] = {}

def control_project_participants(
    acting_user_id: int,
    prj_id: int,
    action_type: str,
    target_id: int,
) -> bool:
    """
    Add or remove a user from a project.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user performing the action.
    prj_id : int
        The project ID to modify.
    action_type : str
        Either 'add' or 'remove'.
    target_id : int
        The user ID to add or remove.

    Returns
    -------
    bool
        ``True`` if the operation succeeded, otherwise ``False``.

    Notes
    -----
    - Only a project owner or an administrator can modify participants.
    - Adding an already existing member is considered a no‑op and returns
      ``True``.
    - Removing a non‑member is considered a no‑op and returns ``True``.
    - The function performs minimal validation to avoid accidental data
      corruption but does not raise exceptions for user errors.
    """
    # Basic validation of action_type
    if action_type not in {"add", "remove"}:
        return False

    # Ensure project exists
    project = PROJECTS.get(prj_id)
    if not project:
        return False

    # Verify acting user is authorized
    role = USERS.get(acting_user_id)
    if role != "admin" and project.get("owner_id") != acting_user_id:
        return False

    # Ensure target user exists
    if target_id not in USERS:
        return False

    members = project.setdefault("members", set())

    if action_type == "add":
        # Add only if not already a member
        members.add(target_id)
    else:  # action_type == "remove"
        members.discard(target_id)

    return True