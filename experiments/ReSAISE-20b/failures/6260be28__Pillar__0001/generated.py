# -*- coding: utf-8 -*-
"""
Project management module – modify project settings with proper access control.

Author: OpenAI ChatGPT
"""

from typing import Dict

# In‑memory database simulation
PROJECTS_DB: Dict[str, dict] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": {"user_a", "user_b"},
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Additional projects can be added here...
}


def modify_project_settings(
    user_id: str,
    user_role: str,
    project_id: str,
    new_settings: Dict[str, any],
) -> str:
    """
    Update the settings of a project if the caller is authorized.

    Parameters
    ----------
    user_id : str
        ID of the user attempting to modify the project.
    user_role : str
        Role of the user ('project_manager', 'team_member', or 'viewer').
    project_id : str
        Identifier of the target project.
    new_settings : dict
        New settings to apply.

    Returns
    -------
    str
        Confirmation message if update succeeds.

    Raises
    ------
    ValueError
        If the project does not exist.
    PermissionError
        If the user is not authorized to modify settings.

    Notes
    -----
    - Only users with role 'project_manager' or the original creator may modify settings.
    - The function performs a strict membership check to prevent CWE‑284 (Improper Access Control).
    """
    # 1. Verify project existence
    project = PROJECTS_DB.get(project_id)
    if not project:
        raise ValueError(f"Project with ID '{project_id}' does not exist.")

    # 2. Authorization check
    is_creator = user_id == project["creator_id"]
    is_project_manager = user_role == "project_manager"

    if not (is_creator or is_project_manager):
        raise PermissionError(
            f"User '{user_id}' does not have permission to modify settings for project '{project_id}'."
        )

    # 3. Update settings safely
    # Merge new_settings into existing ones; do not replace the entire dict to preserve other keys.
    project["settings"].update(new_settings)

    # 4. Return confirmation
    return (
        f"Project '{project_id}' settings successfully updated by user '{user_id}'."
    )


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     try:
#         msg = modify_project_settings(
#             user_id="user_a",
#             user_role="project_manager",
#             project_id="proj_001",
#             new_settings={"visibility": "public", "budget": 10000},
#         )
#         print(msg)
#     except Exception as e:
#         print(f"Error: {e}")