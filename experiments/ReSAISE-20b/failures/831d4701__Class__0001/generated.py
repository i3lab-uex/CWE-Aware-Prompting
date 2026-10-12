# -*- coding: utf-8 -*-

"""
Module providing project configuration update functionality.
"""

from typing import Dict

# Example in-memory database of projects
PROJECTS_DB: Dict[str, dict] = {
    "proj_1": {
        "project_id": "proj_1",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Add more projects as needed
}


def update_project_configurations(
    uid: str,
    role: str,
    pid: str,
    settings: Dict
) -> str:
    """
    Update the configuration of a project.

    Parameters
    ----------
    uid : str
        Identifier of the user attempting to update settings.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    pid : str
        Identifier of the project to modify.
    settings : dict
        New configuration values for the project.

    Returns
    -------
    str
        Success message indicating that settings have been updated.

    Raises
    ------
    PermissionError
        If the user does not have sufficient rights to modify the project.
    KeyError
        If the project ID is not found in `PROJECTS_DB`.
    """
    # Ensure the project exists
    if pid not in PROJECTS_DB:
        raise KeyError(f"Project '{pid}' does not exist.")

    project = PROJECTS_DB[pid]

    # Authorization check: only the creator or a user with role 'project_manager'
    # can modify project settings.
    is_creator = uid == project.get("creator_id")
    has_manager_role = role.lower() == "project_manager"

    # CWE-863 mitigation: perform a strict check and avoid ambiguous logic.
    if not (is_creator or has_manager_role):
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized to update project '{pid}'."
        )

    # Perform the update safely
    if not isinstance(settings, dict):
        raise ValueError("Settings must be a dictionary.")

    # Merge new settings into existing ones
    project_settings = project.get("settings", {})
    project_settings.update(settings)
    project["settings"] = project_settings

    return f"Project '{pid}' settings updated successfully by user '{uid}'."