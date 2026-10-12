# update_project_configurations.py

"""
This module provides a function to safely modify project settings in a shared
project management platform. It enforces proper access control based on the
user's role and membership in the project, mitigating CWE‑284 (Improper Access Control).
"""

from typing import Dict

# Example in-memory database of projects
PROJECTS_DB: Dict[str, Dict] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_a", "user_b"],
        "settings": {"visibility": "private", "deadline": "2024-12-31"},
    },
    # Additional projects can be added here
}


def update_project_configurations(
    u_id: str,
    u_role: str,
    proj_id: str,
    modified_settings: Dict,
) -> str:
    """
    Update the settings of a project if the user is authorized.

    Parameters
    ----------
    u_id : str
        User ID attempting to modify the project.
    u_role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        ID of the project to update.
    modified_settings : dict
        Dictionary containing settings that should be updated.

    Returns
    -------
    str
        Success message if the update is performed.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project ID does not exist in PROJECTS_DB.
    ValueError
        If modified_settings is empty or contains invalid keys.
    """
    # Validate that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project ID '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization logic
    # Only the creator or users with role 'project_manager' can update settings.
    is_creator = u_id == project["creator_id"]
    is_project_manager = u_role.lower() == "project_manager"
    has_membership_and_team_role = (
        u_id in project["members"] and u_role.lower() == "team_member"
    )

    if not (is_creator or is_project_manager or has_membership_and_team_role):
        raise PermissionError(
            f"User '{u_id}' with role '{u_role}' is not authorized to modify project '{proj_id}'."
        )

    # Validate modified_settings
    if not isinstance(modified_settings, dict) or not modified_settings:
        raise ValueError("modified_settings must be a non-empty dictionary.")

    # Ensure only known settings keys are updated to prevent accidental injection
    allowed_keys = set(project["settings"].keys())
    if not set(modified_settings).issubset(allowed_keys):
        invalid = set(modified_settings) - allowed_keys
        raise ValueError(f"Attempted to modify unknown settings keys: {invalid}")

    # Perform the update
    project["settings"].update(modified_settings)

    return f"Project '{proj_id}' settings updated successfully by user '{u_id}'."