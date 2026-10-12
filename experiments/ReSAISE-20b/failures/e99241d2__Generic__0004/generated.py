from __future__ import annotations

import copy
from typing import Dict, Any

# Sample in-memory database of projects.
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
    Update settings of a project if the user is authorized.

    Parameters
    ----------
    emp_id : str
        Unique identifier of the employee requesting the update.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', or 'viewer').
    proj_id : str
        Identifier of the project to update.
    updated_settings : dict
        Dictionary containing the settings to be updated.

    Returns
    -------
    str
        Success message confirming update.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify project settings.
    KeyError
        If the specified project ID is not found in the database.
    ValueError
        If updated_settings is not a dictionary or contains invalid keys.
    """
    # Validate input types
    if not isinstance(updated_settings, dict):
        raise ValueError("updated_settings must be a dictionary")

    # Retrieve the project
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as exc:
        raise KeyError(f"Project ID '{proj_id}' does not exist") from exc

    # Permission check: allow if user is creator or has role 'project_manager'
    authorized = (
        emp_id == project["creator_id"] or role.lower() == "project_manager"
    )
    if not authorized:
        raise PermissionError(
            f"User '{emp_id}' with role '{role}' is not authorized to update project settings."
        )

    # Optional: ensure only allowed keys are updated
    allowed_keys = {"deadline", "visibility", "budget", "description"}
    for key in updated_settings:
        if key not in allowed_keys:
            raise ValueError(f"Invalid setting key: '{key}'")

    # Perform the update atomically
    project["settings"].update(copy.deepcopy(updated_settings))

    return f"Project '{proj_id}' settings updated successfully by user '{emp_id}'."