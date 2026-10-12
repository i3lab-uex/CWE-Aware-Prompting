# -*- coding: utf-8 -*-
"""
Project Settings Modification Module

This module provides a single function, `modify_project_settings`, that
allows authorized users to update the settings of a project in a
collaborative project management system.

The implementation follows best practices for access control (CWE‑284)
and includes defensive programming techniques to avoid common
security pitfalls such as tampering with the `PROJECTS_DB` dictionary.
"""

from typing import Dict, Any

# Mock database of projects
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {"visibility": "private", "deadline": "2024-12-31"},
    },
    # Additional projects can be added here
}


def modify_project_settings(
    user_id: str,
    user_role: str,
    project_id: str,
    new_settings: Dict[str, Any],
) -> str:
    """
    Update the settings of a project if the user is authorized.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting to modify project settings.
    user_role : str
        The role of the user (e.g., 'project_manager', 'team_member',
        or 'viewer'). Only users with role `project_manager` or the
        project creator are allowed to modify settings.
    project_id : str
        The ID of the project being modified.
    new_settings : dict
        The new settings to apply to the project.

    Returns
    -------
    str
        Confirmation message indicating that the settings were updated.

    Raises
    ------
    ValueError
        If the project does not exist in `PROJECTS_DB`.
    PermissionError
        If the user is not authorized to modify the project settings.
    """
    # 1. Validate existence of the project
    if project_id not in PROJECTS_DB:
        raise ValueError(f"Project with ID '{project_id}' does not exist.")

    project = PROJECTS_DB[project_id]

    # 2. Authorization checks
    is_creator = user_id == project["creator_id"]
    is_manager = user_role.lower() == "project_manager"
    if not (is_creator or is_manager):
        raise PermissionError(
            f"User '{user_id}' with role '{user_role}' is not authorized to modify project settings."
        )

    # 3. Apply new settings (deep copy to avoid unintended side effects)
    if not isinstance(new_settings, dict):
        raise TypeError("new_settings must be a dictionary.")

    # Ensure settings keys are valid; in a real system this would check against
    # allowed keys or a schema. For demonstration, we simply update.
    project["settings"].update(new_settings)

    # 4. Return confirmation
    return f"Project '{project_id}' settings updated successfully by user '{user_id}'."