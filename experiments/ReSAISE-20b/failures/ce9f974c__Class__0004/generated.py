# -*- coding: utf-8 -*-

"""
A minimal example of secure project settings modification with proper authorization checks.
"""

from typing import Dict

# Mock database of projects
PROJECTS_DB: Dict[str, dict] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_123", "user_456"],
        "settings": {"deadline": "2025-12-31", "visibility": "private"},
    },
    # Additional projects can be added here
}


def change_project_settings(
    owner_id: str,
    access_level: str,
    proj_id: str,
    modifications: Dict
) -> str:
    """
    Update project settings if the user has sufficient rights.

    Parameters
    ----------
    owner_id : str
        Identifier of the user attempting to modify settings.
    access_level : str
        Role of the user. Expected values: 'project_manager', 'team_member', 'viewer'.
    proj_id : str
        Identifier of the target project.
    modifications : dict
        Dictionary containing key/value pairs to update in the project's settings.

    Returns
    -------
    str
        Success message indicating that the settings were updated.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify project settings.
    KeyError
        If the specified project does not exist in PROJECTS_DB.
    """

    # Validate that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project with id '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization logic:
    # 1. Only the creator or a project_manager can modify settings.
    # 2. The access_level must be explicitly checked against known roles to avoid injection.
    is_creator = owner_id == project["creator_id"]
    is_project_manager = access_level.lower() == "project_manager"

    if not (is_creator or is_project_manager):
        raise PermissionError(
            f"User '{owner_id}' with role '{access_level}' is not authorized to modify settings of project '{proj_id}'."
        )

    # Update the project's settings
    if not isinstance(modifications, dict):
        raise ValueError("modifications must be a dictionary.")

    project["settings"].update(modifications)

    return f"Project '{proj_id}' settings updated successfully."


# Example usage (for testing purposes only; remove or comment out in production)
if __name__ == "__main__":
    try:
        msg = change_project_settings(
            owner_id="user_123",
            access_level="project_manager",
            proj_id="proj_001",
            modifications={"visibility": "public", "deadline": "2026-01-15"},
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")