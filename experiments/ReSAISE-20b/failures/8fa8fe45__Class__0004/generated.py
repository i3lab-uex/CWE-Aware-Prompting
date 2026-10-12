#!/usr/bin/env python3
"""
Project preference modification with correct authorization checks.
"""

from typing import Dict, Any

# Sample in‑memory database of projects
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj1": {
        "project_id": "proj1",
        "creator_id": "user123",
        "members": ["user123", "user456"],
        "settings": {"visibility": "private", "deadline": "2025-12-31"},
    },
    # Add more projects as needed
}

def alter_project_preferences(
    member_id: str,
    member_role: str,
    proj_id: str,
    fresh_settings: Dict[str, Any],
) -> str:
    """
    Modify the settings of a project after performing strict authorization checks.

    Parameters
    ----------
    member_id : str
        The ID of the user attempting to modify the project.
    member_role : str
        Role of the user: e.g., 'project_manager', 'team_member', 'viewer'.
    proj_id : str
        The ID of the project to update.
    fresh_settings : dict
        Dictionary containing new settings values.

    Returns
    -------
    str
        Success message indicating the project was updated.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the project.
    KeyError
        If the specified project does not exist in PROJECTS_DB.
    """

    # 1. Validate that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project with ID '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # 2. Verify that the member is part of the project
    if member_id not in project["members"]:
        raise PermissionError(
            f"User '{member_id}' is not a member of project '{proj_id}'."
        )

    # 3. Enforce correct authorization logic
    #   - Only the creator or a user with role 'project_manager' can modify settings.
    is_creator = member_id == project["creator_id"]
    is_project_manager = member_role.lower() == "project_manager"

    if not (is_creator or is_project_manager):
        raise PermissionError(
            f"User '{member_id}' does not have permission to modify project settings."
        )

    # 4. Apply the new settings securely
    #   - Avoid direct assignment to prevent accidental injection of malicious keys.
    for key, value in fresh_settings.items():
        # Basic validation: ensure the key is a string and not attempting to modify protected fields
        if not isinstance(key, str):
            raise ValueError(f"Setting key '{key}' must be a string.")
        if key in {"project_id", "creator_id", "members"}:
            raise ValueError(f"Modification of '{key}' is not allowed.")
        # Update the setting
        project["settings"][key] = value

    return f"Project '{proj_id}' settings updated successfully."


# Example usage (for manual testing)
if __name__ == "__main__":
    try:
        msg = alter_project_preferences(
            member_id="user123",
            member_role="project_manager",
            proj_id="proj1",
            fresh_settings={"visibility": "public", "deadline": "2026-01-15"},
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")