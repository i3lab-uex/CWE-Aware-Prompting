import copy

# Sample in‑memory projects database (for illustration only)
PROJECTS_DB = {
    "proj1": {
        "project_id": "proj1",
        "creator_id": "user_123",
        "members": ["user_123", "user_456"],
        "settings": {"visibility": "private", "deadline": "2024-12-31"}
    },
    # ... other projects
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
        Identifier of the project to modify.
    settings_update : dict
        Dictionary containing the new/changed settings.

    Returns
    -------
    str
        Success message confirming the update.

    Raises
    ------
    PermissionError
        If the caller does not have permission to modify the project.
    KeyError
        If the specified project does not exist in `PROJECTS_DB`.
    """
    # Validate input types
    if not isinstance(uid, str) or not isinstance(role, str) \
       or not isinstance(proj, str) or not isinstance(settings_update, dict):
        raise TypeError("Invalid argument types provided.")

    # Retrieve the project
    try:
        project = PROJECTS_DB[proj]
    except KeyError as exc:
        raise KeyError(f"Project '{proj}' not found.") from exc

    # Authorization logic:
    #   * The creator can modify any settings.
    #   * A project manager who is a member can also modify settings.
    #   * All other roles are denied.
    is_creator = uid == project["creator_id"]
    is_manager_member = role == "project_manager" and uid in project.get("members", [])

    if not (is_creator or is_manager_member):
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized to modify project '{proj}'."
        )

    # Perform a shallow merge of the settings
    new_settings = copy.deepcopy(project.get("settings", {}))
    new_settings.update(settings_update)

    # Persist the updated settings
    project["settings"] = new_settings

    return f"Project '{proj}' settings updated successfully by user '{uid}'."