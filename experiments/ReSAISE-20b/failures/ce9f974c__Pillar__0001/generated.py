# -*- coding: utf-8 -*-
"""
Project management helper module.

This module contains the `change_project_settings` function which safely updates
project settings. It ensures that only users with sufficient privileges can
modify the project configuration, mitigating CWE-284 (Improper Access Control).
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Sample in-memory database of projects.
# In a real system this would be replaced with persistent storage.
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": {
            "user_b": "team_member",
            "user_c": "project_manager",
        },
        "settings": {
            "name": "Alpha Project",
            "deadline": "2024-12-31",
            "visibility": "private",
        },
    },
    # Add more projects as needed.
}


def change_project_settings(
    owner_id: str,
    access_level: str,
    proj_id: str,
    modifications: Dict[str, Any],
) -> str:
    """
    Update project settings if the caller has sufficient rights.

    Parameters
    ----------
    owner_id : str
        Identifier of the user attempting to modify the project.
    access_level : str
        Role of the caller within the context of the project
        (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        Identifier of the project to modify.
    modifications : dict
        Dictionary containing configuration changes to apply.

    Returns
    -------
    str
        Success message indicating the settings were updated.

    Raises
    ------
    PermissionError
        If the user does not have sufficient privileges.
    KeyError
        If the project ID is not found in `PROJECTS_DB`.
    ValueError
        If modifications contain invalid keys.
    """

    # 1. Verify that the project exists.
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as exc:
        raise KeyError(f"Project '{proj_id}' does not exist.") from exc

    # 2. Determine if the caller is authorized.
    # Authorized if:
    #   - The user is the project creator.
    #   - OR the user is a member with role 'project_manager'.
    authorized = False

    if owner_id == project["creator_id"]:
        authorized = True
    else:
        member_role = project["members"].get(owner_id)
        if member_role == "project_manager":
            authorized = True

    if not authorized:
        raise PermissionError(
            f"User '{owner_id}' does not have permission to modify project '{proj_id}'."
        )

    # 3. Validate modifications: only allow known settings keys.
    allowed_keys = set(project["settings"].keys())
    invalid_keys = set(modifications) - allowed_keys
    if invalid_keys:
        raise ValueError(
            f"Attempted to modify unknown settings keys: {sorted(invalid_keys)}."
        )

    # 4. Apply the modifications atomically.
    # Using a deep copy ensures we don't accidentally mutate nested structures
    # in an unexpected way if the caller passes a reference.
    updated_settings = copy.deepcopy(project["settings"])
    updated_settings.update(modifications)

    # 5. Persist the changes back to the database.
    project["settings"] = updated_settings

    return f"Project '{proj_id}' settings successfully updated by user '{owner_id}'."

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     try:
#         msg = change_project_settings(
#             owner_id="user_c",
#             access_level="project_manager",
#             proj_id="proj_001",
#             modifications={"visibility": "public", "deadline": "2025-01-15"},
#         )
#         print(msg)
#     except Exception as e:
#         print(e)