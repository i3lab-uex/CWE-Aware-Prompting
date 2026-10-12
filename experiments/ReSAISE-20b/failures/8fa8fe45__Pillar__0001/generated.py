# -*- coding: utf-8 -*-
"""
Implementation of the `alter_project_preferences` function.
"""

from __future__ import annotations

import copy
from typing import Dict, List


# Simulated in‑memory database of projects.
PROJECTS_DB: Dict[str, Dict] = {
    # Example project entry
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_123", "user_456"],
        # Default settings
        "settings": {
            "visibility": "private",
            "notifications": True,
            "deadline": None,
        },
    },
    # Add more projects as needed
}


def alter_project_preferences(
    member_id: str,
    member_role: str,
    proj_id: str,
    fresh_settings: Dict,
) -> str:
    """
    Modify the settings of a project.

    Parameters
    ----------
    member_id : str
        ID of the user attempting to modify settings.
    member_role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        Identifier of the project to be updated.
    fresh_settings : dict
        Dictionary containing settings that should be applied.

    Returns
    -------
    str
        Success message if the operation is authorized and completed.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project settings.
    KeyError
        If the specified project does not exist.
    """
    # Validate that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project with ID '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization logic:
    # 1. The creator can always modify settings.
    # 2. Users with role 'project_manager' are also allowed.
    # 3. All other roles are denied.
    authorized = False
    if member_id == project["creator_id"]:
        authorized = True
    elif member_role.lower() == "project_manager":
        # Ensure the user is actually a member of the project
        if member_id in project.get("members", []):
            authorized = True

    if not authorized:
        raise PermissionError(
            f"User '{member_id}' with role '{member_role}' is not authorized to modify project settings."
        )

    # Perform a deep copy of the current settings to avoid accidental mutation
    updated_settings = copy.deepcopy(project.get("settings", {}))
    # Merge fresh settings; new keys are added, existing keys are overwritten
    updated_settings.update(fresh_settings)

    # Update the project's settings in the database
    project["settings"] = updated_settings

    return f"Project '{proj_id}' settings successfully updated."


# Example usage (uncomment to test):
# try:
#     msg = alter_project_preferences(
#         member_id="user_123",
#         member_role="project_manager",
#         proj_id="proj_001",
#         fresh_settings={"visibility": "public", "deadline": "2025-12-31"}
#     )
#     print(msg)
# except Exception as e:
#     print(f"Error: {e}")