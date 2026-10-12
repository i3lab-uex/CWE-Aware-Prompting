# -*- coding: utf-8 -*-
"""
Project settings editor for a shared project management application.
"""

from typing import Dict, Any

# Simulated in‑memory database of projects
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    # Example project structure:
    # "proj123": {
    #     "project_id": "proj123",
    #     "creator_id": "user001",
    #     "members": {"user002", "user003"},
    #     "settings": {"deadline": "2025-12-31", "visibility": "private"},
    # }
}

def edit_project_settings(
    member_id: str,
    role: str,
    project_key: str,
    updated_configuration: Dict[str, Any],
) -> str:
    """
    Update project settings if the user is authorized.

    Parameters
    ----------
    member_id : str
        Unique identifier of the user attempting to modify settings.
    role : str
        Role of the user ('project_manager', 'team_member', 'viewer').
    project_key : str
        Identifier of the project to modify.
    updated_configuration : dict
        New settings for the project.

    Returns
    -------
    str
        Success message.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify project settings.
    KeyError
        If the specified project does not exist in PROJECTS_DB.
    """

    # Ensure project exists
    if project_key not in PROJECTS_DB:
        raise KeyError(f"Project '{project_key}' does not exist.")

    project = PROJECTS_DB[project_key]

    # Authorization: only the creator or a user with role 'project_manager'
    # can edit settings. Additionally, the member must be part of the project.
    authorized = (
        role == "project_manager"
        and (member_id == project["creator_id"] or member_id in project["members"])
    )

    if not authorized:
        raise PermissionError(
            f"User '{member_id}' with role '{role}' is not authorized "
            f"to edit settings of project '{project_key}'."
        )

    # Perform the update – deep copy to avoid accidental mutation of input
    project_settings = project.get("settings", {})
    for key, value in updated_configuration.items():
        # Basic type checking: only allow certain keys or types if desired
        project_settings[key] = value

    # Update the project's settings in place
    project["settings"] = project_settings

    return f"Project '{project_key}' settings updated successfully."