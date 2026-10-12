#!/usr/bin/env python3
"""
Project management utilities – change_project_settings

This module defines a single function, `change_project_settings`, which
allows authorized users to update the settings of an existing project.
"""

from __future__ import annotations

import copy
from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Mock database – in a real application this would be replaced with
# persistent storage (e.g., a SQL database or an ORM).  The structure is:
#
#   PROJECTS_DB = {
#       "proj_123": {
#           "project_id": "proj_123",
#           "creator_id": "user_001",
#           "members": {"user_002", "user_003"},
#           "settings": {"name": "Alpha", "deadline": "2024-12-31"},
#       },
#       ...
#   }
# --------------------------------------------------------------------------- #
PROJECTS_DB: Dict[str, Dict[str, Any]] = {}


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
        Role of the caller (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        Identifier of the project to modify.
    modifications : dict
        Dictionary containing the new configuration for the project.

    Returns
    -------
    str
        Success message indicating that the settings were updated.

    Raises
    ------
    KeyError
        If the project ID does not exist in `PROJECTS_DB`.
    PermissionError
        If the caller lacks permission to modify the project.
    ValueError
        If `modifications` is empty or contains invalid keys.
    """

    # Validate input arguments
    if not isinstance(modifications, dict):
        raise ValueError("modifications must be a dictionary")
    if not modifications:
        raise ValueError("No modifications provided")

    # Retrieve the project – raises KeyError if not found
    project = PROJECTS_DB[proj_id]

    # Determine whether the user is authorized to make changes
    # Rules:
    #   * The project creator can always modify.
    #   * Users with the role 'project_manager' are also allowed.
    authorized = (
        owner_id == project.get("creator_id")
        or access_level.lower() == "project_manager"
    )

    if not authorized:
        raise PermissionError(
            f"User '{owner_id}' with role '{access_level}' is not authorized to "
            "modify project settings."
        )

    # Optional: validate that modifications only contain keys present in the
    # existing settings dictionary.  This prevents accidental addition of new
    # keys that might be unsupported.
    existing_settings = project.get("settings", {})
    for key in modifications:
        if key not in existing_settings:
            raise ValueError(
                f"Modification key '{key}' is not a recognized setting."
            )

    # Apply modifications – create a shallow copy to avoid accidental mutation
    new_settings = copy.deepcopy(existing_settings)
    new_settings.update(modifications)

    # Persist the updated settings
    project["settings"] = new_settings

    return (
        f"Project '{proj_id}' settings updated successfully by user "
        f"'{owner_id}'."
    )


# --------------------------------------------------------------------------- #
# Example usage (this section would normally be in a separate test module)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Populate the mock database with a sample project
    PROJECTS_DB["proj_001"] = {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": {"user_b", "user_c"},
        "settings": {
            "name": "Initial Project",
            "deadline": "2025-01-31",
            "visibility": "private",
        },
    }

    # Successful update by the creator
    print(
        change_project_settings(
            owner_id="user_a",
            access_level="viewer",
            proj_id="proj_001",
            modifications={"deadline": "2025-02-28"},
        )
    )

    # Unauthorized attempt by a team member
    try:
        change_project_settings(
            owner_id="user_b",
            access_level="team_member",
            proj_id="proj_001",
            modifications={"visibility": "public"},
        )
    except PermissionError as e:
        print(f"Permission error: {e}")