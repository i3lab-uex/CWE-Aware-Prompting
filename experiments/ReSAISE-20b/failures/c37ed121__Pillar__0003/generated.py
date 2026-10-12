import copy

# Example in‑memory database of projects.
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_100",
        "members": ["user_101", "user_102"],
        # settings can be any key/value pairs
        "settings": {
            "deadline": "2024-12-31",
            "visibility": "private",
        },
    },
    # Additional projects can be added here...
}


def adjust_project_options(editor_id: str, editor_role: str,
                           proj_id: str, updated_settings: dict) -> str:
    """
    Update the settings of a project if the editor has proper authorization.

    Parameters
    ----------
    editor_id : str
        ID of the user attempting to modify project settings.
    editor_role : str
        Role of the user. Expected values are 'project_manager',
        'team_member', or 'viewer'.
    proj_id : str
        ID of the project to update.
    updated_settings : dict
        Dictionary containing setting keys and their new values.

    Returns
    -------
    str
        Success message if update is performed.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the project ID is unknown.
    """
    # Validate input types
    if not isinstance(editor_id, str) or not isinstance(editor_role, str):
        raise TypeError("editor_id and editor_role must be strings")
    if not isinstance(proj_id, str):
        raise TypeError("proj_id must be a string")
    if not isinstance(updated_settings, dict):
        raise TypeError("updated_settings must be a dictionary")

    # Retrieve the project from the database
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as exc:
        raise KeyError(f"Project with ID '{proj_id}' not found") from exc

    # Authorization logic:
    # 1. The creator can always modify settings.
    # 2. A user with role 'project_manager' is allowed to modify any project settings.
    # 3. A team member can modify settings only if they are part of the project members list.
    # 4. Viewers or any other roles are denied.
    authorized = False

    if editor_id == project["creator_id"]:
        authorized = True
    elif editor_role == "project_manager":
        authorized = True
    elif editor_role == "team_member" and editor_id in project.get("members", []):
        authorized = True

    if not authorized:
        raise PermissionError(
            f"User '{editor_id}' with role '{editor_role}' is not authorized "
            "to modify project settings."
        )

    # Perform a deep copy to avoid accidental mutations from caller
    new_settings = copy.deepcopy(project.get("settings", {}))
    # Update the settings with the provided values
    new_settings.update(updated_settings)

    # Persist the updated settings back to the database
    project["settings"] = new_settings

    return f"Project '{proj_id}' settings successfully updated."