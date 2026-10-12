#!/usr/bin/env python3
"""
Project settings adjustment module.

This module implements the `adjust_project_params` function, which updates
project configuration only for authorized users.  The implementation follows
best practices for authorization checks to avoid CWE‑863 (Incorrect
Authorization) and other common security pitfalls.

Author: ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any


# Mock in‑memory database of projects.  In a real application this would be
# replaced by persistent storage (e.g., a database).
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    # Example project structure:
    # "proj_123": {
    #     "project_id": "proj_123",
    #     "creator_id": "user_alice",
    #     "members": ["user_bob", "user_carol"],
    #     "settings": {"deadline": "2025-12-31", "visibility": "private"},
    # }
}


# Define a whitelist of settings that can be updated.  Any attempt to modify
# other keys will raise an exception.
ALLOWED_SETTINGS_KEYS = {"deadline", "visibility", "budget", "priority"}


def _has_project_access(user_token: str, project: Dict[str, Any], role: str) -> bool:
    """
    Determine whether the user has sufficient rights to modify the project.

    The authorization policy is:
      - Project creator (creator_id) always has full rights.
      - Users with role 'project_manager' and who are members of the project
        also have full rights.
      - All other users are denied.

    Parameters:
        user_token (str): Identifier of the user.
        project (dict): Project data from PROJECTS_DB.
        role (str): User's role.

    Returns:
        bool: True if authorized, False otherwise.
    """
    # Check for creator privilege
    if user_token == project["creator_id"]:
        return True

    # Check for managerial privilege among members
    if role == "project_manager" and user_token in project.get("members", []):
        return True

    # Deny by default
    return False


def adjust_project_params(
    user_token: str,
    role: str,
    project_ident: str,
    updated_values: Dict[str, Any],
) -> str:
    """
    Update project settings for an authorized user.

    Parameters:
        user_token (str): Identifier of the user attempting the update.
        role (str): User's role ('project_manager', 'team_member', 'viewer', ...).
        project_ident (str): Identifier of the target project.
        updated_values (dict): Dictionary containing new configuration values.

    Returns:
        str: Success message confirming the update.

    Raises:
        KeyError: If the project identifier does not exist in PROJECTS_DB.
        PermissionError: If the user lacks sufficient authorization.
        ValueError: If `updated_values` contains disallowed keys.
    """
    # 1. Retrieve the project from the database
    if project_ident not in PROJECTS_DB:
        raise KeyError(f"Project '{project_ident}' does not exist.")

    project = PROJECTS_DB[project_ident]

    # 2. Authorization check (CWE‑863 mitigation)
    if not _has_project_access(user_token, project, role):
        raise PermissionError(
            f"User '{user_token}' with role '{role}' is not authorized to modify project '{project_ident}'."
        )

    # 3. Validate update keys against whitelist
    disallowed_keys = set(updated_values) - ALLOWED_SETTINGS_KEYS
    if disallowed_keys:
        raise ValueError(
            f"Attempted to update disallowed settings keys: {sorted(disallowed_keys)}."
        )

    # 4. Perform the update atomically
    # Make a shallow copy of current settings to avoid accidental mutation if
    # an exception occurs during the update.
    new_settings = copy.deepcopy(project.get("settings", {}))
    new_settings.update(updated_values)

    # 5. Persist the changes back to the "database"
    project["settings"] = new_settings

    # 6. Return a success message
    return f"Project '{project_ident}' settings updated successfully by user '{user_token}'."