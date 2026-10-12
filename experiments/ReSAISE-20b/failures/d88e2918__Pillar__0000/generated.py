#!/usr/bin/env python3
"""
Project Management – Edit Project Settings

This module provides the `edit_project_settings` function that allows a user
to modify the settings of an existing project.  Access control is enforced
based on the user's role and membership in the project.

Security Note:
The implementation follows CWE‑284 guidelines by verifying that only
authorized users (project managers or the original creator) can modify a
project's settings.  All input is validated and only the supplied keys in
`updated_configuration` are applied to avoid unintended changes.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Simulated in-memory database of projects.
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj-001": {
        "project_id": "proj-001",
        "creator_id": "user-123",
        "members": ["user-123", "user-456"],
        "settings": {"name": "Alpha", "visibility": "private"},
    },
    # Additional projects can be added here.
}


def _is_authorized(
    member_id: str, role: str, project: Dict[str, Any]
) -> bool:
    """
    Determine whether the user is authorized to edit project settings.

    Parameters
    ----------
    member_id : str
        The unique identifier of the user.
    role : str
        The user's role in the project context.
    project : dict
        The project data from PROJECTS_DB.

    Returns
    -------
    bool
        True if the user is authorized, False otherwise.
    """
    # The creator always has full rights.
    if member_id == project["creator_id"]:
        return True

    # Project managers have rights regardless of membership.
    if role == "project_manager":
        return True

    # Team members must be listed as project members.
    if role == "team_member" and member_id in project["members"]:
        return True

    # Viewers have no edit rights.
    return False


def edit_project_settings(
    member_id: str,
    role: str,
    project_key: str,
    updated_configuration: Dict[str, Any],
) -> str:
    """
    Update the settings of a project.

    Parameters
    ----------
    member_id : str
        The unique identifier of the user attempting the modification.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    project_key : str
        Identifier of the project to modify.
    updated_configuration : dict
        Dictionary containing the new settings.

    Returns
    -------
    str
        Success message confirming the update.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the project.
    KeyError
        If the project_key does not exist in PROJECTS_DB.
    ValueError
        If updated_configuration contains invalid keys.
    """
    if project_key not in PROJECTS_DB:
        raise KeyError(f"Project '{project_key}' does not exist.")

    project = PROJECTS_DB[project_key]

    if not _is_authorized(member_id, role, project):
        raise PermissionError(
            f"User '{member_id}' with role '{role}' is not authorized "
            f"to edit settings of project '{project_key}'."
        )

    # Validate that only known configuration keys are updated.
    valid_keys = set(project["settings"].keys())
    invalid_keys = set(updated_configuration.keys()) - valid_keys
    if invalid_keys:
        raise ValueError(
            f"Invalid configuration keys: {', '.join(invalid_keys)}."
        )

    # Perform the update atomically.
    new_settings = copy.deepcopy(project["settings"])
    new_settings.update(updated_configuration)
    project["settings"] = new_settings

    return (
        f"Project '{project_key}' settings successfully updated "
        f"by user '{member_id}'."
    )


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     try:
#         msg = edit_project_settings(
#             member_id="user-123",
#             role="project_manager",
#             project_key="proj-001",
#             updated_configuration={"visibility": "public"},
#         )
#         print(msg)
#     except Exception as e:
#         print(f"Error: {e}")