import typing as _t

# Simulated database of projects.
PROJECTS_DB: dict[str, dict] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_456", "user_789"],
        "settings": {"deadline": "2024-12-31", "budget": 50000},
    },
    # Add more projects as needed.
}


def adjust_project_params(
    user_token: str,
    role: str,
    project_ident: str,
    updated_values: dict[str, _t.Any],
) -> str:
    """
    Update the settings of a project if the caller has sufficient rights.

    Parameters
    ----------
    user_token : str
        Identifier representing the user attempting to update settings.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    project_ident : str
        Identifier of the project to be modified.
    updated_values : dict[str, Any]
        New configuration values for the project.

    Returns
    -------
    str
        Success message indicating that the settings have been updated.

    Raises
    ------
    PermissionError
        If the user does not have sufficient rights to modify the project.
    KeyError
        If the specified project does not exist in PROJECTS_DB.
    """

    # 1. Validate that the project exists
    if project_ident not in PROJECTS_DB:
        raise KeyError(f"Project '{project_ident}' does not exist.")

    project = PROJECTS_DB[project_ident]

    # 2. Determine if the user is authorized
    #   - Project manager role OR creator of the project
    #   - Optionally, members can edit if they are explicitly allowed (not implemented here)
    is_creator = user_token == project["creator_id"]
    has_manager_role = role.lower() == "project_manager"

    if not (is_creator or has_manager_role):
        raise PermissionError(
            f"User '{user_token}' with role '{role}' is not authorized to update project '{project_ident}'."
        )

    # 3. Update the project's settings
    if not isinstance(updated_values, dict):
        raise ValueError("updated_values must be a dictionary.")

    # Merge existing settings with the new values
    project["settings"].update(updated_values)

    return (
        f"Project '{project_ident}' settings successfully updated by user '{user_token}'."
    )