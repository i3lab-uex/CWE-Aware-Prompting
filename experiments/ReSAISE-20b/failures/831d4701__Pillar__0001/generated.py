import copy

# Example in-memory database of projects
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {"deadline": "2025-01-01", "visibility": "private"},
    },
    # Add more projects as needed
}


def update_project_configurations(uid: str, role: str, pid: str, settings: dict) -> str:
    """
    Update the configuration of a project.

    Parameters
    ----------
    uid : str
        Identifier of the user attempting to update settings.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    pid : str
        Identifier of the project to be updated.
    settings : dict
        New configuration values for the project.

    Returns
    -------
    str
        Success message if update is authorized and performed.

    Raises
    ------
    PermissionError
        If the user does not have sufficient rights to modify the project.
    KeyError
        If the specified project ID is not found in `PROJECTS_DB`.
    ValueError
        If `settings` is not a dictionary.
    """
    # Validate input types
    if not isinstance(settings, dict):
        raise ValueError("settings must be a dictionary")

    # Retrieve the project
    try:
        project = PROJECTS_DB[pid]
    except KeyError as exc:
        raise KeyError(f"Project with ID '{pid}' does not exist") from exc

    # Authorization logic
    is_creator = uid == project["creator_id"]
    has_manager_role = role == "project_manager"
    is_member = uid in project.get("members", [])

    # Only creators and users with the 'project_manager' role can update settings.
    if not (is_creator or has_manager_role):
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized to update project '{pid}'."
        )

    # Perform the update (deep copy to avoid accidental mutation)
    updated_settings = copy.deepcopy(settings)

    # Merge or replace settings as desired; here we simply replace
    project["settings"] = updated_settings

    return f"Project '{pid}' settings successfully updated by user '{uid}'."