import copy

# Sample in‑memory projects database
PROJECTS_DB = {
    "proj1": {
        "project_id": "proj1",
        "creator_id": "user123",
        "members": ["user123", "user456"],
        "settings": {"visibility": "private", "deadline": "2024-12-31"}
    },
    # more projects...
}

def change_project_config(uid: str, role: str, proj: str, settings_update: dict) -> str:
    """
    Update the settings of a project if the user is authorized.

    Parameters
    ----------
    uid : str
        Unique identifier of the requesting user.
    role : str
        Role of the user ('project_manager', 'team_member', or 'viewer').
    proj : str
        Identifier of the project to update.
    settings_update : dict
        Dictionary containing updated settings keys and values.

    Returns
    -------
    str
        Success message upon successful update.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify project settings.
    KeyError
        If the specified project does not exist.
    ValueError
        If `settings_update` is not a dictionary or contains invalid keys.
    """
    # Validate input types
    if not isinstance(settings_update, dict):
        raise ValueError("settings_update must be a dictionary")

    # Retrieve the project; raise KeyError if missing
    try:
        project = PROJECTS_DB[proj]
    except KeyError as exc:
        raise KeyError(f"Project '{proj}' not found") from exc

    # Authorization logic:
    # 1. User must be the creator or have role 'project_manager'.
    # 2. Additionally, if not the creator, user must be listed as a member.
    is_creator = uid == project["creator_id"]
    has_manager_role = role == "project_manager"
    is_member = uid in project.get("members", [])

    if not (is_creator or has_manager_role):
        raise PermissionError(
            "Only the project creator or a project manager can modify settings."
        )
    if not is_creator and not is_member:
        raise PermissionError(
            "User must be a project member to modify settings."
        )

    # Perform the update in a safe manner
    # Create a shallow copy to avoid accidental reference sharing
    new_settings = copy.deepcopy(project["settings"])
    for key, value in settings_update.items():
        # Basic validation: ensure the key exists in current settings
        if key not in new_settings:
            raise ValueError(f"Invalid setting key: {key}")
        # Additional type checks can be added here
        new_settings[key] = value

    # Commit the changes
    project["settings"] = new_settings

    return f"Project '{proj}' settings updated successfully."