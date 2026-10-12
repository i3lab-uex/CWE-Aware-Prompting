#!/usr/bin/env python3
"""
Project management helper – update project settings.

This module provides a single public function:
    change_project_settings(owner_id, access_level, proj_id, modifications)

The function validates that the caller has sufficient permissions to
modify a project's settings.  It raises PermissionError when access is denied.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Dummy in‑memory database – replace with real persistence layer.
# Each project is a dict containing:
#   - project_id (str)
#   - creator_id (str)
#   - members   (dict[str, str])  # user_id -> role
#   - settings  (dict)
# --------------------------------------------------------------------------- #
PROJECTS_DB: dict[str, dict] = {
    "proj-001": {
        "project_id": "proj-001",
        "creator_id": "user-alice",
        "members": {
            "user-bob": "team_member",
            "user-charlie": "viewer",
        },
        "settings": {"deadline": "2025-12-31", "visibility": "private"},
    },
    # Additional projects can be added here.
}


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _has_write_permission(
    owner_id: str, access_level: str, project: dict
) -> bool:
    """
    Determine if the caller can modify the project's settings.

    Rules:
        1. The project creator always has write permission.
        2. Users with the 'project_manager' role have permission.
    """
    if owner_id == project["creator_id"]:
        return True

    # Normal members are stored in the 'members' mapping.
    member_role = project["members"].get(owner_id)
    return access_level == "project_manager" and member_role == "project_manager"


# --------------------------------------------------------------------------- #
# Main API
# --------------------------------------------------------------------------- #
def change_project_settings(
    owner_id: str,
    access_level: str,
    proj_id: str,
    modifications: dict,
) -> str:
    """
    Update the settings of a project.

    Parameters
    ----------
    owner_id : str
        The user attempting to modify the project.
    access_level : str
        Role of the user in the context of this operation
        (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        Identifier of the target project.
    modifications : dict
        Dictionary containing key/value pairs to update in the project's settings.

    Returns
    -------
    str
        Success message confirming that the settings were updated.

    Raises
    ------
    PermissionError
        If `owner_id` does not have permission to modify the project.
    KeyError
        If `proj_id` is unknown in ``PROJECTS_DB``.
    ValueError
        If `modifications` contains keys that are not allowed to be updated.
    """
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    if not _has_write_permission(owner_id, access_level, project):
        raise PermissionError(
            f"User '{owner_id}' does not have permission to modify project '{proj_id}'."
        )

    # Define a whitelist of allowed setting keys.
    ALLOWED_SETTINGS = {"deadline", "visibility", "description"}

    # Validate modifications
    invalid_keys = set(modifications) - ALLOWED_SETTINGS
    if invalid_keys:
        raise ValueError(
            f"Invalid setting keys for update: {sorted(invalid_keys)}"
        )

    # Apply changes atomically
    project_settings = project["settings"]
    for key, value in modifications.items():
        project_settings[key] = value

    return f"Project '{proj_id}' settings successfully updated."


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        msg = change_project_settings(
            owner_id="user-bob",
            access_level="project_manager",
            proj_id="proj-001",
            modifications={"deadline": "2026-01-15", "visibility": "public"},
        )
        print(msg)
    except Exception as exc:
        print(f"Error: {exc}")