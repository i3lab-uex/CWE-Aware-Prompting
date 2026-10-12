#!/usr/bin/env python3
"""
Project settings modification module.

This module defines the `modify_project_settings` function which allows a user to
update project settings in a collaborative management system.  The function performs
robust authorization checks and validates input data to prevent common security
issues such as CWE‑863 (Incorrect Authorization).
"""

from __future__ import annotations

# Simulated database of projects
PROJECTS_DB: dict[str, dict] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": {"user_123", "user_456"},
        "settings": {"visibility": "private", "deadline": "2024-12-31"},
    },
    # Add more projects as needed
}


def modify_project_settings(
    user_id: str,
    user_role: str,
    project_id: str,
    new_settings: dict[str, object],
) -> str:
    """
    Update project settings if the user is authorized.

    Parameters
    ----------
    user_id : str
        ID of the user attempting to modify settings.
    user_role : str
        Role of the user (e.g., 'project_manager', 'team_member', or 'viewer').
    project_id : str
        ID of the target project.
    new_settings : dict[str, object]
        Dictionary containing settings to be applied.

    Returns
    -------
    str
        Confirmation message upon successful update.

    Raises
    ------
    ValueError
        If the project does not exist or if new_settings is not a dictionary.
    PermissionError
        If the user is not authorized to modify the project settings.

    Notes
    -----
    - Only users with role 'project_manager' or the creator of the project can
      modify settings.
    - The function validates that `new_settings` is a dictionary to prevent
      accidental type errors.
    - No external dependencies are required; the function operates on an in-memory
      dictionary `PROJECTS_DB`.
    """

    # 1. Verify that the project exists.
    project = PROJECTS_DB.get(project_id)
    if project is None:
        raise ValueError(f"Project with ID '{project_id}' does not exist.")

    # 2. Authorization check: only project_manager or creator can modify.
    is_creator = user_id == project["creator_id"]
    has_permission = (
        user_role == "project_manager" or is_creator
    )
    if not has_permission:
        raise PermissionError(
            f"User '{user_id}' with role '{user_role}' is not authorized to modify project settings."
        )

    # 3. Validate new_settings type.
    if not isinstance(new_settings, dict):
        raise ValueError("new_settings must be a dictionary.")

    # 4. Apply the new settings (deep copy to avoid side effects if needed).
    project["settings"].update(new_settings)

    # 5. Return confirmation.
    return (
        f"Project '{project_id}' settings updated successfully by user "
        f"'{user_id}'."
    )


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     try:
#         result = modify_project_settings(
#             user_id="user_123",
#             user_role="project_manager",
#             project_id="proj_001",
#             new_settings={"visibility": "public"},
#         )
#         print(result)
#     except Exception as e:
#         print(f"Error: {e}")