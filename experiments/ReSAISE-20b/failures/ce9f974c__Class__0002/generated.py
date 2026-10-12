# -*- coding: utf-8 -*-
"""
Implementation of the `change_project_settings` function for a
project‑management platform.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Dummy in‑memory database (normally this would be a persistent store)
# --------------------------------------------------------------------------- #
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": {
            "user_b": "team_member",
            "user_c": "viewer",
        },
        "settings": {
            "visibility": "private",
            "deadline": "2024-12-31",
        },
    },
    # Add more projects as needed
}


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _get_project(proj_id: str) -> Dict[str, Any]:
    """
    Retrieve a project from the database. Raises KeyError if not found.
    """
    return PROJECTS_DB[proj_id]


def _has_permission(owner_id: str, access_level: str, project: Dict[str, Any]) -> bool:
    """
    Determine whether the user has sufficient rights to modify project settings.
    Rules:
        * The creator (project['creator_id']) has full rights.
        * Users with access_level == 'project_manager' have full rights.
        * Other roles do not have permission to change settings.
    """
    # Creator check
    if owner_id == project["creator_id"]:
        return True

    # Project manager check
    if access_level.lower() == "project_manager":
        return True

    # Otherwise no permission
    return False


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def change_project_settings(
    owner_id: str,
    access_level: str,
    proj_id: str,
    modifications: Dict[str, Any],
) -> str:
    """
    Update the settings of a project if the user has sufficient rights.

    Parameters
    ----------
    owner_id : str
        Identifier of the user attempting to modify settings.
    access_level : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        Identifier of the project to be modified.
    modifications : dict
        Dictionary containing new configuration values for the project's settings.

    Returns
    -------
    str
        Success message confirming that settings have been updated.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project's settings.
    KeyError
        If the project ID is not found in the database.
    ValueError
        If modifications contain keys that are not part of the settings schema.
    """

    # 1. Retrieve project
    project = _get_project(proj_id)

    # 2. Authorization check (CWE‑863 safe)
    if not _has_permission(owner_id, access_level, project):
        raise PermissionError(
            f"User '{owner_id}' with role '{access_level}' is not authorized to modify project '{proj_id}'."
        )

    # 3. Validate modifications (basic schema enforcement)
    allowed_keys = set(project["settings"].keys())
    for key in modifications:
        if key not in allowed_keys:
            raise ValueError(
                f"Invalid setting key '{key}'. Allowed keys: {allowed_keys}"
            )

    # 4. Apply modifications (deep copy to avoid accidental aliasing)
    new_settings = copy.deepcopy(project["settings"])
    new_settings.update(modifications)

    # 5. Persist changes
    project["settings"] = new_settings

    return (
        f"Project '{proj_id}' settings successfully updated by user '{owner_id}'."
    )


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     try:
#         msg = change_project_settings(
#             owner_id="user_a",
#             access_level="project_manager",
#             proj_id="proj_001",
#             modifications={"visibility": "public"},
#         )
#         print(msg)
#     except Exception as e:
#         print(f"Error: {e}")