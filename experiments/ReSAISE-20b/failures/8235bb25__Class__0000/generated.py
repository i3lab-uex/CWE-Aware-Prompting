import typing as _t

# Sample in‑memory database of projects
PROJECTS_DB: dict[str, dict] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_123", "user_456"],
        "settings": {"visibility": "private", "deadline": "2024-12-31"},
    },
    # Additional projects can be added here
}


def update_project_configurations(
    u_id: str,
    u_role: str,
    proj_id: str,
    modified_settings: dict[str, _t.Any],
) -> str:
    """
    Update project settings if the user is authorized.

    Parameters
    ----------
    u_id : str
        ID of the user attempting to modify the project.
    u_role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        Identifier of the project to update.
    modified_settings : dict[str, Any]
        Settings key/value pairs to be updated.

    Returns
    -------
    str
        Success message when the update is performed.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project ID is not found in the database.
    """
    # Ensure the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization: only the creator or a user with role 'project_manager' can update
    is_creator = u_id == project["creator_id"]
    is_project_manager = u_role.lower() == "project_manager"

    if not (is_creator or is_project_manager):
        raise PermissionError(
            f"User '{u_id}' with role '{u_role}' is not authorized to update project '{proj_id}'."
        )

    # Perform the update
    project["settings"].update(modified_settings)

    return f"Project '{proj_id}' settings successfully updated by user '{u_id}'."