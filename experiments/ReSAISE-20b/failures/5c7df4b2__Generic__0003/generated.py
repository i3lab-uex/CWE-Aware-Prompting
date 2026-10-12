import copy
from typing import Dict

# Simulated in‑memory database of projects
PROJECTS_DB: Dict[str, dict] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_123", "user_456"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Add more projects as needed
}


def adjust_project_params(
    user_token: str,
    role: str,
    project_ident: str,
    updated_values: Dict[str, any],
) -> str:
    """
    Update project settings if the user has sufficient rights.

    Parameters
    ----------
    user_token : str
        Identifier of the user attempting to modify settings.
    role : str
        Role of the user ('project_manager', 'team_member', 'viewer', ...).
    project_ident : str
        Identifier of the project to be updated.
    updated_values : dict
        New configuration values for the project's settings.

    Returns
    -------
    str
        Success message confirming that settings were updated.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project identifier is not found in PROJECTS_DB.
    """
    # Validate project existence
    if project_ident not in PROJECTS_DB:
        raise KeyError(f"Project '{project_ident}' does not exist.")

    project = PROJECTS_DB[project_ident]

    # Authorization logic
    is_creator = user_token == project["creator_id"]
    is_member = user_token in project.get("members", [])
    has_manager_role = role.lower() == "project_manager"

    # Only the creator or a member with project_manager role can modify settings
    if not (is_creator or (is_member and has_manager_role)):
        raise PermissionError(
            f"User '{user_token}' does not have permission to modify project '{project_ident}'."
        )

    # Ensure updated_values is a dictionary
    if not isinstance(updated_values, dict):
        raise ValueError("updated_values must be a dictionary.")

    # Perform the update in a safe way
    new_settings = copy.deepcopy(project.get("settings", {}))
    for key, value in updated_values.items():
        new_settings[key] = value

    # Commit the changes
    project["settings"] = new_settings

    return (
        f"Settings for project '{project_ident}' successfully updated by user '{user_token}'."
    )