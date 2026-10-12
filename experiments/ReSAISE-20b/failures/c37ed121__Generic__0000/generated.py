# adjust_project_options.py

from typing import Dict, Any


# Sample in-memory database of projects
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_123", "user_456"],
        "settings": {
            "visibility": "private",
            "deadline": "2024-12-31",
        },
    },
    # Add more projects as needed
}


def adjust_project_options(
    editor_id: str,
    editor_role: str,
    proj_id: str,
    updated_settings: Dict[str, Any],
) -> str:
    """
    Modify project settings if the user has proper authorization.

    Parameters
    ----------
    editor_id : str
        ID of the user attempting to modify the project.
    editor_role : str
        Role of the user. Expected values: 'project_manager', 'team_member', 'viewer'.
    proj_id : str
        ID of the project to update.
    updated_settings : dict
        Dictionary containing setting keys and new values.

    Returns
    -------
    str
        Success message upon successful update.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify project settings.
    KeyError
        If the specified project does not exist in PROJECTS_DB.
    """
    # Validate that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization: only the creator or a user with role 'project_manager' can edit
    is_creator = editor_id == project["creator_id"]
    has_permission_role = editor_role.lower() == "project_manager"

    if not (is_creator or has_permission_role):
        raise PermissionError(
            f"User '{editor_id}' with role '{editor_role}' is not authorized to modify project settings."
        )

    # Update the settings safely
    for key, value in updated_settings.items():
        if key not in project["settings"]:
            # Optionally allow new keys; here we warn and skip
            raise KeyError(f"Setting key '{key}' does not exist in the project configuration.")
        project["settings"][key] = value

    return f"Project '{proj_id}' settings updated successfully."


# Example usage (for testing purposes only)
if __name__ == "__main__":
    try:
        result = adjust_project_options(
            editor_id="user_123",
            editor_role="project_manager",
            proj_id="proj_001",
            updated_settings={"visibility": "public", "deadline": "2025-01-15"},
        )
        print(result)
    except Exception as e:
        print(f"Error: {e}")