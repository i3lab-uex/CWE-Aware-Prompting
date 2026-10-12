# SPDX-License-Identifier: MIT
"""
Project Settings Modification Module

This module implements the `modify_project_settings` function which allows
authorized users to update project settings in a collaborative environment.
The implementation follows the CWE-284 (Improper Access Control) guidelines
by strictly validating user permissions before performing any modifications.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Example in‑memory database of projects.
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    # Example project entry:
    # "proj_123": {
    #     "project_id": "proj_123",
    #     "creator_id": "user_1",
    #     "members": ["user_2", "user_3"],
    #     "settings": {"visibility": "private", "deadline": "2025-12-31"}
    # }
}


def modify_project_settings(
    user_id: str,
    user_role: str,
    project_id: str,
    new_settings: Dict[str, Any],
) -> str:
    """
    Update the settings of a project if the user is authorized.

    Parameters
    ----------
    user_id : str
        ID of the user attempting to modify the project.
    user_role : str
        Role of the user. Expected values: 'project_manager', 'team_member',
        or 'viewer'.
    project_id : str
        ID of the target project.
    new_settings : dict
        Dictionary containing the settings to apply.

    Returns
    -------
    str
        Confirmation message if update succeeds, otherwise an authorization error.

    Raises
    ------
    ValueError
        If the specified project does not exist.
    """

    # 1. Validate that the project exists
    project = PROJECTS_DB.get(project_id)
    if project is None:
        raise ValueError(f"Project with ID '{project_id}' does not exist.")

    # 2. Authorization check
    # Only a project_manager who is either the creator or a member can modify settings.
    if user_role != "project_manager":
        return f"Authorization error: User '{user_id}' does not have permission to modify project settings."

    if user_id != project["creator_id"] and user_id not in project.get("members", []):
        return f"Authorization error: User '{user_id}' is not a member of project '{project_id}'."

    # 3. Perform the update
    # Use a deep copy to avoid accidental mutation of input data.
    sanitized_settings = copy.deepcopy(new_settings)
    project["settings"] = sanitized_settings

    return f"Project '{project_id}' settings updated successfully by user '{user_id}'."