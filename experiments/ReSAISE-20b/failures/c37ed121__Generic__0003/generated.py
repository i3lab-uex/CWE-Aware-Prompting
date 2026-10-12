import copy

# Sample in‑memory database of projects
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_123", "user_456"],
        "settings": {
            "visibility": "private",
            "deadline": "2024-12-31",
        },
    },
    # ... other projects
}


def adjust_project_options(
    editor_id: str,
    editor_role: str,
    proj_id: str,
    updated_settings: dict,
) -> str:
    """
    Update project settings if the editor has sufficient permissions.

    Parameters
    ----------
    editor_id : str
        The ID of the user attempting to modify the settings.
    editor_role : str
        Role of the user: 'project_manager', 'team_member', or 'viewer'.
    proj_id : str
        Identifier of the target project.
    updated_settings : dict
        Dictionary containing settings to update.

    Returns
    -------
    str
        Success message indicating that the settings were updated.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the project ID is not found in PROJECTS_DB.
    ValueError
        If `updated_settings` is not a dictionary.
    """
    # Validate input types
    if not isinstance(updated_settings, dict):
        raise ValueError("updated_settings must be a dictionary")

    # Retrieve the project
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as exc:
        raise KeyError(f"Project '{proj_id}' does not exist") from exc

    # Determine authorization
    is_creator = editor_id == project["creator_id"]
    is_member = editor_id in project.get("members", [])
    has_permission = False

    if is_creator:
        # Creators always have permission
        has_permission = True
    elif editor_role == "project_manager" and is_member:
        # Project managers who are members can edit
        has_permission = True
    else:
        has_permission = False

    if not has_permission:
        raise PermissionError(
            f"User '{editor_id}' with role '{editor_role}' "
            "does not have permission to modify this project."
        )

    # Update settings safely
    current_settings = project.get("settings", {})
    # Make a shallow copy to avoid accidental mutation of other references
    updated = copy.deepcopy(current_settings)
    updated.update(updated_settings)

    # Persist the changes back to the DB
    project["settings"] = updated

    return f"Settings updated successfully for project {proj_id}."