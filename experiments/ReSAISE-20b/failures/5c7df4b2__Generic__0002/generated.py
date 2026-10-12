# adjust_project_params.py

from typing import Dict, Any

# Mock database of projects for demonstration purposes.
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_456", "user_789"],
        "settings": {"name": "Alpha", "deadline": "2025-12-31"}
    },
    # Add more projects as needed.
}

def adjust_project_params(
    user_token: str,
    role: str,
    project_ident: str,
    updated_values: Dict[str, Any]
) -> str:
    """
    Update project settings if the user has sufficient permissions.

    Args:
        user_token (str): Identifier of the user attempting to update settings.
        role (str): Role of the user ('project_manager', 'team_member', 'viewer').
        project_ident (str): Identifier of the target project.
        updated_values (dict): New configuration values to merge into existing settings.

    Returns:
        str: Success message upon successful update.

    Raises:
        KeyError: If the project identifier does not exist in PROJECTS_DB.
        PermissionError: If the user is not authorized to modify project settings.
    """
    # Validate that the project exists
    if project_ident not in PROJECTS_DB:
        raise KeyError(f"Project '{project_ident}' does not exist.")

    project = PROJECTS_DB[project_ident]

    # Authorization logic:
    # 1. The creator of the project can always modify settings.
    # 2. A user with role 'project_manager' and who is a member of the project can modify settings.
    # 3. All other roles are denied permission.
    is_creator = user_token == project["creator_id"]
    is_member = user_token in project.get("members", [])
    has_manager_role = role == "project_manager"

    if not (is_creator or (has_manager_role and is_member)):
        raise PermissionError(
            f"User '{user_token}' with role '{role}' is not authorized to modify project settings."
        )

    # Merge the updated values into existing settings safely.
    if not isinstance(updated_values, dict):
        raise TypeError("updated_values must be a dictionary.")

    # Prevent accidental overwrite of critical keys
    protected_keys = {"project_id", "creator_id", "members"}
    for key in updated_values:
        if key in protected_keys:
            raise ValueError(f"Modification of protected key '{key}' is not allowed.")

    # Update settings
    project["settings"].update(updated_values)

    return f"Project '{project_ident}' settings updated successfully."

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     try:
#         msg = adjust_project_params(
#             user_token="user_456",
#             role="project_manager",
#             project_ident="proj_001",
#             updated_values={"deadline": "2026-01-15", "budget": 50000}
#         )
#         print(msg)
#     except Exception as e:
#         print(f"Error: {e}")