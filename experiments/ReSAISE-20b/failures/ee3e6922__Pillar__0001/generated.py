import copy

# Example in‑memory database of projects.
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": {"user_123", "user_456"},
        "settings": {
            "name": "Initial Project",
            "visibility": "private",
            "deadline": None,
        },
    },
    # Additional projects can be added here.
}


def change_project_config(uid: str, role: str, proj: str, settings_update: dict) -> str:
    """
    Update the configuration of a project if the caller is authorized.

    Parameters
    ----------
    uid : str
        Unique identifier of the user attempting the modification.
    role : str
        Role of the caller (e.g., 'project_manager', 'team_member', or 'viewer').
    proj : str
        Identifier of the project to update.
    settings_update : dict
        Dictionary containing the new settings values.

    Returns
    -------
    str
        Success message indicating that the project was updated.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project does not exist in ``PROJECTS_DB``.
    TypeError
        If ``settings_update`` is not a dictionary.
    """
    # Validate input types
    if not isinstance(settings_update, dict):
        raise TypeError("settings_update must be a dictionary")

    # Ensure the project exists
    if proj not in PROJECTS_DB:
        raise KeyError(f"Project '{proj}' does not exist")

    project = PROJECTS_DB[proj]

    # Authorization logic
    is_creator = uid == project["creator_id"]
    has_manager_role = role.lower() == "project_manager"

    if not (is_creator or has_manager_role):
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized to modify project '{proj}'."
        )

    # Perform a deep copy of the current settings to avoid accidental mutation
    updated_settings = copy.deepcopy(project["settings"])
    # Merge updates; settings_update may override existing keys
    updated_settings.update(settings_update)

    # Persist the changes
    project["settings"] = updated_settings

    return f"Project '{proj}' settings successfully updated."