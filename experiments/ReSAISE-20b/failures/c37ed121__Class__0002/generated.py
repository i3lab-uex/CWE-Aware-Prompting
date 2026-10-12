import typing

# Mock database of projects for demonstration purposes.
# In a real application this would be replaced with persistent storage or an ORM.
PROJECTS_DB: dict[str, dict] = {
    "proj1": {
        "project_id": "proj1",
        "creator_id": "user123",
        "members": ["user123", "user456"],
        "settings": {
            "deadline": "2024-12-31",
            "visibility": "private"
        }
    },
    # Additional projects can be added here.
}

def adjust_project_options(
    editor_id: str,
    editor_role: str,
    proj_id: str,
    updated_settings: typing.Dict[str, typing.Any]
) -> str:
    """
    Update project settings if the editor has sufficient permissions.

    Args:
        editor_id: ID of the user attempting to modify settings.
        editor_role: Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
        proj_id: ID of the target project.
        updated_settings: Dictionary with settings to update.

    Returns:
        A success message if the update is performed.

    Raises:
        PermissionError: If the user lacks permission to modify the project.
        KeyError: If the project does not exist.
    """
    # Ensure the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization logic:
    # - Only the creator or a user with role 'project_manager' can modify settings.
    #   (Assumes that creators are implicitly project managers.)
    if editor_id != project["creator_id"] and editor_role.lower() != "project_manager":
        raise PermissionError("You do not have permission to modify this project's settings.")

    # Perform the update in a safe manner
    if not isinstance(updated_settings, dict):
        raise ValueError("updated_settings must be a dictionary.")

    # Merge new settings with existing ones
    project["settings"].update(updated_settings)

    return f"Project '{proj_id}' settings successfully updated."

# Example usage (would normally be part of unit tests or the application logic)
if __name__ == "__main__":
    try:
        msg = adjust_project_options(
            editor_id="user123",
            editor_role="project_manager",
            proj_id="proj1",
            updated_settings={"visibility": "public", "deadline": "2025-01-15"}
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")