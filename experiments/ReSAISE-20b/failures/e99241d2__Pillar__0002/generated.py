from __future__ import annotations

import copy
from typing import Dict, Any

# Simulated database of projects
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    # Example entry
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "emp_1001",
        "members": ["emp_1002", "emp_1003"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
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
        Unique identifier of the employee attempting the update.
    role : str
        Role of the employee (e.g., 'project_manager', 'team_member', or 'viewer').
    proj_id : str
        Identifier of the project to update.
    updated_settings : dict
        Dictionary containing settings to be merged into the project's current settings.

    Returns
    -------
    str
        Success message indicating the project was updated.

    Raises
    ------
    PermissionError
        If the employee does not have permission to modify the project.
    KeyError
        If the project ID is not found in the database.
    """
    # Validate that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project ID '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization logic:
    # - The creator of the project can always modify settings.
    # - Users with role 'project_manager' can also modify settings.
    # - All other roles are denied.
    authorized = False
    if emp_id == project["creator_id"]:
        authorized = True
    elif role.lower() == "project_manager":
        authorized = True

    if not authorized:
        raise PermissionError(
            f"Employee '{emp_id}' with role '{role}' is not authorized to modify project '{proj_id}'."
        )

    # Merge updated settings into existing ones (deep copy to avoid side-effects)
    new_settings = copy.deepcopy(project["settings"])
    new_settings.update(updated_settings)

    # Apply the update
    project["settings"] = new_settings

    return f"Project '{proj_id}' settings updated successfully."