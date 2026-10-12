#!/usr/bin/env python3
"""
Module: project_settings.py

Provides a secure function to modify project settings in the
in-memory `PROJECTS_DB` dictionary.

Security focus: prevents unauthorized users from changing settings.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Sample in-memory database of projects.
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_100",
        "members": {
            "user_101": "project_manager",
            "user_102": "team_member",
        },
        "settings": {
            "visibility": "private",
            "deadline": "2024-12-31",
        },
    },
    # ... other projects
}


def change_project_settings(
    owner_id: str,
    access_level: str,
    proj_id: str,
    modifications: Dict[str, Any],
) -> str:
    """
    Update the settings of a project if the caller has sufficient rights.

    Parameters
    ----------
    owner_id : str
        The identifier of the user attempting to update settings.
    access_level : str
        Role of the user: 'project_manager', 'team_member', or 'viewer'.
    proj_id : str
        Identifier of the project to be modified.
    modifications : dict
        Dictionary containing new configuration values for the project.

    Returns
    -------
    str
        Success message indicating that settings were updated.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify project settings.
    KeyError
        If the specified project ID is not found in `PROJECTS_DB`.
    """
    # Validate that the project exists.
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project ID '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Determine if the user is authorized.
    # The creator and any project_manager member can modify settings.
    is_creator = owner_id == project["creator_id"]
    is_project_manager = (
        project["members"].get(owner_id) == "project_manager"
    )

    if not (is_creator or is_project_manager):
        raise PermissionError(
            f"User '{owner_id}' does not have permission to modify settings "
            "for project '{proj_id}'."
        )

    # Perform a shallow merge of modifications into the existing settings.
    # Use copy to avoid accidental mutation before validation if needed.
    updated_settings = copy.deepcopy(project["settings"])
    for key, value in modifications.items():
        # Basic validation: ensure key exists or is allowed to be added.
        if not isinstance(key, str):
            raise ValueError(f"Setting key must be a string: got {key!r}")
        updated_settings[key] = value

    # Apply the changes atomically.
    project["settings"] = updated_settings

    return (
        f"Project '{proj_id}' settings successfully updated by user "
        f"'{owner_id}'."
    )


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     try:
#         msg = change_project_settings(
#             owner_id="user_101",
#             access_level="project_manager",
#             proj_id="proj_001",
#             modifications={"visibility": "public", "deadline": "2025-01-15"},
#         )
#         print(msg)
#     except Exception as e:
#         print(f"Error: {e}")