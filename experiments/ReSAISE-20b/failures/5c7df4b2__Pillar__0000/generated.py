# -*- coding: utf-8 -*-
"""
Project management utilities.
"""

from typing import Dict, Any

# Sample in‑memory database of projects
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": {"user_123", "user_456"},
        "settings": {
            "visibility": "private",
            "deadline": "2024-12-31",
        },
    },
    # ... other projects ...
}

# List of allowed keys that can be updated in project settings
ALLOWED_SETTINGS_KEYS = {"visibility", "deadline", "description"}


def adjust_project_params(
    user_token: str,
    role: str,
    project_ident: str,
    updated_values: Dict[str, Any],
) -> str:
    """
    Update project settings if the caller has sufficient privileges.

    Args:
        user_token: Identifier of the calling user.
        role: Role of the caller (e.g., 'project_manager', 'team_member', 'viewer').
        project_ident: Identifier of the target project.
        updated_values: Dictionary with new settings.

    Returns:
        Success message string.

    Raises:
        PermissionError: If the caller is not authorized.
        KeyError: If the project does not exist.
    """
    # Validate that the target project exists
    if project_ident not in PROJECTS_DB:
        raise KeyError(f"Project '{project_ident}' not found.")

    project = PROJECTS_DB[project_ident]

    # Determine if the user is authorized
    is_creator = project["creator_id"] == user_token
    is_manager = role == "project_manager"
    is_member = user_token in project["members"]

    # Only a creator or a project manager can change settings
    if not (is_creator or is_manager):
        raise PermissionError(
            "Unauthorized: Only project creators or managers can modify settings."
        )

    # Filter the updated values to allowed keys only
    filtered_updates = {
        k: v for k, v in updated_values.items() if k in ALLOWED_SETTINGS_KEYS
    }

    # If no valid keys provided, raise an error
    if not filtered_updates:
        raise ValueError("No valid settings keys provided for update.")

    # Apply updates
    project["settings"].update(filtered_updates)

    return (
        f"Project '{project_ident}' settings updated successfully by user "
        f"'{user_token}'. Updated keys: {list(filtered_updates.keys())}."
    )