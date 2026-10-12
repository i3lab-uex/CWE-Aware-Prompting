# -*- coding: utf-8 -*-
"""
Project Configuration Update Module

This module provides a single function, `update_project_configurations`, which
allows authorized users to modify the settings of a project.  The function
performs strict authorization checks to guard against CWE-863
(Incorrect Authorization) by ensuring that only the project creator or a user
with an explicit 'project_manager' role can update the settings.

Author: ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# In‑memory representation of the projects database
# --------------------------------------------------------------------------- #

PROJECTS_DB: dict[str, dict] = {
    # Example project structure
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_alice",
        "members": {"user_bob", "user_charlie"},
        "settings": {
            "deadline": "2024-12-31",
            "visibility": "private",
        },
    },
    # Add more projects as needed...
}


# --------------------------------------------------------------------------- #
# Helper Functions
# --------------------------------------------------------------------------- #

def _has_update_rights(uid: str, role: str, project: dict) -> bool:
    """
    Determine if a user is allowed to update the project's settings.

    Args:
        uid: User identifier.
        role: Role of the user in the system.
        project: Project dictionary.

    Returns:
        True if the user has rights, False otherwise.
    """
    # Only the project creator or users with an explicit 'project_manager' role
    # can modify settings.  Membership alone is not sufficient.
    if uid == project["creator_id"]:
        return True
    if role == "project_manager":
        # Optional: also check that the manager is a member of the project.
        return uid in project.get("members", set())
    return False


# --------------------------------------------------------------------------- #
# Main Function
# --------------------------------------------------------------------------- #

def update_project_configurations(
    uid: str,
    role: str,
    pid: str,
    settings: dict[str, object],
) -> str:
    """
    Update the configuration of a specified project.

    Args:
        uid: Identifier of the user attempting the update.
        role: Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
        pid: Identifier of the project to be updated.
        settings: Dictionary containing new configuration values.

    Returns:
        A success message confirming the update.

    Raises:
        KeyError: If the project ID does not exist in PROJECTS_DB.
        PermissionError: If the user lacks authorization to update settings.
    """
    # Retrieve project; raise KeyError if not found (implicit 404)
    try:
        project = PROJECTS_DB[pid]
    except KeyError as exc:
        raise KeyError(f"Project ID '{pid}' not found.") from exc

    # Authorization check – must be done before any state mutation
    if not _has_update_rights(uid, role, project):
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized to update project '{pid}'."
        )

    # Merge new settings into existing ones
    if not isinstance(settings, dict):
        raise TypeError("settings must be a dictionary.")

    # Defensive copy to avoid accidental aliasing
    updated_settings = dict(project["settings"])
    for key, value in settings.items():
        # Basic validation: disallow setting reserved keys
        if key in {"project_id", "creator_id", "members"}:
            raise ValueError(f"Attempt to modify reserved key '{key}'.")
        updated_settings[key] = value

    # Persist changes
    project["settings"] = updated_settings

    return f"Project '{pid}' settings successfully updated by user '{uid}'."