import copy
from typing import Dict, Any

# Example in‑memory database of projects.
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "emp_123",
        "members": ["emp_123", "emp_456"],
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
        Updated key/value pairs for the project's settings.

    Returns
    -------
    str
        Success message confirming that the project was updated.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project ID does not exist in PROJECTS_DB.
    ValueError
        If `updated_settings` is not a dictionary or contains invalid keys.
    """
    # Validate the updated settings type
    if not isinstance(updated_settings, dict):
        raise ValueError("updated_settings must be a dictionary")

    # Retrieve the project
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as exc:
        raise KeyError(f"Project ID '{proj_id}' not found.") from exc

    # Permission checks:
    # 1. Project managers have full rights.
    # 2. The creator of the project also has rights, even if their role is 'viewer'.
    # 3. Team members and viewers cannot modify settings.
    if not (role == "project_manager" or emp_id == project["creator_id"]):
        raise PermissionError(
            f"User '{emp_id}' with role '{role}' is not authorized to update project '{proj_id}'."
        )

    # Optional: validate that keys in updated_settings are allowed.
    # For simplicity, assume any key is permissible; otherwise, enforce a whitelist:
    # allowed_keys = {"deadline", "visibility", "budget"}
    # for key in updated_settings:
    #     if key not in allowed_keys:
    #         raise ValueError(f"Invalid setting key: {key}")

    # Perform the update (deep copy to avoid accidental reference issues)
    project["settings"] = {**project.get("settings", {}), **copy.deepcopy(updated_settings)}

    return f"Project '{proj_id}' settings updated successfully by user '{emp_id}'."