# -*- coding: utf-8 -*-
"""
Project configuration update module.

The function `update_project_configurations` allows a user to modify the
settings of an existing project in the shared `PROJECTS_DB`.  Only users
who are the creator or have a *project_manager* role are permitted to make
changes.  Unauthorized attempts raise a :class:`PermissionError`.

This implementation mitigates CWE-284 (Improper Access Control) by
verifying both the user identity and role before performing any update.
"""

from copy import deepcopy
from typing import Dict

# Example in-memory database of projects. In a real application this would be
# replaced by persistent storage such as a relational database or a document store.
PROJECTS_DB: Dict[str, Dict] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "emp_123",
        "members": ["emp_123", "emp_456"],
        "settings": {"visibility": "private", "deadline": "2025-12-31"},
    },
    # Additional projects can be added here...
}


def update_project_configurations(
    emp_id: str,
    role: str,
    proj_id: str,
    updated_settings: Dict,
) -> str:
    """
    Update the settings of a project if the caller is authorized.

    Parameters
    ----------
    emp_id : str
        The unique identifier of the employee making the request.
    role : str
        Role of the employee (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        Identifier of the project to update.
    updated_settings : dict
        New settings dictionary to apply.

    Returns
    -------
    str
        Success message confirming the update.

    Raises
    ------
    KeyError
        If `proj_id` does not exist in the database.
    PermissionError
        If the employee is not authorized to update the project.
    ValueError
        If `updated_settings` is not a dictionary.

    Notes
    -----
    - Only the project creator or users with role 'project_manager' may modify settings.
    - The function performs a shallow merge of `updated_settings` into the existing
      project settings; keys in `updated_settings` override existing ones.
    - The database is mutated directly; in production use transactions or locks
      to avoid race conditions.
    """
    # Validate input types
    if not isinstance(updated_settings, dict):
        raise ValueError("updated_settings must be a dictionary")

    # Retrieve the project; raise KeyError if not found
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as exc:
        raise KeyError(f"Project with ID '{proj_id}' does not exist") from exc

    # Authorization check
    is_creator = emp_id == project.get("creator_id")
    is_manager = role.lower() == "project_manager"

    if not (is_creator or is_manager):
        raise PermissionError(
            f"User '{emp_id}' with role '{role}' is not authorized to update project '{proj_id}'."
        )

    # Perform the update (merge dictionaries)
    # Use deepcopy to avoid accidental mutation of input data
    new_settings = deepcopy(project.get("settings", {}))
    new_settings.update(updated_settings)
    project["settings"] = new_settings

    return f"Project '{proj_id}' settings updated successfully by user '{emp_id}'."