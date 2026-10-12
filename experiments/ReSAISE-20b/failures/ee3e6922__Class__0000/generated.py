#!/usr/bin/env python3
"""
Project configuration updater.

This module provides a single function, `change_project_config`, which allows
authorized users to update the settings of an existing project.  The function
performs a strict authorization check that guards against CWE‑863
(Incorrect Authorization).

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Example in‑memory database of projects.
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": {"user_456", "user_789"},
        # Settings are stored as a nested dictionary.
        "settings": {"visibility": "private", "deadline": "2024-12-31"},
    },
    # Additional projects can be added here.
}


def _is_authorized(uid: str, role: str, project: Dict[str, Any]) -> bool:
    """
    Determine whether the user is authorized to change project settings.

    Authorization policy:
        - The creator of the project (project['creator_id']) is always allowed.
        - Users with role 'project_manager' are allowed for any project.
        - All other roles (e.g., 'team_member', 'viewer') are not allowed.

    Parameters
    ----------
    uid : str
        User ID attempting the change.
    role : str
        Role of the user.
    project : dict
        Project record from PROJECTS_DB.

    Returns
    -------
    bool
        True if the user is authorized, False otherwise.
    """
    # Ensure role comparison uses strict equality and normalisation to avoid
    # accidental authorisations due to case or whitespace.
    role_normalised = role.strip().lower()
    if uid == project["creator_id"]:
        return True
    if role_normalised == "project_manager":
        return True
    # Explicitly deny all other roles.
    return False


def change_project_config(uid: str, role: str, proj: str,
                          settings_update: Dict[str, Any]) -> str:
    """
    Update the settings of a project if the user is authorized.

    Parameters
    ----------
    uid : str
        Unique identifier of the user attempting the modification.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj : str
        Identifier of the project whose settings should be changed.
    settings_update : dict
        Updated settings for the project. Only keys present in this dictionary
        will be updated; all other existing settings remain unchanged.

    Returns
    -------
    str
        Success message indicating the project was updated.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify this project's settings.
    KeyError
        If the project ID does not exist in PROJECTS_DB.
    """
    # Validate that the project exists.
    if proj not in PROJECTS_DB:
        raise KeyError(f"Project '{proj}' does not exist.")

    project = PROJECTS_DB[proj]

    # Perform strict authorization check.
    if not _is_authorized(uid, role, project):
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized to modify "
            f"project '{proj}'."
        )

    # Ensure settings_update is a dictionary.
    if not isinstance(settings_update, dict):
        raise ValueError("settings_update must be a dictionary.")

    # Perform a safe update: create a copy to avoid mutating nested structures
    # inadvertently and then replace the project's settings.
    updated_settings = copy.deepcopy(project["settings"])
    for key, value in settings_update.items():
        updated_settings[key] = value

    # Assign the new settings back to the project.
    PROJECTS_DB[proj]["settings"] = updated_settings

    return f"Project '{proj}' settings successfully updated."


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     try:
#         msg = change_project_config(
#             uid="user_123",
#             role="project_manager",
#             proj="proj_001",
#             settings_update={"visibility": "public", "deadline": "2025-01-15"}
#         )
#         print(msg)
#     except Exception as e:
#         print(f"Error: {e}")