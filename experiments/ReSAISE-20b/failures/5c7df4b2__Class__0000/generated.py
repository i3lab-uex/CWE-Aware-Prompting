# -*- coding: utf-8 -*-
"""
Project management utility – adjust_project_params

This module contains a single public function, `adjust_project_params`, that
updates the settings of an existing project.  The operation is protected by
authorization checks to avoid CWE‑863 (Incorrect Authorization).

Author: ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any


# Sample in‑memory database of projects.  In a real system this would be
# replaced by a persistent store (e.g., SQL, NoSQL, etc.).
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_alice",
        "members": {"user_bob", "user_carol"},
        "settings": {
            "deadline": "2024-12-31",
            "visibility": "private",
        },
    },
    # Additional projects can be added here.
}


def _is_user_authorized(user_token: str, role: str, project: Dict[str, Any]) -> bool:
    """
    Internal helper to determine if a user is allowed to modify the project.

    The policy is:
        * Project creator (user_token == creator_id) – always authorized.
        * User with role 'project_manager' – always authorized regardless of
          membership status (assuming they are the project manager).
        * Any other user – must be a member of the project.

    Parameters
    ----------
    user_token : str
        The identifier representing the user.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    project : dict
        Project dictionary from PROJECTS_DB.

    Returns
    -------
    bool
        True if authorized, False otherwise.
    """
    # Creator check (exact match)
    if user_token == project["creator_id"]:
        return True

    # Project manager role check
    if role.lower() == "project_manager":
        return True

    # Membership check – members are stored as a set for O(1) lookup
    return user_token in project.get("members", set())


def adjust_project_params(
    user_token: str,
    role: str,
    project_ident: str,
    updated_values: Dict[str, Any],
) -> str:
    """
    Update the settings of a project after performing authorization checks.

    Parameters
    ----------
    user_token : str
        Identifier for the requesting user.
    role : str
        Role of the requesting user.
    project_ident : str
        Identifier of the target project.
    updated_values : dict
        New configuration values to merge into the project's settings.

    Returns
    -------
    str
        Success message confirming the update.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the project.
    KeyError
        If the specified project does not exist in PROJECTS_DB.
    ValueError
        If updated_values is not a dictionary or contains invalid keys.
    """
    # Validate inputs
    if not isinstance(updated_values, dict):
        raise ValueError("updated_values must be a dictionary")

    # Retrieve the project; KeyError will propagate if not found
    project = PROJECTS_DB[project_ident]

    # Authorization check – prevent CWE-863
    if not _is_user_authorized(user_token, role, project):
        raise PermissionError(
            f"User '{user_token}' does not have permission to update project "
            f"'{project_ident}'."
        )

    # Perform the settings update
    # Make a shallow copy to avoid accidental mutation of shared objects.
    new_settings = copy.deepcopy(project.get("settings", {}))
    for key, value in updated_values.items():
        if not isinstance(key, str):
            raise ValueError("Setting keys must be strings")
        new_settings[key] = value

    # Persist the changes
    project["settings"] = new_settings

    return f"Project '{project_ident}' settings successfully updated."


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to test):
#
# try:
#     msg = adjust_project_params(
#         user_token="user_bob",
#         role="team_member",
#         project_ident="proj_001",
#         updated_values={"visibility": "public", "deadline": "2025-01-15"},
#     )
#     print(msg)
# except Exception as e:
#     print(f"Error: {e}")
#
# --------------------------------------------------------------------------- #