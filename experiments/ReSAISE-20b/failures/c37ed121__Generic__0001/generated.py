# -*- coding: utf-8 -*-
"""
Utility module for adjusting project options in a shared project management platform.
"""

from typing import Dict

# Sample in‑memory database of projects
PROJECTS_DB: Dict[str, Dict] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {
            "visibility": "private",
            "deadline": "2024-12-31",
        },
    },
    # Add more projects as needed
}


def adjust_project_options(
    editor_id: str,
    editor_role: str,
    proj_id: str,
    updated_settings: Dict
) -> str:
    """
    Update the settings of a project if the editor is authorized.

    Parameters
    ----------
    editor_id : str
        ID of the user attempting to modify the project.
    editor_role : str
        Role of the user (`'project_manager'`, `'team_member'`, `'viewer'`).
    proj_id : str
        Identifier of the target project.
    updated_settings : dict
        Dictionary containing settings to be updated.

    Returns
    -------
    str
        Success message indicating that the settings were updated.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project ID does not exist in `PROJECTS_DB`.
    ValueError
        If `updated_settings` is not a dictionary.
    """
    # Validate inputs
    if not isinstance(updated_settings, dict):
        raise ValueError("updated_settings must be a dictionary")

    # Retrieve the project
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as exc:
        raise KeyError(f"Project with ID '{proj_id}' does not exist.") from exc

    # Authorization logic
    is_creator = editor_id == project["creator_id"]
    is_member = editor_id in project.get("members", [])
    has_manager_role = editor_role == "project_manager"

    if not (has_manager_role and (is_creator or is_member)):
        raise PermissionError(
            f"User '{editor_id}' with role '{editor_role}' is not authorized "
            f"to modify project '{proj_id}'."
        )

    # Merge updated settings into existing ones
    project_settings = project.get("settings", {})
    if not isinstance(project_settings, dict):
        # In case settings are corrupted; reset to empty dict
        project["settings"] = {}
        project_settings = {}

    project_settings.update(updated_settings)
    project["settings"] = project_settings

    return f"Project '{proj_id}' settings updated successfully."