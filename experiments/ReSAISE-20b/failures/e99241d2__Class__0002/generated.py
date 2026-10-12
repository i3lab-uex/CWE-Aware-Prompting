import copy

# Mock database of projects
PROJECTS_DB = {
    "proj1": {
        "project_id": "proj1",
        "creator_id": "emp001",
        "members": ["emp002", "emp003"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"}
    },
    # Add more projects as needed
}

def update_project_configurations(emp_id: str, role: str, proj_id: str,
                                   updated_settings: dict) -> str:
    """
    Update the settings of a project if the caller is authorized.

    Parameters
    ----------
    emp_id : str
        The unique identifier of the user attempting to modify settings.
    role : str
        Role of the caller: 'project_manager', 'team_member', or 'viewer'.
    proj_id : str
        Identifier of the project whose settings are to be updated.
    updated_settings : dict
        Dictionary containing the new settings.

    Returns
    -------
    str
        Success message upon successful update.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the project.
    KeyError
        If the project does not exist in PROJECTS_DB.
    """

    # Validate input types (basic type checks)
    if not isinstance(emp_id, str) or not isinstance(role, str):
        raise TypeError("emp_id and role must be strings")
    if not isinstance(proj_id, str):
        raise TypeError("proj_id must be a string")
    if not isinstance(updated_settings, dict):
        raise TypeError("updated_settings must be a dictionary")

    # Retrieve project data
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as exc:
        raise KeyError(f"Project '{proj_id}' not found") from exc

    # Authorization logic
    is_creator = emp_id == project["creator_id"]
    is_member = emp_id in project.get("members", [])
    authorized_roles = {"project_manager"}

    # Allow project managers to edit any project
    if role in authorized_roles:
        authorized = True
    # Allow creators to edit regardless of role
    elif is_creator:
        authorized = True
    # Team members can edit only if they are the creator (redundant above)
    elif role == "team_member" and is_creator:
        authorized = True
    else:
        authorized = False

    if not authorized:
        raise PermissionError(
            f"User '{emp_id}' with role '{role}' is not authorized to update project '{proj_id}'."
        )

    # Perform the update safely: replace settings with a copy to avoid accidental mutation
    new_settings = copy.deepcopy(updated_settings)
    project["settings"].update(new_settings)

    return f"Project '{proj_id}' settings updated successfully by user '{emp_id}'."