# change_project_settings.py

"""
Implementation of the `change_project_settings` function for a project management platform.
"""

from typing import Dict, Any

# Simulated in-memory database of projects
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    # Example project for demonstration purposes
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],  # list of user IDs
        "settings": {
            "deadline": "2024-12-31",
            "visibility": "private"
        }
    },
    # Additional projects can be added here
}

def change_project_settings(
    owner_id: str,
    access_level: str,
    proj_id: str,
    modifications: Dict[str, Any]
) -> str:
    """
    Update project settings if the caller has sufficient rights.

    Parameters
    ----------
    owner_id : str
        Identifier of the user attempting to modify the project.
    access_level : str
        Role of the user ('project_manager', 'team_member', 'viewer', etc.).
    proj_id : str
        Identifier of the project to modify.
    modifications : dict
        New configuration values for the project settings.

    Returns
    -------
    str
        Success message confirming the update.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the project.
    KeyError
        If the project ID does not exist in `PROJECTS_DB`.
    ValueError
        If modifications is not a dictionary.
    """
    # Validate input types
    if not isinstance(modifications, dict):
        raise ValueError("modifications must be a dictionary")

    # Retrieve the project
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as exc:
        raise KeyError(f"Project ID '{proj_id}' not found.") from exc

    # Authorization logic
    is_creator = owner_id == project["creator_id"]
    has_manager_role = access_level.lower() == "project_manager"
    is_member = owner_id in project["members"]

    # Only the creator or a project manager member can modify settings
    if not (is_creator or (has_manager_role and is_member)):
        raise PermissionError(
            f"User '{owner_id}' does not have permission to modify project settings."
        )

    # Merge modifications into existing settings
    # Use a shallow copy to avoid mutating the original dict unintentionally
    updated_settings = {**project["settings"], **modifications}
    project["settings"] = updated_settings

    return f"Project '{proj_id}' settings successfully updated."

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         msg = change_project_settings(
#             owner_id="user_b",
#             access_level="project_manager",
#             proj_id="proj_001",
#             modifications={"visibility": "public"}
#         )
#         print(msg)
#     except Exception as e:
#         print(f"Error: {e}")