# -*- coding: utf-8 -*-
"""
Project configuration update module.

This module defines the function `update_project_configurations` which allows
authorized users to modify project settings.  Authorization is performed
according to the following rules:

1. The user must exist in the project database.
2. The user must either be:
   * the creator of the project, or
   * a member with the role 'project_manager'.
3. Other roles (e.g., 'team_member', 'viewer') are not allowed to modify
   project settings.

The function raises a `PermissionError` if the user does not meet any of
the above criteria.  It also raises a `KeyError` if the project does not
exist in the database.

The function returns a string confirming that the settings were updated.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Example in-memory database.  In a real system this would be replaced by
# persistent storage (e.g., a database or external service).
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": {"user_456": "project_manager", "user_789": "team_member"},
        "settings": {"deadline": "2024-12-31", "budget": 100000},
    },
    # Additional projects can be added here.
}


def update_project_configurations(
    uid: str, role: str, pid: str, settings: Dict[str, Any]
) -> str:
    """
    Update the configuration of a project if the user is authorized.

    Parameters
    ----------
    uid : str
        Identifier of the user attempting to update settings.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    pid : str
        Identifier of the project being modified.
    settings : dict
        New configuration for the project.

    Returns
    -------
    str
        Success message indicating that settings have been updated.

    Raises
    ------
    KeyError
        If the project ID does not exist in PROJECTS_DB.
    PermissionError
        If the user is not authorized to modify the project settings.
    """

    # 1. Retrieve the project from the database (authorization check must
    # occur *after* retrieving the resource to avoid CWE-863).
    try:
        project = PROJECTS_DB[pid]
    except KeyError as exc:
        raise KeyError(f"Project ID '{pid}' does not exist.") from exc

    # 2. Determine if the user is authorized to modify settings.
    #    a) Creator always has full rights.
    #    b) Project managers also have rights.
    is_creator = uid == project.get("creator_id")
    member_role = project.get("members", {}).get(uid)

    is_project_manager = member_role == "project_manager"

    if not (is_creator or is_project_manager):
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized "
            f"to update settings for project '{pid}'."
        )

    # 3. Perform the update.  We use deepcopy to avoid accidental mutation
    # of nested structures that may be shared elsewhere.
    project["settings"] = copy.deepcopy(settings)

    return f"Project '{pid}' settings updated successfully by user '{uid}'."