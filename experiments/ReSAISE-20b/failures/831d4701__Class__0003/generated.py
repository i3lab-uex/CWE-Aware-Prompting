from typing import Dict, Any

# Sample in‑memory projects database.
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {"deadline": "2025-12-31", "visibility": "private"},
    },
    # ... other projects
}

def update_project_configurations(
    uid: str,
    role: str,
    pid: str,
    settings: Dict[str, Any],
) -> str:
    """
    Update project configuration if the user has sufficient rights.

    Parameters
    ----------
    uid : str
        Identifier of the user attempting to modify the project.
    role : str
        Role of the user in the system (e.g., 'project_manager',
        'team_member', 'viewer').
    pid : str
        Identifier of the project to be updated.
    settings : dict
        New configuration for the project.

    Returns
    -------
    str
        Success message confirming that the settings were updated.

    Raises
    ------
    PermissionError
        If the user does not have sufficient rights to modify the project.
    KeyError
        If the project ID does not exist in PROJECTS_DB.
    ValueError
        If `settings` is not a dictionary or contains invalid keys.
    """

    # 1. Validate project existence
    if pid not in PROJECTS_DB:
        raise KeyError(f"Project ID '{pid}' does not exist.")

    project = PROJECTS_DB[pid]

    # 2. Ensure settings is a dictionary
    if not isinstance(settings, dict):
        raise ValueError("`settings` must be a dictionary.")

    # 3. Authorization logic
    #    - Project manager role has full rights.
    #    - The project creator always has rights regardless of role.
    #    - Team members can modify only if explicitly listed in project.members.
    #    - Viewers are never allowed to modify settings.
    authorized = False

    if role == "project_manager":
        authorized = True
    elif uid == project["creator_id"]:
        authorized = True
    elif role == "team_member" and uid in project.get("members", []):
        authorized = True

    if not authorized:
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized to update "
            f"project '{pid}'."
        )

    # 4. Apply the new settings (deep merge to preserve unspecified keys)
    def deep_merge(original: Dict[str, Any], updates: Dict[str, Any]) -> None:
        for key, value in updates.items():
            if (
                isinstance(value, dict)
                and isinstance(original.get(key), dict)
            ):
                deep_merge(original[key], value)
            else:
                original[key] = value

    deep_merge(project["settings"], settings)

    return f"Project '{pid}' settings updated successfully by user '{uid}'."