import copy

# Example in‑memory database of projects.
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "emp_123",
        "members": ["emp_123", "emp_456"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Add more projects as needed.
}


def update_project_configurations(emp_id: str, role: str, proj_id: str,
                                   updated_settings: dict) -> str:
    """
    Update the settings of a project if the user is authorized.

    Parameters
    ----------
    emp_id : str
        The unique identifier of the user attempting the modification.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', or 'viewer').
    proj_id : str
        Identifier of the project whose settings should be changed.
    updated_settings : dict
        Updated settings for the project.

    Returns
    -------
    str
        Success message upon successful update.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the project settings.
    KeyError
        If the specified project does not exist.
    """

    # Verify that the project exists.
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization logic:
    # 1. The creator of the project can always update.
    # 2. Users with role 'project_manager' are also allowed.
    # 3. Other roles (e.g., team_member, viewer) are denied by default.
    is_creator = emp_id == project["creator_id"]
    is_manager = role.lower() == "project_manager"

    if not (is_creator or is_manager):
        raise PermissionError(
            f"User '{emp_id}' with role '{role}' is not authorized to update project '{proj_id}'."
        )

    # Perform the update.
    # Use deepcopy to avoid accidental mutation of input data.
    new_settings = copy.deepcopy(updated_settings)
    project["settings"].update(new_settings)

    return f"Project '{proj_id}' settings updated successfully by user '{emp_id}'."