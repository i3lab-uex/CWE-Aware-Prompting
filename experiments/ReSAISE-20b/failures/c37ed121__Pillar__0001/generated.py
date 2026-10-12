from __future__ import annotations

import copy
from typing import Dict, Any


# Example in-memory database of projects
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_123", "user_456"],
        "settings": {"visibility": "private", "deadline": "2024-12-31"},
    },
    # Additional projects can be added here
}


def adjust_project_options(
    editor_id: str,
    editor_role: str,
    proj_id: str,
    updated_settings: Dict[str, Any],
) -> str:
    """
    Update the settings of a project if the editor is authorized.

    Parameters
    ----------
    editor_id : str
        The ID of the user attempting to modify the project.
    editor_role : str
        The role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        The ID of the project to be updated.
    updated_settings : dict
        Dictionary containing the settings to update.

    Returns
    -------
    str
        Success message indicating that the project was updated.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project ID does not exist in PROJECTS_DB.
    """
    # Ensure the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization: only the creator or a user with 'project_manager' role can modify
    if editor_id != project["creator_id"] and editor_role.lower() != "project_manager":
        raise PermissionError(
            f"User '{editor_id}' with role '{editor_role}' is not authorized to modify project '{proj_id}'."
        )

    # Merge the updated settings into the existing ones
    current_settings = project.get("settings", {})
    # Create a deep copy to avoid accidental mutation of nested structures
    new_settings = copy.deepcopy(current_settings)
    for key, value in updated_settings.items():
        new_settings[key] = value

    project["settings"] = new_settings

    return f"Project '{proj_id}' settings updated successfully by user '{editor_id}'."