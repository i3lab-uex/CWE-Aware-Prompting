#!/usr/bin/env python3
"""
A minimal in‑memory project management module that allows a user to modify
project settings with proper authorization checks.
"""

from __future__ import annotations

import copy
from typing import Dict, Any


# --- Mock database -----------------------------------------------------------

PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    # Example project
    "proj_123": {
        "project_id": "proj_123",
        "creator_id": "user_1",
        "members": ["user_2", "user_3"],
        # Settings are stored as a dictionary; defaults for illustration
        "settings": {"visibility": "private", "deadline": None},
    }
}


# --- Core function -----------------------------------------------------------

def modify_project_settings(
    user_id: str,
    user_role: str,
    project_id: str,
    new_settings: Dict[str, Any],
) -> str:
    """
    Modify the settings of a project if the user is authorized.

    Parameters
    ----------
    user_id : str
        ID of the user attempting to modify settings.
    user_role : str
        Role of the user. Allowed roles for modification are:
        'project_manager', 'creator'.
    project_id : str
        ID of the project to modify.
    new_settings : dict
        Dictionary containing the new settings.

    Returns
    -------
    str
        Confirmation message if the update succeeded.

    Raises
    ------
    ValueError
        If the project does not exist or if `new_settings` is not a dict.
    PermissionError
        If the user is not authorized to modify the project settings.

    Notes
    -----
    - The function performs a shallow copy of `new_settings` to avoid accidental
      mutation of the caller's dictionary.
    - Only users with role 'project_manager' or the project's creator may
      modify settings. Other roles are rejected.
    """

    # Validate input types
    if not isinstance(new_settings, dict):
        raise ValueError("new_settings must be a dictionary")

    # Fetch the project
    project = PROJECTS_DB.get(project_id)
    if not project:
        raise ValueError(f"Project with ID '{project_id}' does not exist")

    # Authorization logic
    is_creator = project.get("creator_id") == user_id
    has_manager_role = user_role.lower() == "project_manager"

    if not (is_creator or has_manager_role):
        raise PermissionError(
            f"User '{user_id}' with role '{user_role}' is not authorized to modify project settings"
        )

    # Apply the new settings
    # We merge existing settings with new ones, giving precedence to new_settings.
    updated_settings = copy.deepcopy(project["settings"])
    updated_settings.update(copy.deepcopy(new_settings))
    project["settings"] = updated_settings

    return (
        f"Project '{project_id}' settings successfully updated by user '{user_id}'."
    )


# --- Example usage -----------------------------------------------------------

if __name__ == "__main__":
    try:
        result = modify_project_settings(
            user_id="user_1",
            user_role="project_manager",
            project_id="proj_123",
            new_settings={"visibility": "public", "deadline": "2024-12-31"},
        )
        print(result)
    except Exception as exc:
        print(f"Error: {exc}")