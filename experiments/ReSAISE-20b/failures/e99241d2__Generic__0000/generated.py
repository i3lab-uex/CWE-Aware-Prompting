from typing import Dict, Any

# Sample in‑memory database of projects.
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "emp_1001",
        "members": ["emp_1002", "emp_1003"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Additional projects can be added here.
}


def update_project_configurations(
    emp_id: str,
    role: str,
    proj_id: str,
    updated_settings: Dict[str, Any],
) -> str:
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
        Success message indicating that the project settings were updated.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify project settings.
    KeyError
        If the specified project does not exist in the database.
    """
    # Validate that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project with ID '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Determine if the user has permission to update settings.
    # Permissions:
    #   - Project manager role can edit any project they created or are a member of.
    #   - Team members can only edit projects where they are listed as members.
    #   - Viewers cannot modify settings.
    is_creator = emp_id == project["creator_id"]
    is_member = emp_id in project.get("members", [])

    authorized = False
    if role == "project_manager":
        # Project managers can edit projects they created or are part of.
        authorized = is_creator or is_member
    elif role == "team_member":
        # Team members can edit projects they belong to.
        authorized = is_member
    else:
        # Viewers or other roles cannot modify settings.
        authorized = False

    if not authorized:
        raise PermissionError(
            f"User '{emp_id}' with role '{role}' is not authorized "
            "to update settings for project '{}'.".format(proj_id)
        )

    # Merge the updated settings into existing settings.
    if not isinstance(updated_settings, dict):
        raise ValueError("updated_settings must be a dictionary.")

    project["settings"].update(updated_settings)

    return (
        f"Project '{proj_id}' settings successfully updated by user "
        f"'{emp_id}'."
    )