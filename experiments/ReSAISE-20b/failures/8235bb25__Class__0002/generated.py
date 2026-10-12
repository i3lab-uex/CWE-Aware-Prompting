import copy

# Sample in‑memory database of projects
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {
            "visibility": "private",
            "deadline": "2024-12-31",
        },
    },
    # Add more projects as needed
}


def update_project_configurations(u_id: str, u_role: str, proj_id: str,
                                  modified_settings: dict) -> str:
    """
    Update the settings of a project after verifying that the caller has
    sufficient permissions.

    Parameters
    ----------
    u_id : str
        ID of the user attempting the update.
    u_role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        ID of the project to be updated.
    modified_settings : dict
        Dictionary containing key/value pairs that should override the
        existing project settings.

    Returns
    -------
    str
        Success message if the update is performed.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project ID is not found in PROJECTS_DB.
    ValueError
        If `modified_settings` is empty or contains invalid keys.

    Notes
    -----
    The function performs the following security checks in order:
      1. Verify that `proj_id` exists.
      2. Ensure the caller is either:
         - The project creator, or
         - A member of the project with a role that permits editing.
      3. Validate that `modified_settings` is non‑empty and only contains
         keys that already exist in the project's settings dictionary.
    This ordering mitigates CWE‑863 by ensuring that authorization checks
    are performed *after* confirming the resource exists, preventing
    potential timing or logic errors.
    """
    # 1. Check that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project ID '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # 2. Authorization check
    is_creator = u_id == project["creator_id"]
    is_member = u_id in project.get("members", [])

    # Define which roles can edit
    editable_roles = {"project_manager"}

    authorized = (
        is_creator or
        (is_member and u_role in editable_roles)
    )

    if not authorized:
        raise PermissionError(
            f"User '{u_id}' with role '{u_role}' is not authorized "
            "to modify settings for project '{proj_id}'."
        )

    # 3. Validate modified_settings
    if not isinstance(modified_settings, dict) or not modified_settings:
        raise ValueError("`modified_settings` must be a non‑empty dictionary.")

    current_settings_keys = set(project["settings"].keys())
    invalid_keys = set(modified_settings.keys()) - current_settings_keys
    if invalid_keys:
        raise ValueError(
            f"The following keys are not valid settings: {', '.join(invalid_keys)}"
        )

    # 4. Apply updates
    project["settings"].update(copy.deepcopy(modified_settings))

    return (
        f"Settings for project '{proj_id}' successfully updated by user "
        f"'{u_id}'."
    )