import copy

# Example in-memory database of projects
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Add more projects as needed
}

def adjust_project_options(editor_id: str, editor_role: str, proj_id: str,
                           updated_settings: dict) -> str:
    """
    Modify project settings if the editor has sufficient permissions.

    Parameters
    ----------
    editor_id : str
        ID of the user attempting to modify settings.
    editor_role : str
        Role of the user ('project_manager', 'team_member', 'viewer').
    proj_id : str
        Identifier of the project to update.
    updated_settings : dict
        Dictionary containing settings to be updated.

    Returns
    -------
    str
        Success message upon successful update.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the project settings.
    KeyError
        If the specified project does not exist.
    ValueError
        If updated_settings is not a dictionary or empty.
    """
    # Validate input types and non-empty settings
    if not isinstance(updated_settings, dict) or not updated_settings:
        raise ValueError("updated_settings must be a non-empty dictionary")

    # Retrieve the project
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as exc:
        raise KeyError(f"Project with ID '{proj_id}' not found") from exc

    # Authorization logic
    is_creator = editor_id == project["creator_id"]
    has_manager_privilege = editor_role == "project_manager"

    if not (is_creator or has_manager_privilege):
        raise PermissionError(
            f"User '{editor_id}' with role '{editor_role}' is not authorized "
            "to modify project settings."
        )

    # Perform a safe update: clone current settings to avoid accidental mutation
    new_settings = copy.deepcopy(project["settings"])
    new_settings.update(updated_settings)

    # Commit the updated settings back to the database
    project["settings"] = new_settings

    return f"Project '{proj_id}' settings updated successfully."

# Example usage:
if __name__ == "__main__":
    try:
        msg = adjust_project_options(
            editor_id="user_a",
            editor_role="project_manager",
            proj_id="proj_001",
            updated_settings={"visibility": "public", "deadline": "2025-01-15"},
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")