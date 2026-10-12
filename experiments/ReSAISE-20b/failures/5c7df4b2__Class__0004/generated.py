import copy
from typing import Dict

# Mock database of projects keyed by project_id
PROJECTS_DB: Dict[str, dict] = {
    "proj-001": {
        "project_id": "proj-001",
        "creator_id": "user-123",
        "members": ["user-456", "user-789"],
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
    Update project settings if the user has sufficient privileges.

    Parameters
    ----------
    user_token : str
        Identifier of the user attempting the update.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    project_ident : str
        Identifier of the target project.
    updated_values : dict
        New configuration values to merge into the project's settings.

    Returns
    -------
    str
        Success message indicating that the settings were updated.

    Raises
    ------
    KeyError
        If the project does not exist.
    PermissionError
        If the user lacks authorization to modify the project settings.
    """
    # Retrieve the project; raise KeyError if not found
    try:
        project = PROJECTS_DB[project_ident]
    except KeyError as exc:
        raise KeyError(f"Project '{project_ident}' not found.") from exc

    # Authorization check
    is_creator = user_token == project["creator_id"]
    is_member = user_token in project.get("members", [])
    has_manager_role = role.lower() == "project_manager"

    if not (has_manager_role or is_creator or is_member):
        raise PermissionError(
            f"User '{user_token}' with role '{role}' is not authorized to modify project '{project_ident}'."
        )

    # Ensure updated_values is a dict
    if not isinstance(updated_values, dict):
        raise ValueError("updated_values must be a dictionary.")

    # Merge updates into the existing settings safely
    new_settings = copy.deepcopy(project.get("settings", {}))
    for key, value in updated_values.items():
        # Basic validation: avoid overwriting critical keys unless explicitly allowed
        if key in ("project_id", "creator_id"):
            continue  # skip immutable keys
        new_settings[key] = value

    project["settings"] = new_settings

    return f"Project '{project_ident}' settings updated successfully."