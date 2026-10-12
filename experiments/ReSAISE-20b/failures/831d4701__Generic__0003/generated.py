import copy

# Sample in‑memory projects database
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {"visibility": "private", "deadline": "2025-12-31"},
    },
    # ... other projects ...
}

def update_project_configurations(uid: str, role: str, pid: str, settings: dict) -> str:
    """
    Update the configuration of a project.

    Parameters
    ----------
    uid : str
        Identifier of the user attempting to modify the project.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    pid : str
        Identifier of the project to be updated.
    settings : dict
        New configuration values for the project.

    Returns
    -------
    str
        Success message indicating that settings have been updated.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the project.
    KeyError
        If the project ID does not exist in PROJECTS_DB.
    ValueError
        If `settings` is not a dictionary or contains invalid keys.

    Notes
    -----
    - Only the project creator or users with role 'project_manager'
      are allowed to update settings.
    - The function performs a shallow merge of the provided `settings`
      into the existing project configuration.
    """
    # Validate input types
    if not isinstance(settings, dict):
        raise ValueError("`settings` must be a dictionary")

    # Ensure project exists
    if pid not in PROJECTS_DB:
        raise KeyError(f"Project ID '{pid}' does not exist")

    project = PROJECTS_DB[pid]

    # Authorization check
    authorized_roles = {"project_manager"}
    is_creator = uid == project["creator_id"]
    has_role_authorized = role in authorized_roles

    if not (is_creator or has_role_authorized):
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized to update project '{pid}'."
        )

    # Perform a shallow merge of settings
    updated_settings = copy.deepcopy(project["settings"])
    updated_settings.update(settings)

    # Update the project in the database
    PROJECTS_DB[pid]["settings"] = updated_settings

    return f"Settings updated for project '{pid}'."