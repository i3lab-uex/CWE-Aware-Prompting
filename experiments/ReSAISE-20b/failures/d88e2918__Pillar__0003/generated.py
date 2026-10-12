# -*- coding: utf-8 -*-
"""
Project settings editor for a shared project management application.
"""

from typing import Dict

# Simulated in‑memory database of projects
PROJECTS_DB: Dict[str, Dict] = {
    # Example project entry
    "proj_123": {
        "project_id": "proj_123",
        "creator_id": "user_001",
        "members": ["user_001", "user_002"],
        "settings": {"name": "Sample Project", "deadline": "2024-12-31"},
    },
    # Additional projects can be added here
}


def edit_project_settings(
    member_id: str,
    role: str,
    project_key: str,
    updated_configuration: Dict
) -> str:
    """
    Update the settings of a project if the caller is authorized.

    Parameters
    ----------
    member_id : str
        The unique identifier of the user attempting the modification.
    role : str
        Role of the user, e.g., 'project_manager', 'team_member', or 'viewer'.
    project_key : str
        Identifier of the project whose settings should be changed.
    updated_configuration : dict
        Updated settings for the project.

    Returns
    -------
    str
        Success message confirming the update.

    Raises
    ------
    PermissionError
        If the user is not authorized to edit the project settings.
    KeyError
        If the specified project does not exist.
    ValueError
        If `updated_configuration` is not a dictionary.
    """

    # Validate input types
    if not isinstance(updated_configuration, dict):
        raise ValueError("updated_configuration must be a dictionary")

    # Retrieve the project from the database
    try:
        project = PROJECTS_DB[project_key]
    except KeyError as exc:
        raise KeyError(f"Project '{project_key}' not found") from exc

    # Authorization logic
    is_creator = member_id == project.get("creator_id")
    is_project_manager_role = role.lower() == "project_manager"
    has_member_access = member_id in project.get("members", [])

    # The user must be either the creator or have an explicit manager role
    if not (is_creator or is_project_manager_role):
        raise PermissionError(
            f"User '{member_id}' does not have permission to edit project settings"
        )

    # Optional: Ensure the user is a member of the project
    if not has_member_access:
        raise PermissionError(
            f"User '{member_id}' is not a member of project '{project_key}'"
        )

    # Apply the updates
    project_settings = project.setdefault("settings", {})
    project_settings.update(updated_configuration)

    # Return a success message
    return f"Project '{project_key}' settings updated successfully by user '{member_id}'."