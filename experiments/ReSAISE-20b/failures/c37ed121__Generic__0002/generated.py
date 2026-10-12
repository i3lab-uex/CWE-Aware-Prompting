# -*- coding: utf-8 -*-
"""
Utility module for modifying project settings in a shared project management platform.
"""

from typing import Dict

# Example in‑memory database. In production this would be a persistent store.
PROJECTS_DB: Dict[str, dict] = {
    # Sample project entry
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_123", "user_456"],
        "settings": {
            "visibility": "private",
            "deadline": "2024-12-31",
        },
    },
    # Add more projects as needed...
}

# Roles that are allowed to modify project settings
ALLOWED_ROLES = {"project_manager", "creator"}


def adjust_project_options(
    editor_id: str,
    editor_role: str,
    proj_id: str,
    updated_settings: Dict,
) -> str:
    """
    Modify the settings of a project if the editor has sufficient permissions.

    Parameters
    ----------
    editor_id : str
        The ID of the user attempting to modify the project.
    editor_role : str
        Role of the editor. Expected values: 'project_manager', 'team_member', 'viewer'.
    proj_id : str
        Identifier of the project to be updated.
    updated_settings : dict
        Dictionary containing key/value pairs that should be merged into the project's settings.

    Returns
    -------
    str
        Success message confirming that the settings were updated.

    Raises
    ------
    PermissionError
        If the editor does not have permission to modify project settings.
    KeyError
        If the specified project ID does not exist in ``PROJECTS_DB``.
    """
    # Ensure the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization checks
    is_creator = editor_id == project["creator_id"]
    has_allowed_role = editor_role in ALLOWED_ROLES

    # In a real system we might also check if the user is a member or has an explicit permission flag.
    # For simplicity we consider that only creators and project managers can edit settings.
    if not (is_creator or has_allowed_role):
        raise PermissionError(
            f"User '{editor_id}' with role '{editor_role}' is not authorized to modify project settings."
        )

    # Update the project's settings safely
    if not isinstance(updated_settings, dict):
        raise ValueError("updated_settings must be a dictionary.")

    # Merge the new settings into the existing ones
    project["settings"].update(updated_settings)

    return f"Project '{proj_id}' settings updated successfully by user '{editor_id}'."