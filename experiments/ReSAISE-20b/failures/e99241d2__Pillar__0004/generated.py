import copy

# Sample in‑memory database of projects.
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "emp_1001",
        "members": {"emp_1002", "emp_1003"},
        "settings": {
            "name": "Launch Campaign",
            "deadline": "2024-12-31",
        },
    },
    # Additional projects can be added here...
}


def update_project_configurations(
    emp_id: str,
    role: str,
    proj_id: str,
    updated_settings: dict,
) -> str:
    """
    Update the settings of a project if the caller is authorized.

    Args:
        emp_id: Unique identifier of the user attempting the modification.
        role: Role of the user. Accepted values are:
              'project_manager', 'team_member', or 'viewer'.
        proj_id: Identifier of the project to be updated.
        updated_settings: Dictionary containing new settings for the project.

    Returns:
        A success message indicating that the project has been updated.

    Raises:
        KeyError: If the project does not exist.
        PermissionError: If the user is not authorized to modify the project.
        ValueError: If updated_settings is not a dictionary or contains invalid keys.

    Notes:
        - Only the project creator or users with role 'project_manager'
          who are members of the project can modify settings.
        - The function performs a shallow copy of the incoming dictionary
          to avoid accidental mutation of caller data.
    """

    # Validate that updated_settings is a dictionary
    if not isinstance(updated_settings, dict):
        raise ValueError("updated_settings must be a dictionary")

    # Ensure the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project '{proj_id}' does not exist")

    project = PROJECTS_DB[proj_id]

    # Authorization logic
    is_creator = emp_id == project["creator_id"]
    is_member = emp_id in project.get("members", set())
    can_modify = False

    if is_creator:
        # Project creator has full rights
        can_modify = True
    elif role == "project_manager" and is_member:
        # Project managers who are also members can modify
        can_modify = True

    if not can_modify:
        raise PermissionError(
            f"User '{emp_id}' with role '{role}' is not authorized to modify project '{proj_id}'."
        )

    # Update the settings safely
    # Use copy to avoid side effects if the incoming dict is reused elsewhere
    new_settings = copy.deepcopy(project["settings"])
    for key, value in updated_settings.items():
        # Basic validation: only allow known keys
        if key not in new_settings:
            raise ValueError(f"Invalid setting key: '{key}'")
        new_settings[key] = value

    # Persist the changes
    project["settings"] = new_settings

    return f"Project '{proj_id}' settings updated successfully."