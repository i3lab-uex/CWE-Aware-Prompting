# -*- coding: utf-8 -*-
"""
Module containing the project configuration updater.
"""

from __future__ import annotations

# Simulated database of projects
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_456", "user_789"],
        "settings": {
            "deadline": "2024-12-31",
            "visibility": "private",
        },
    },
    # Additional projects can be added here
}


def update_project_configurations(
    u_id: str,
    u_role: str,
    proj_id: str,
    modified_settings: dict,
) -> str:
    """
    Update the settings of a project after performing authorization checks.

    Parameters
    ----------
    u_id : str
        ID of the user attempting the update.
    u_role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        Identifier of the project to update.
    modified_settings : dict
        Dictionary containing settings keys and their new values.

    Returns
    -------
    str
        Success message when the update is performed.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project ID is not found in the database.
    """
    # Validate that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project with ID '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization logic:
    #   - The creator can always modify.
    #   - Users with role 'project_manager' are allowed.
    #   - All other roles are denied.
    if u_id != project["creator_id"] and u_role.lower() != "project_manager":
        raise PermissionError(
            f"User '{u_id}' with role '{u_role}' is not authorized to update project '{proj_id}'."
        )

    # Perform the update (shallow merge of settings)
    project["settings"].update(modified_settings)

    return f"Settings updated successfully for project '{proj_id}'."