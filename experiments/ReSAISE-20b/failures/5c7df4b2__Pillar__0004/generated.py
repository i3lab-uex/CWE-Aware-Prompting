from __future__ import annotations

import copy
from typing import Dict, Any


# Mock database of projects. In a real application this would be replaced by persistent storage.
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_456", "user_789"],
        "settings": {"visibility": "private", "deadline": "2024-12-31"},
    },
    # Additional projects can be added here.
}


def adjust_project_params(
    user_token: str,
    role: str,
    project_ident: str,
    updated_values: Dict[str, Any],
) -> str:
    """
    Update project settings if the user has sufficient privileges.

    Args:
        user_token: Identifier of the user attempting to modify settings.
        role: Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
        project_ident: Identifier of the target project.
        updated_values: Dictionary with new configuration values for the project.

    Returns:
        A success message indicating that settings were updated.

    Raises:
        PermissionError: If the user does not have permission to modify the project.
        KeyError: If the specified project does not exist in PROJECTS_DB.
    """
    # Verify that the project exists
    if project_ident not in PROJECTS_DB:
        raise KeyError(f"Project '{project_ident}' does not exist.")

    project = PROJECTS_DB[project_ident]

    # Enforce proper access control:
    # 1. Only a project manager is allowed to update settings.
    # 2. The creator of the project implicitly has managerial rights.
    # 3. Optionally, members could be allowed if role is 'project_manager'.
    has_permission = False
    if role == "project_manager":
        # Project managers can update settings for any project they are part of.
        if (
            user_token == project["creator_id"]
            or user_token in project.get("members", [])
        ):
            has_permission = True

    if not has_permission:
        raise PermissionError(
            f"User '{user_token}' with role '{role}' is not authorized to modify project '{project_ident}'."
        )

    # Merge the updated values into the existing settings.
    # Use a deep copy to avoid accidental mutation of input data.
    new_settings = copy.deepcopy(project["settings"])
    new_settings.update(updated_values)

    # Apply the update to the project database.
    project["settings"] = new_settings

    return f"Project '{project_ident}' settings successfully updated."


# Example usage (for testing purposes only; remove or comment out in production)
if __name__ == "__main__":
    try:
        message = adjust_project_params(
            user_token="user_456",
            role="project_manager",
            project_ident="proj_001",
            updated_values={"visibility": "public", "priority": "high"},
        )
        print(message)
    except Exception as e:
        print(f"Error: {e}")