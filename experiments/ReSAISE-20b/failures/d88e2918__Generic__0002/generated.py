import copy
from typing import Dict, Any

# Example in‑memory database of projects
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj-001": {
        "project_id": "proj-001",
        "creator_id": "user-123",
        "members": ["user-123", "user-456"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # ... additional projects ...
}


def edit_project_settings(
    member_id: str,
    role: str,
    project_key: str,
    updated_configuration: Dict[str, Any],
) -> str:
    """
    Update the settings of a project if the caller is authorized.

    Parameters
    ----------
    member_id : str
        Unique identifier of the user attempting to modify settings.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    project_key : str
        Identifier of the target project.
    updated_configuration : dict
        Settings to be merged into the existing configuration.

    Returns
    -------
    str
        Success message upon successful update.

    Raises
    ------
    PermissionError
        If the user does not have permission to edit the project settings.
    KeyError
        If the specified project_key is not found in PROJECTS_DB.
    """

    # Validate existence of the project
    if project_key not in PROJECTS_DB:
        raise KeyError(f"Project '{project_key}' does not exist.")

    project = PROJECTS_DB[project_key]

    # Permission check:
    #   - Must be a member of the project.
    #   - Must have role 'project_manager' or be the creator.
    is_member = member_id in project.get("members", [])
    is_creator = member_id == project.get("creator_id")
    has_manager_role = role.lower() == "project_manager"

    if not is_member or (not (has_manager_role or is_creator)):
        raise PermissionError(
            f"User '{member_id}' does not have permission to edit project settings."
        )

    # Merge the updated configuration safely
    if not isinstance(updated_configuration, dict):
        raise ValueError("updated_configuration must be a dictionary.")

    # Perform deep copy to avoid accidental mutation of input
    new_settings = copy.deepcopy(project.get("settings", {}))
    for key, value in updated_configuration.items():
        new_settings[key] = value

    # Update the project's settings
    project["settings"] = new_settings

    return f"Project '{project_key}' settings updated successfully."


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         msg = edit_project_settings(
#             member_id="user-123",
#             role="project_manager",
#             project_key="proj-001",
#             updated_configuration={"visibility": "public", "budget": 50000},
#         )
#         print(msg)
#     except Exception as e:
#         print(f"Error: {e}")