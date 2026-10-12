import datetime

# Mock database of projects
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_123", "user_456"],
        "settings": {
            "deadline": "2024-12-31",
            "visibility": "private"
        }
    },
    # Additional projects can be added here
}

def update_project_configurations(u_id: str, u_role: str,
                                  proj_id: str,
                                  modified_settings: dict) -> str:
    """
    Update the configuration settings of a project.

    Parameters
    ----------
    u_id : str
        ID of the user attempting the update.
    u_role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        ID of the project to update.
    modified_settings : dict
        Dictionary containing settings to be updated.

    Returns
    -------
    str
        Success message if the update is performed.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project ID is not found in PROJECTS_DB.
    """
    # Validate that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project ID '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization logic:
    # 1. Project creator always has permission.
    # 2. Users with role 'project_manager' have permission if they are a member of the project.
    # 3. Other roles do not have permission.
    if u_id == project["creator_id"]:
        authorized = True
    elif u_role == "project_manager" and u_id in project["members"]:
        authorized = True
    else:
        authorized = False

    if not authorized:
        raise PermissionError(
            f"User '{u_id}' with role '{u_role}' is not authorized to modify project '{proj_id}'."
        )

    # Apply the modifications
    for key, value in modified_settings.items():
        if key not in project["settings"]:
            # Optionally allow new keys; here we permit them
            project["settings"][key] = value
        else:
            # Update existing key
            project["settings"][key] = value

    # Record the update timestamp (optional)
    project.setdefault("_audit", []).append(
        {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "modified_by": u_id,
            "changes": modified_settings
        }
    )

    return f"Project '{proj_id}' settings updated successfully."

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         msg = update_project_configurations(
#             u_id="user_456",
#             u_role="project_manager",
#             proj_id="proj_001",
#             modified_settings={"visibility": "public", "deadline": "2025-01-31"}
#         )
#         print(msg)
#     except Exception as e:
#         print(e)