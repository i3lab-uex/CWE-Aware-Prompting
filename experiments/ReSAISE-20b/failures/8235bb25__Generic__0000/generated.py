from typing import Dict

# Sample in‑memory database of projects
PROJECTS_DB: Dict[str, Dict] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Add more projects as needed
}


def update_project_configurations(
    u_id: str,
    u_role: str,
    proj_id: str,
    modified_settings: Dict
) -> str:
    """
    Update project settings if the user is authorized.

    Parameters
    ----------
    u_id : str
        ID of the user attempting to modify settings.
    u_role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        ID of the project to be updated.
    modified_settings : dict
        Dictionary containing settings that should be updated.

    Returns
    -------
    str
        Success message if update is performed.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project ID does not exist in PROJECTS_DB.
    """
    # Validate that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization check:
    # Only a user with role 'project_manager' who is either the creator
    # or a member of the project can modify settings.
    if u_role != "project_manager":
        raise PermissionError("Only a project manager can update settings.")

    if u_id != project["creator_id"] and u_id not in project.get("members", []):
        raise PermissionError(
            "User is not authorized to modify this project's settings."
        )

    # Merge the modified settings into the existing ones.
    project_settings = project.setdefault("settings", {})
    if not isinstance(modified_settings, dict):
        raise ValueError("modified_settings must be a dictionary.")

    project_settings.update(modified_settings)

    return f"Settings updated successfully for project '{proj_id}'."