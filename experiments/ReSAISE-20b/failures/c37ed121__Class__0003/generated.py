import copy

# Mock database of projects
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_1",
        "members": ["user_2", "user_3"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    "proj_002": {
        "project_id": "proj_002",
        "creator_id": "user_4",
        "members": ["user_5"],
        "settings": {"deadline": "2025-03-15", "visibility": "public"},
    },
}


def adjust_project_options(
    editor_id: str,
    editor_role: str,
    proj_id: str,
    updated_settings: dict,
) -> str:
    """
    Modify the settings of a project after performing proper authorization checks.

    Args:
        editor_id: ID of the user attempting to modify settings.
        editor_role: Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
        proj_id: ID of the project to update.
        updated_settings: Dictionary containing settings to be updated.

    Returns:
        A success message indicating the project was updated.

    Raises:
        PermissionError: If the user is not authorized to modify the project.
        KeyError: If the project ID does not exist in PROJECTS_DB.
    """
    # 1. Validate that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project {proj_id} does not exist.")

    project = PROJECTS_DB[proj_id]

    # 2. Authorization logic
    # Only the project creator or a user with role 'project_manager' can modify settings.
    # Additionally, if the editor is listed as a member but not a manager or creator,
    # they are denied.
    if editor_id != project["creator_id"] and editor_role.lower() != "project_manager":
        raise PermissionError(
            f"User {editor_id} with role '{editor_role}' is not authorized to modify project {proj_id}"
        )

    # 3. Perform the update
    # Make a shallow copy to avoid accidental mutation if settings contain nested dicts.
    new_settings = copy.deepcopy(project["settings"])
    for key, value in updated_settings.items():
        # Optional: Validate keys or types here if needed
        new_settings[key] = value

    project["settings"] = new_settings

    return f"Project {proj_id} settings successfully updated."


# Example usage
if __name__ == "__main__":
    try:
        result = adjust_project_options(
            editor_id="user_1",
            editor_role="project_manager",
            proj_id="proj_001",
            updated_settings={"visibility": "public"},
        )
        print(result)
    except Exception as e:
        print(f"Error: {e}")