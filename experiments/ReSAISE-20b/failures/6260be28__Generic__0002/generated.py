# -*- coding: utf-8 -*-
"""
Project settings modification module.
"""

from typing import Dict, Any

# Sample in-memory projects database
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_01",
        "members": ["user_02", "user_03"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Add more projects as needed
}


def modify_project_settings(
    user_id: str,
    user_role: str,
    project_id: str,
    new_settings: Dict[str, Any],
) -> str:
    """
    Modify the settings of a project after performing authorization checks.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting to modify project settings.
    user_role : str
        The role of the user (e.g., 'project_manager', 'team_member', or 'viewer').
    project_id : str
        The ID of the project being modified.
    new_settings : dict
        The new settings to apply to the project.

    Returns
    -------
    str
        Confirmation message if the update succeeded.

    Raises
    ------
    ValueError
        If the project does not exist.
    PermissionError
        If the user is not authorized to modify the settings.
    """
    # 1. Project existence check
    project = PROJECTS_DB.get(project_id)
    if not project:
        raise ValueError(f"Project with ID '{project_id}' does not exist.")

    # 2. Authorization check
    is_creator = user_id == project["creator_id"]
    is_member = user_id in project.get("members", [])

    # Only a project manager who is either the creator or a member can modify settings
    if user_role != "project_manager" or not (is_creator or is_member):
        raise PermissionError(
            f"User '{user_id}' with role '{user_role}' is not authorized "
            f"to modify settings for project '{project_id}'."
        )

    # 3. Apply the new settings
    if not isinstance(new_settings, dict):
        raise TypeError("new_settings must be a dictionary.")

    # Merge new settings into existing ones (shallow copy)
    project["settings"].update(new_settings)

    # 4. Return confirmation
    return (
        f"Settings for project '{project_id}' successfully updated by user "
        f"'{user_id}'."
    )


# Example usage (for testing purposes only)
if __name__ == "__main__":
    try:
        result = modify_project_settings(
            user_id="user_01",
            user_role="project_manager",
            project_id="proj_001",
            new_settings={"visibility": "public", "budget": 5000},
        )
        print(result)
    except Exception as exc:
        print(f"Error: {exc}")