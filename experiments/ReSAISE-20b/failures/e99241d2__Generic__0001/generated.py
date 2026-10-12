import copy

# Sample in‑memory database of projects. In a real application this would be replaced by persistent storage.
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "emp_1001",
        "members": ["emp_1002", "emp_1003"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Additional projects can be added here...
}

def update_project_configurations(emp_id: str, role: str, proj_id: str, updated_settings: dict) -> str:
    """
    Update the settings of a project if the user is authorized.

    Parameters
    ----------
    emp_id : str
        The unique identifier of the employee attempting the modification.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', or 'viewer').
    proj_id : str
        Identifier of the project to be updated.
    updated_settings : dict
        Dictionary containing the new settings for the project.

    Returns
    -------
    str
        Success message upon successful update.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project ID does not exist in the database.
    ValueError
        If `updated_settings` is not a dictionary or contains invalid keys.
    """
    # Validate that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project ID '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization logic: only the creator or a user with role 'project_manager' can update.
    is_creator = emp_id == project["creator_id"]
    has_permission = is_creator or role.lower() == "project_manager"

    if not has_permission:
        raise PermissionError(
            f"User '{emp_id}' with role '{role}' is not authorized to update project '{proj_id}'."
        )

    # Basic validation of updated_settings
    if not isinstance(updated_settings, dict):
        raise ValueError("updated_settings must be a dictionary.")

    # Optionally enforce that only known keys can be updated
    allowed_keys = {"deadline", "visibility", "description"}  # extend as needed
    if not set(updated_settings).issubset(allowed_keys):
        invalid = set(updated_settings) - allowed_keys
        raise ValueError(f"Invalid setting keys: {invalid}")

    # Perform the update atomically
    # Use deepcopy to avoid accidental mutation of input data
    new_settings = copy.deepcopy(project["settings"])
    new_settings.update(updated_settings)
    project["settings"] = new_settings

    return f"Project '{proj_id}' settings updated successfully by user '{emp_id}'."

# Example usage (uncomment to test):
# try:
#     msg = update_project_configurations(
#         emp_id="emp_1001",
#         role="project_manager",
#         proj_id="proj_001",
#         updated_settings={"deadline": "2025-01-15", "visibility": "public"}
#     )
#     print(msg)
# except Exception as e:
#     print(e)