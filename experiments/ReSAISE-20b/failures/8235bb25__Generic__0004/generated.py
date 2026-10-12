import copy

# Example in-memory projects database.
# In a real system this would be replaced by a persistent datastore.
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_01",
        "members": ["user_01", "user_02"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # ... other projects ...
}


def update_project_configurations(u_id: str, u_role: str, proj_id: str,
                                  modified_settings: dict) -> str:
    """
    Update the settings of a project if the user is authorized.

    Parameters
    ----------
    u_id : str
        ID of the user attempting to modify the project.
    u_role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        Identifier of the project to update.
    modified_settings : dict
        Dictionary containing settings to be updated.

    Returns
    -------
    str
        Success message if the update is performed.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project does not exist in PROJECTS_DB.
    """
    # Ensure project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization logic:
    # 1. The user must be the creator or a project manager.
    # 2. Additionally, they should be listed as a member of the project.
    is_creator = u_id == project["creator_id"]
    has_role_permission = u_role in {"project_manager", "team_member"}

    if not (is_creator or has_role_permission):
        raise PermissionError(
            f"User '{u_id}' with role '{u_role}' is not authorized to modify project '{proj_id}'."
        )

    if u_id not in project["members"]:
        raise PermissionError(
            f"User '{u_id}' is not a member of project '{proj_id}'."
        )

    # Merge the modified settings into existing settings safely.
    # Use a copy to avoid mutating original dict unintentionally.
    updated_settings = copy.deepcopy(project["settings"])
    for key, value in modified_settings.items():
        # Basic validation: ensure keys are strings and values are JSON-serializable.
        if not isinstance(key, str):
            raise ValueError(f"Setting key '{key}' must be a string.")
        updated_settings[key] = value

    # Persist the changes back to the database.
    project["settings"] = updated_settings

    return f"Project '{proj_id}' settings successfully updated by user '{u_id}'."