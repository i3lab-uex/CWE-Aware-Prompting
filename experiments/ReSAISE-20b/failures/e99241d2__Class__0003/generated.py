import copy

# Simulated in‑memory database of projects.
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "emp_100",
        "members": {"emp_101", "emp_102"},
        "settings": {
            "name": "Alpha",
            "visibility": "private",
            "deadline": "2024-12-31"
        }
    },
    # Additional projects can be added here.
}

def update_project_configurations(emp_id: str,
                                   role: str,
                                   proj_id: str,
                                   updated_settings: dict) -> str:
    """
    Update the settings of a project if the caller is authorized.

    Parameters
    ----------
    emp_id : str
        Unique identifier of the user attempting the update.
    role : str
        Role of the caller ('project_manager', 'team_member', or 'viewer').
    proj_id : str
        Identifier of the project to update.
    updated_settings : dict
        Dictionary containing new settings for the project.

    Returns
    -------
    str
        Success message indicating that the update was performed.

    Raises
    ------
    PermissionError
        If the caller does not have permission to modify the project.
    KeyError
        If the specified project ID is not found in the database.
    ValueError
        If `updated_settings` is not a dictionary or contains invalid keys.
    """
    # 1. Validate input types
    if not isinstance(updated_settings, dict):
        raise ValueError("updated_settings must be a dictionary.")

    # 2. Retrieve the project
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as exc:
        raise KeyError(f"Project ID '{proj_id}' not found.") from exc

    # 3. Authorization check
    #   - Only the creator or a user with role 'project_manager' may update settings.
    #   - Use strict equality checks to avoid CWE‑863 pitfalls.
    is_creator = emp_id == project["creator_id"]
    is_manager_role = role == "project_manager"

    if not (is_creator or is_manager_role):
        raise PermissionError(
            f"User '{emp_id}' with role '{role}' is not authorized to update project settings."
        )

    # 4. Validate that the keys in updated_settings exist in current settings
    allowed_keys = set(project["settings"].keys())
    for key in updated_settings:
        if key not in allowed_keys:
            raise ValueError(f"Invalid setting key: '{key}'. Allowed keys: {allowed_keys}")

    # 5. Apply the update atomically
    new_settings = copy.deepcopy(project["settings"])
    new_settings.update(updated_settings)
    project["settings"] = new_settings

    return f"Project '{proj_id}' settings updated successfully by user '{emp_id}'."