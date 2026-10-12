# -*- coding: utf-8 -*-
"""
A simple in‑memory project management system with authorization checks.
"""

from typing import Dict, Any

# Mock database: project_id -> project data
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Add more projects as needed
}


def modify_project_settings(
    user_id: str,
    user_role: str,
    project_id: str,
    new_settings: Dict[str, Any],
) -> str:
    """
    Update the settings of a project if the user is authorized.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting to modify project settings.
    user_role : str
        Role of the user. Expected values: 'project_manager',
        'team_member', or 'viewer'.
    project_id : str
        The ID of the project to modify.
    new_settings : dict
        Dictionary containing the settings to update.

    Returns
    -------
    str
        Confirmation message if the update succeeded.

    Raises
    ------
    ValueError
        If the project does not exist.
    PermissionError
        If the user is not authorized to modify settings.
    """
    # Check that the project exists
    if project_id not in PROJECTS_DB:
        raise ValueError(f"Project '{project_id}' does not exist.")

    project = PROJECTS_DB[project_id]

    # Authorization logic (CWE‑863 safe implementation)
    authorized = False
    if user_role == "project_manager":
        # Project managers can modify settings only for projects they own
        if user_id == project["creator_id"]:
            authorized = True

    # Optionally allow a manager role for team members
    if not authorized and user_role == "project_manager":
        if user_id in project["members"]:
            authorized = True

    # Deny access for other roles
    if not authorized:
        raise PermissionError(
            f"User '{user_id}' with role '{user_role}' is not authorized "
            f"to modify settings for project '{project_id}'."
        )

    # Perform the update
    if not isinstance(new_settings, dict):
        raise TypeError("new_settings must be a dictionary.")

    # Merge new settings (shallow copy)
    project["settings"].update(new_settings)

    return (
        f"Settings for project '{project_id}' have been updated successfully "
        f"by user '{user_id}'."
    )


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         msg = modify_project_settings(
#             user_id="user_a",
#             user_role="project_manager",
#             project_id="proj_001",
#             new_settings={"visibility": "public"},
#         )
#         print(msg)
#     except Exception as e:
#         print(f"Error: {e}")