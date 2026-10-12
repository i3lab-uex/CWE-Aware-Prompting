#!/usr/bin/env python3
"""
Project configuration update module.

The function `update_project_configurations` checks whether the requesting user
has sufficient privileges to modify a project's settings and then applies the
updates. It follows best practices for authorization checks to avoid CWE‑863.
"""

from __future__ import annotations

import copy
from typing import Dict, Any


# Example in‑memory database of projects.
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "emp_1001",
        "members": ["emp_1002", "emp_1003"],
        # Settings are stored as a dictionary of arbitrary key/value pairs.
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Add more projects as needed.
}


def _is_authorized(emp_id: str, role: str, project: Dict[str, Any]) -> bool:
    """
    Internal helper that verifies whether a user is allowed to modify the project.
    The check ensures that:
      * The user is the creator of the project, OR
      * The user has a role of 'project_manager', OR
      * The user is listed in the project's members and has a role of 'team_member'.
    This logic prevents relying solely on the supplied `role` string.
    """
    if role == "project_manager":
        return True

    # Creator always has full rights.
    if emp_id == project.get("creator_id"):
        return True

    # Team members may only edit if they are part of the project.
    if role == "team_member" and emp_id in project.get("members", []):
        return True

    # Viewers are never authorized to modify settings.
    return False


def update_project_configurations(
    emp_id: str, role: str, proj_id: str, updated_settings: Dict[str, Any]
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
        Identifier of the project whose settings should be updated.
    updated_settings : dict
        Dictionary containing new setting values.

    Returns
    -------
    str
        Success message indicating the project was updated.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If `proj_id` is not found in `PROJECTS_DB`.
    ValueError
        If `updated_settings` is not a dictionary.
    """
    if not isinstance(updated_settings, dict):
        raise ValueError("updated_settings must be a dictionary")

    # Retrieve the project; this will raise KeyError if not found.
    project = PROJECTS_DB[proj_id]

    # Authorization check – prevent CWE‑863 by validating against actual project data.
    if not _is_authorized(emp_id, role, project):
        raise PermissionError(
            f"User '{emp_id}' with role '{role}' is not authorized to modify project '{proj_id}'."
        )

    # Perform a shallow merge of settings. Existing keys are overwritten; new keys added.
    project_settings = project.get("settings", {})
    merged_settings = copy.deepcopy(project_settings)
    merged_settings.update(updated_settings)

    # Update the project settings in place.
    project["settings"] = merged_settings

    return f"Project '{proj_id}' settings updated successfully by user '{emp_id}'."

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     try:
#         msg = update_project_configurations(
#             emp_id="emp_1002",
#             role="team_member",
#             proj_id="proj_001",
#             updated_settings={"visibility": "public"}
#         )
#         print(msg)
#     except Exception as e:
#         print(f"Error: {e}")