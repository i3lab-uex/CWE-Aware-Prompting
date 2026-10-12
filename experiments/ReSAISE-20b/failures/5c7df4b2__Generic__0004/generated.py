import copy

# Sample in‑memory projects database
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_123", "user_456"],
        "settings": {"name": "Alpha", "deadline": "2024-12-31"},
    },
    # Add more projects as needed
}


def adjust_project_params(user_token: str, role: str,
                          project_ident: str,
                          updated_values: dict) -> str:
    """
    Update the settings of a project if the caller has sufficient privileges.

    Parameters
    ----------
    user_token : str
        Identifier for the user attempting to modify the project.
    role : str
        Role of the caller (e.g., 'project_manager', 'team_member', 'viewer').
    project_ident : str
        Identifier of the target project.
    updated_values : dict
        Dictionary containing new configuration values for the project's settings.

    Returns
    -------
    str
        Success message confirming that the project settings were updated.

    Raises
    ------
    PermissionError
        If the caller is not authorized to modify the project.
    KeyError
        If the specified project does not exist in PROJECTS_DB.
    TypeError
        If `updated_values` is not a dictionary.

    Notes
    -----
    - Only users with role 'project_manager' or the creator of the project can modify settings.
    - The function replaces the entire `settings` dictionary with a deep copy of `updated_values`.
    """
    # Validate input types
    if not isinstance(updated_values, dict):
        raise TypeError("updated_values must be a dictionary")

    # Retrieve the project
    try:
        project = PROJECTS_DB[project_ident]
    except KeyError as exc:
        raise KeyError(f"Project '{project_ident}' not found") from exc

    # Authorization check
    is_creator = user_token == project.get("creator_id")
    has_manager_role = role.lower() == "project_manager"

    if not (is_creator or has_manager_role):
        raise PermissionError("User is not authorized to update project settings")

    # Update the project's settings safely
    new_settings = copy.deepcopy(updated_values)
    project["settings"] = new_settings

    return f"Project '{project_ident}' settings successfully updated."


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         msg = adjust_project_params(
#             user_token="user_123",
#             role="project_manager",
#             project_ident="proj_001",
#             updated_values={"name": "Beta", "deadline": "2025-01-15"}
#         )
#         print(msg)
#     except Exception as e:
#         print(f"Error: {e}")