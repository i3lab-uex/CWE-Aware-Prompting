import copy

# Sample in‑memory database of projects.
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_123", "user_456"],
        "settings": {
            "visibility": "private",
            "deadline": "2024-12-31"
        }
    },
    # More projects can be added here...
}


def alter_project_preferences(
    member_id: str,
    member_role: str,
    proj_id: str,
    fresh_settings: dict
) -> str:
    """
    Modify project settings if the caller is authorized.

    Parameters
    ----------
    member_id : str
        The ID of the user attempting to change settings.
    member_role : str
        Role of the caller (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        The ID of the project to be updated.
    fresh_settings : dict
        Dictionary containing new settings values.

    Returns
    -------
    str
        Success message if update is performed.

    Raises
    ------
    PermissionError
        If the caller does not have permission to modify settings.
    KeyError
        If `proj_id` is not found in the database.
    TypeError
        If `fresh_settings` is not a dictionary.
    """
    # Basic input validation
    if not isinstance(fresh_settings, dict):
        raise TypeError("fresh_settings must be a dictionary")

    # Retrieve the project from the database
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as e:
        raise KeyError(f"Project ID '{proj_id}' does not exist") from e

    # Authorization check: only a project manager (or creator) may alter settings
    if member_role != "project_manager" or member_id not in project["members"]:
        raise PermissionError(
            f"User '{member_id}' does not have permission to modify project settings"
        )

    # Perform the update atomically
    original_settings = copy.deepcopy(project["settings"])
    project["settings"].update(fresh_settings)

    # Log the change (in a real system, this would be written to audit logs)
    print(
        f"[AUDIT] User '{member_id}' updated settings of project '{proj_id}'. "
        f"Old: {original_settings} -> New: {project['settings']}"
    )

    return f"Project '{proj_id}' settings updated successfully."


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         result = alter_project_preferences(
#             member_id="user_123",
#             member_role="project_manager",
#             proj_id="proj_001",
#             fresh_settings={"visibility": "public", "deadline": "2025-01-15"}
#         )
#         print(result)
#     except Exception as e:
#         print(f"Error: {e}")