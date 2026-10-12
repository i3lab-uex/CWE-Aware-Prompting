# -*- coding: utf-8 -*-
"""
Project settings modification module.

This module provides a single public function, ``modify_project_settings``, which
allows authorized users to update the settings of a project in a collaborative
project management system.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import typing as _t

# Simulated in‑memory database of projects.
# In a real system this would be replaced by persistent storage (e.g., a database).
PROJECTS_DB: dict[str, dict] = {
    # Example project entry
    "proj-001": {
        "project_id": "proj-001",
        "creator_id": "user-123",
        "members": ["user-456", "user-789"],
        "settings": {
            "visibility": "private",
            "deadline": "2024-12-31",
        },
    },
}


def modify_project_settings(
    user_id: str,
    user_role: str,
    project_id: str,
    new_settings: dict[str, _t.Any],
) -> str:
    """
    Update the settings of a project after performing authorization checks.

    Parameters
    ----------
    user_id : str
        Identifier of the user attempting to modify the project.
    user_role : str
        Role of the user. Expected values are 'project_manager', 'team_member',
        or 'viewer'. Only users with role 'project_manager' or the project
        creator are allowed to modify settings.
    project_id : str
        Identifier of the target project.
    new_settings : dict[str, Any]
        Dictionary containing the settings to be applied.

    Returns
    -------
    str
        Confirmation message indicating successful update.

    Raises
    ------
    ValueError
        If the specified project does not exist.
    PermissionError
        If the user is not authorized to modify the project's settings.

    Notes
    -----
    The function performs a strict check that the project exists before
    evaluating authorization.  This mitigates CWE‑863 (Incorrect Authorization)
    by ensuring that the existence of a resource is verified before any
    permission logic runs.  It also guards against race conditions where a
    project could be deleted between checks by performing the authorization
    on the already retrieved object.
    """
    # -------------------------------------------------------------------------
    # 1. Verify project existence
    # -------------------------------------------------------------------------
    project = PROJECTS_DB.get(project_id)
    if not project:
        raise ValueError(f"Project with ID '{project_id}' does not exist.")

    # -------------------------------------------------------------------------
    # 2. Authorization check
    # -------------------------------------------------------------------------
    is_creator = user_id == project.get("creator_id")
    is_manager = user_role == "project_manager"
    if not (is_creator or is_manager):
        raise PermissionError(
            f"User '{user_id}' with role '{user_role}' is not authorized "
            "to modify project settings."
        )

    # -------------------------------------------------------------------------
    # 3. Apply new settings
    # -------------------------------------------------------------------------
    if not isinstance(new_settings, dict):
        raise TypeError("new_settings must be a dictionary.")

    # Perform a shallow merge to preserve existing keys not mentioned in new_settings
    project["settings"].update(new_settings)

    # -------------------------------------------------------------------------
    # 4. Return confirmation
    # -------------------------------------------------------------------------
    return (
        f"Project '{project_id}' settings updated successfully by user "
        f"'{user_id}'."
    )