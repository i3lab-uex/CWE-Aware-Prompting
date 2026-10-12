# -*- coding: utf-8 -*-
"""
Project Settings Modification Module

This module provides a secure implementation for updating project settings
in a simulated project management platform. The function `change_project_settings`
performs proper authorization checks to prevent CWE-863 (Incorrect Authorization)
and ensures that only users with sufficient rights can modify a project's
configuration.
"""

from typing import Dict

# Simulated database of projects.
PROJECTS_DB: Dict[str, dict] = {
    "proj-001": {
        "project_id": "proj-001",
        "creator_id": "user-123",
        "members": ["user-456", "user-789"],
        "settings": {"name": "Alpha", "visibility": "private"},
    },
    # Additional projects can be added here.
}


def change_project_settings(
    owner_id: str,
    access_level: str,
    proj_id: str,
    modifications: Dict[str, any],
) -> str:
    """
    Update the settings of a project if the user has sufficient rights.

    Parameters
    ----------
    owner_id : str
        Identifier of the user attempting to update settings.
    access_level : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        Identifier of the project to modify.
    modifications : dict
        Dictionary containing new configuration key/value pairs.

    Returns
    -------
    str
        Success message confirming the update.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the project.
    KeyError
        If the specified project does not exist in PROJECTS_DB.
    """

    # 1. Verify that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # 2. Authorization check
    # Only the creator or a user with role 'project_manager' may modify settings.
    if not (
        owner_id == project["creator_id"] or access_level.lower() == "project_manager"
    ):
        raise PermissionError(
            f"User '{owner_id}' with role '{access_level}' is not authorized "
            "to modify project settings."
        )

    # 3. Apply modifications safely
    for key, value in modifications.items():
        if key not in project["settings"]:
            # Optionally allow adding new keys; otherwise raise an error
            project["settings"][key] = value
        else:
            # Replace existing key with new value
            project["settings"][key] = value

    return f"Project '{proj_id}' settings updated successfully by user '{owner_id}'."