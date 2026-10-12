# -*- coding: utf-8 -*-
"""
Project management helper functions.

This module contains the `edit_project_settings` function which allows
authorized users to update project configuration.  It performs a robust
authorization check based on the user's role and membership in the
project, mitigating CWE‑863 (Incorrect Authorization).
"""

from typing import Dict, Any

# Example in-memory database of projects.
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    # Example project entry:
    # "proj_123": {
    #     "project_id": "proj_123",
    #     "creator_id": "user_1",
    #     "members": ["user_2", "user_3"],
    #     "settings": {"visibility": "private", "deadline": "2025-01-01"}
    # }
}


def edit_project_settings(
    member_id: str,
    role: str,
    project_key: str,
    updated_configuration: Dict[str, Any]
) -> str:
    """
    Update the settings of a project if the caller is authorized.

    Parameters
    ----------
    member_id : str
        Unique identifier of the user attempting the modification.
    role : str
        Role of the user. Accepted values are:
            - 'project_manager'
            - 'team_member'
            - 'viewer'
    project_key : str
        Identifier of the project whose settings should be changed.
    updated_configuration : dict
        Dictionary containing the new configuration values.

    Returns
    -------
    str
        Success message upon successful update.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project_key does not exist in PROJECTS_DB.
    ValueError
        If role is unrecognized or updated_configuration is not a dict.

    Notes
    -----
    * Only users with the role 'project_manager' or the project creator are allowed
      to edit settings.  The function checks both the role and membership to
      prevent CWE‑863 style attacks.
    * The configuration update is performed atomically: the new settings
      replace the old ones entirely.  If a merge is required, callers can
      provide a merged dictionary beforehand.
    """
    # Basic input validation
    if not isinstance(updated_configuration, dict):
        raise ValueError("updated_configuration must be a dictionary")

    if role not in {"project_manager", "team_member", "viewer"}:
        raise ValueError(f"Unrecognized role: {role}")

    # Retrieve the project
    try:
        project = PROJECTS_DB[project_key]
    except KeyError as exc:
        raise KeyError(f"Project '{project_key}' not found") from exc

    # Authorization check: only project manager or creator can edit
    is_creator = member_id == project["creator_id"]
    has_manager_role = role == "project_manager"

    if not (is_creator or has_manager_role):
        raise PermissionError(
            f"User '{member_id}' with role '{role}' is not authorized "
            "to edit settings for project '{}'.".format(project_key)
        )

    # Perform the update
    project["settings"] = updated_configuration.copy()

    return f"Project '{project_key}' settings updated successfully."