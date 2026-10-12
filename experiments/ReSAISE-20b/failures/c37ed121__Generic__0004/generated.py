import copy

# Sample in-memory database of projects.
PROJECTS_DB = {
    "proj_1": {
        "project_id": "proj_1",
        "creator_id": "user_100",
        "members": ["user_101", "user_102"],
        # default settings
        "settings": {
            "visibility": "private",
            "deadline": None,
            "notifications": True,
        },
    },
    # more projects can be added here
}

def adjust_project_options(
    editor_id: str,
    editor_role: str,
    proj_id: str,
    updated_settings: dict
) -> str:
    """
    Update the settings of a project if the editor is authorized.

    Parameters
    ----------
    editor_id : str
        ID of the user attempting to modify settings.
    editor_role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        ID of the project to be updated.
    updated_settings : dict
        Dictionary containing key/value pairs that should replace or add to the project's settings.

    Returns
    -------
    str
        Success message if the update was applied.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project settings.
    KeyError
        If `proj_id` is not found in PROJECTS_DB.
    """

    # Retrieve the project; raise KeyError if it doesn't exist
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as exc:
        raise KeyError(f"Project with ID '{proj_id}' does not exist.") from exc

    # Authorization logic:
    #   - The creator can always modify settings.
    #   - A user with role 'project_manager' is also allowed to modify settings.
    #   - All other roles are forbidden.
    if editor_id != project["creator_id"] and editor_role.lower() != "project_manager":
        raise PermissionError(
            f"User '{editor_id}' with role '{editor_role}' is not authorized to modify project settings."
        )

    # Perform a safe merge of the updated settings into the existing ones.
    # We avoid mutating the original dict directly to prevent accidental side effects.
    new_settings = copy.deepcopy(project["settings"])
    for key, value in updated_settings.items():
        # Basic validation: ensure the key is a string and not empty
        if not isinstance(key, str) or not key:
            raise ValueError(f"Invalid setting key: {key!r}")
        # Optional: enforce type checks for known settings
        if key == "visibility" and value not in {"public", "private"}:
            raise ValueError(f"Invalid visibility value: {value!r}")
        if key == "notifications" and not isinstance(value, bool):
            raise ValueError(f"'notifications' must be a boolean, got {type(value).__name__}")
        new_settings[key] = value

    # Update the project in the database
    project["settings"] = new_settings

    return f"Project '{proj_id}' settings updated successfully."