#!/usr/bin/env python3
"""
update_project_configurations.py

Implements an update function for project settings with proper access control.
"""

from __future__ import annotations
import copy
from typing import Dict, Any

# Example in-memory database; replace with actual persistence layer as needed
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "emp_1001",
        "members": {"emp_1001", "emp_1002"},
        "settings": {
            "deadline": "2024-12-31",
            "visibility": "private",
        },
    },
    # Add more projects here...
}

def _is_authorized(emp_id: str, role: str, project: Dict[str, Any]) -> bool:
    """
    Determine if the user has permission to modify project settings.
    Only project managers or the creator may update settings.
    """
    if role == "project_manager":
        return True
    if emp_id == project.get("creator_id"):
        return True
    # Optionally allow team members with explicit permission in future
    return False

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
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        Identifier of the project to update.
    updated_settings : dict
        Dictionary containing settings to be merged into the existing ones.

    Returns
    -------
    str
        Success message confirming the update.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the project settings.
    KeyError
        If the specified project does not exist in PROJECTS_DB.
    """
    # Validate that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project '{proj_id}' not found.")

    project = PROJECTS_DB[proj_id]

    # Check authorization
    if not _is_authorized(emp_id, role, project):
        raise PermissionError(
            f"User '{emp_id}' with role '{role}' is not authorized to update project settings."
        )

    # Perform a deep copy of existing settings to avoid accidental mutation
    current_settings = copy.deepcopy(project.get("settings", {}))

    # Merge updated settings; updated values overwrite existing ones
    current_settings.update(updated_settings)

    # Persist the changes back to the database
    project["settings"] = current_settings

    return f"Project '{proj_id}' settings updated successfully by user '{emp_id}'."

# Example usage (comment out in production)
if __name__ == "__main__":
    try:
        msg = update_project_configurations(
            emp_id="emp_1001",
            role="project_manager",
            proj_id="proj_001",
            updated_settings={"visibility": "public", "budget": 50000},
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")