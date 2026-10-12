# adjust_project_options.py

from typing import Dict, Any

# Example in-memory projects database
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_456", "user_789"],
        "settings": {
            "visibility": "private",
            "deadline": "2024-12-31"
        }
    },
    # ... other projects
}


def adjust_project_options(
    editor_id: str,
    editor_role: str,
    proj_id: str,
    updated_settings: Dict[str, Any]
) -> str:
    """
    Modify the settings of a project after performing authorization checks.

    Parameters
    ----------
    editor_id : str
        ID of the user attempting to modify the project.
    editor_role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        Identifier of the project to update.
    updated_settings : dict
        Dictionary containing settings to be updated.

    Returns
    -------
    str
        Success message indicating that the project was updated.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project ID is not found in PROJECTS_DB.
    """

    # Ensure project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project ID '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization: only a 'project_manager' who is either the creator
    # or a member of the project can modify settings.
    if editor_role != "project_manager":
        raise PermissionError("Only users with the role 'project_manager' can modify project settings.")

    if editor_id != project["creator_id"] and editor_id not in project.get("members", []):
        raise PermissionError("User is not authorized to modify this project's settings.")

    # Perform the update (merge existing settings with new ones)
    project["settings"].update(updated_settings)

    return f"Project '{proj_id}' settings successfully updated."


# Example usage (for testing purposes only)
if __name__ == "__main__":
    try:
        result = adjust_project_options(
            editor_id="user_123",
            editor_role="project_manager",
            proj_id="proj_001",
            updated_settings={"visibility": "public", "deadline": "2025-01-15"}
        )
        print(result)
    except Exception as e:
        print(f"Error: {e}")