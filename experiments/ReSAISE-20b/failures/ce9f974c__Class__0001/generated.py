#!/usr/bin/env python3
"""
Project Settings Management

This module defines a single function, `change_project_settings`, which updates
the configuration of an existing project in the in‑memory database
`PROJECTS_DB`.  The function performs a strict authorization check to avoid
CWE‑863: Incorrect Authorization.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# In‑memory database of projects
PROJECTS_DB: dict[str, dict] = {
    # Example project for illustration purposes
    "proj_123": {
        "project_id": "proj_123",
        "creator_id": "user_1",
        "members": {
            # member_id: role
            "user_2": "project_manager",
            "user_3": "team_member",
        },
        "settings": {
            "deadline": "2024-12-31",
            "visibility": "private",
        },
    }
}

# Roles that are allowed to change project settings
ALLOWED_ROLES = {"project_manager"}


def _authorize(owner_id: str, access_level: str, project: dict) -> None:
    """
    Internal helper that validates whether the user is authorized to modify
    the project's settings.

    Raises:
        PermissionError: If the caller does not have permission.
    """
    # 1. Creator always has full rights
    if owner_id == project["creator_id"]:
        return

    # 2. Check membership and role
    member_role = project["members"].get(owner_id)
    if member_role is None:
        raise PermissionError("User is not a member of the project.")

    # 3. Only users with allowed roles may modify settings
    if member_role not in ALLOWED_ROLES:
        raise PermissionError(
            f"User role '{member_role}' does not permit changing settings."
        )

    # 4. The access_level argument must match the role
    if member_role != access_level:
        raise PermissionError(
            f"Access level '{access_level}' does not match member role '{member_role}'."
        )


def change_project_settings(
    owner_id: str,
    access_level: str,
    proj_id: str,
    modifications: dict,
) -> str:
    """
    Update the settings of a project if the caller has sufficient rights.

    Parameters
    ----------
    owner_id : str
        Identifier of the user attempting to update settings.
    access_level : str
        Role description (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        Identifier of the target project.
    modifications : dict
        Key/value pairs to merge into the project's settings.

    Returns
    -------
    str
        Success message upon successful update.

    Raises
    ------
    KeyError
        If the project does not exist.
    PermissionError
        If the user is unauthorized to modify settings.
    ValueError
        If `modifications` is not a dictionary or empty.
    """
    # Validate input types
    if not isinstance(modifications, dict):
        raise ValueError("Modifications must be a dictionary.")
    if not modifications:
        raise ValueError("No changes provided.")

    # Retrieve the project
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as exc:
        raise KeyError(f"Project with ID '{proj_id}' not found.") from exc

    # Authorization check
    _authorize(owner_id, access_level, project)

    # Apply modifications safely (only update existing keys or add new ones)
    for key, value in modifications.items():
        project["settings"][key] = value

    return f"Project '{proj_id}' settings updated successfully."


# Example usage (uncomment to test)
if __name__ == "__main__":
    try:
        msg = change_project_settings(
            owner_id="user_2",
            access_level="project_manager",
            proj_id="proj_123",
            modifications={"visibility": "public"},
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")