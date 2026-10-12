#!/usr/bin/env python3
"""
Project configuration update module.
"""

from typing import Dict

# Mock database of projects. In a real system this would be replaced by
# persistent storage (e.g., a relational database or NoSQL store).
PROJECTS_DB: Dict[str, dict] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_alice",
        "members": ["user_bob", "user_charlie"],
        "settings": {"deadline": "2025-12-31", "budget": 50000},
    },
    # ... other projects ...
}


def _is_authorized(uid: str, role: str, project: dict) -> bool:
    """
    Determine if a user is allowed to update the given project's settings.

    :param uid: User identifier.
    :param role: Role of the user (e.g., 'project_manager', 'team_member').
    :param project: The project dictionary.
    :return: True if authorized, False otherwise.
    """
    # Only the creator or a user with role 'project_manager' can modify settings.
    return uid == project["creator_id"] or role == "project_manager"


def update_project_configurations(uid: str, role: str, pid: str, settings: Dict) -> str:
    """
    Update the configuration of a project if the caller is authorized.

    :param uid: Identifier of the user attempting to update settings.
    :param role: Role of that user.
    :param pid: Identifier of the project to modify.
    :param settings: New configuration values for the project.
    :return: Success message indicating that the settings were updated.
    :raises PermissionError: If the user does not have permission to modify the project.
    :raises KeyError: If the project ID is not found in PROJECTS_DB.
    """
    # Ensure the project exists
    if pid not in PROJECTS_DB:
        raise KeyError(f"Project '{pid}' does not exist.")

    project = PROJECTS_DB[pid]

    # Check authorization
    if not _is_authorized(uid, role, project):
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized to update project '{pid}'."
        )

    # Basic validation of settings (ensure it's a dict)
    if not isinstance(settings, dict):
        raise ValueError("Settings must be provided as a dictionary.")

    # Update settings
    project["settings"].update(settings)

    return f"Project '{pid}' configuration updated successfully."


# Example usage (for testing purposes only)
if __name__ == "__main__":
    try:
        msg = update_project_configurations(
            uid="user_alice",
            role="project_manager",
            pid="proj_001",
            settings={"budget": 75000, "deadline": "2026-01-31"},
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")