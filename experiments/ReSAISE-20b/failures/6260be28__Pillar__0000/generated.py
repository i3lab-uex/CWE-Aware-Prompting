# -*- coding: utf-8 -*-
"""
Project Settings Modification Module

This module defines a single function `modify_project_settings` which
handles the update of project settings in a collaborative project
management system.  The implementation includes rigorous authorization
checks to avoid CWE‑284 (Improper Access Control) and ensures that
only legitimate users can modify a project.

Author: ChatGPT
"""

from __future__ import annotations

# Simulated in‑memory database of projects.
# Each project record contains:
#   - 'project_id': str
#   - 'creator_id': str
#   - 'members': set[str]  # user IDs that belong to the project
#   - 'settings': dict    # arbitrary key/value settings
PROJECTS_DB: dict[str, dict] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_alice",
        "members": {"user_alice", "user_bob"},
        "settings": {"visibility": "private", "deadline": "2025-12-31"},
    },
    # Additional projects can be added here
}

# Define the roles that are allowed to modify project settings.
ALLOWED_ROLES = {"project_manager", "team_member"}


def _is_user_authorized(user_id: str, user_role: str, project: dict) -> bool:
    """
    Internal helper to verify if a user is authorized to modify the project.

    A user is authorized if:
        1. The user's role is in ALLOWED_ROLES.
        2. The user is the creator of the project, OR
           the user belongs to the project's members set.

    Parameters:
        user_id (str): The ID of the user.
        user_role (str): The role assigned to the user.
        project (dict): The project record.

    Returns:
        bool: True if authorized, False otherwise.
    """
    # Validate role
    if user_role not in ALLOWED_ROLES:
        return False

    # Check creator or membership
    if user_id == project["creator_id"] or user_id in project["members"]:
        return True

    return False


def modify_project_settings(
    user_id: str,
    user_role: str,
    project_id: str,
    new_settings: dict,
) -> str:
    """
    Update the settings of a project after performing authorization checks.

    Args:
        user_id (str): ID of the user attempting to modify settings.
        user_role (str): Role of the user ('project_manager', 'team_member', or 'viewer').
        project_id (str): ID of the target project.
        new_settings (dict): Dictionary containing the new settings.

    Returns:
        str: Confirmation message upon successful update.

    Raises:
        ValueError: If the project does not exist.
        PermissionError: If the user is not authorized to modify settings.

    Security Notes:
        - The function checks both role and membership to mitigate CWE-284.
        - It performs a shallow merge of settings; sensitive fields can be
          explicitly filtered if required.
    """
    # Retrieve the project from the database
    project = PROJECTS_DB.get(project_id)
    if not project:
        raise ValueError(f"Project with ID '{project_id}' does not exist.")

    # Authorization check
    if not _is_user_authorized(user_id, user_role, project):
        raise PermissionError(
            f"User '{user_id}' with role '{user_role}' is not authorized to modify project '{project_id}'."
        )

    # Merge new settings into existing ones (shallow copy)
    project["settings"].update(new_settings)

    return (
        f"Project '{project_id}' settings updated successfully by user '{user_id}'."
    )


# Example usage (for testing purposes only; remove or guard under __main__ in production)
if __name__ == "__main__":
    try:
        print(
            modify_project_settings(
                user_id="user_bob",
                user_role="team_member",
                project_id="proj_001",
                new_settings={"visibility": "public"},
            )
        )
    except Exception as e:
        print(f"Error: {e}")