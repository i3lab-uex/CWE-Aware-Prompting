# -*- coding: utf-8 -*-

"""
Project Management – Settings Update

This module provides a single function `adjust_project_params` that
allows authorized users to update project settings. It enforces
access control by checking the user role and membership in the target
project, thereby mitigating CWE-284: Improper Access Control.
"""

from typing import Dict

# Sample in-memory database of projects
PROJECTS_DB: Dict[str, Dict] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": {"user_a", "user_b"},
        "settings": {
            "deadline": "2024-12-31",
            "budget": 10000,
        },
    },
    # Add more projects as needed
}


def adjust_project_params(
    user_token: str,
    role: str,
    project_ident: str,
    updated_values: Dict
) -> str:
    """
    Update the settings of a project if the user has sufficient rights.

    Parameters
    ----------
    user_token : str
        Identifier of the user attempting to update settings.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    project_ident : str
        Identifier of the target project.
    updated_values : dict
        New configuration values for the project's settings.

    Returns
    -------
    str
        Success message confirming the update.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the project settings.
    KeyError
        If the specified project does not exist in PROJECTS_DB.
    """

    # Validate that the project exists
    if project_ident not in PROJECTS_DB:
        raise KeyError(f"Project '{project_ident}' does not exist.")

    project = PROJECTS_DB[project_ident]

    # Define which roles are allowed to modify settings
    ALLOWED_ROLES = {"project_manager", "team_lead"}

    # Authorization checks
    is_creator = user_token == project["creator_id"]
    is_member = user_token in project.get("members", set())
    has_role = role.lower() in ALLOWED_ROLES

    if not (is_creator or (has_role and is_member)):
        raise PermissionError(
            f"User '{user_token}' with role '{role}' is not authorized to update project settings."
        )

    # Perform the update – only keys that exist in current settings are allowed
    for key, value in updated_values.items():
        if key not in project["settings"]:
            # Prevent adding arbitrary new settings unless explicitly allowed
            raise KeyError(f"Setting '{key}' does not exist in the project configuration.")
        project["settings"][key] = value

    return f"Project '{project_ident}' settings updated successfully by user '{user_token}'."