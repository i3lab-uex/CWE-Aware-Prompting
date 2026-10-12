import copy

# Simulated in‑memory database of projects.
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "emp_100",
        "members": ["emp_101", "emp_102"],
        # Settings stored as a dictionary
        "settings": {
            "name": "Project Alpha",
            "deadline": "2024-12-31",
            "visibility": "private"
        }
    },
    # Additional projects can be added here...
}


def update_project_configurations(emp_id: str, role: str, proj_id: str,
                                   updated_settings: dict) -> str:
    """
    Update the settings of a project after performing robust authorization checks.

    Parameters
    ----------
    emp_id : str
        Unique identifier of the employee attempting the update.
    role : str
        Role of the employee (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        Identifier of the project to update.
    updated_settings : dict
        Dictionary containing the new settings for the project.

    Returns
    -------
    str
        Success message if the update is applied.

    Raises
    ------
    PermissionError
        If the employee does not have sufficient privileges.
    KeyError
        If the project ID is not found in PROJECTS_DB.
    ValueError
        If updated_settings is not a dictionary or contains invalid keys.
    """

    # 1. Validate input types
    if not isinstance(updated_settings, dict):
        raise ValueError("updated_settings must be a dictionary.")

    # 2. Retrieve the project
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as exc:
        raise KeyError(f"Project '{proj_id}' not found.") from exc

    # 3. Authorization logic (CWE-863 safe implementation)
    # Only a project manager who is either the creator or a member may update settings.
    authorized = False

    if role == "project_manager":
        # Check membership first to avoid false positives.
        if emp_id == project["creator_id"] or emp_id in project["members"]:
            authorized = True

    # Optionally, allow team members with elevated privileges (if needed)
    elif role == "team_member":
        # For stricter security, disallow direct updates for team members.
        authorized = False

    elif role == "viewer":
        authorized = False

    # Additional roles can be added here with explicit rules.

    if not authorized:
        raise PermissionError(
            f"Employee '{emp_id}' with role '{role}' is not authorized to update project '{proj_id}'."
        )

    # 4. Validate settings keys against allowed fields
    ALLOWED_KEYS = {"name", "deadline", "visibility"}
    for key in updated_settings:
        if key not in ALLOWED_KEYS:
            raise ValueError(f"Invalid setting key: '{key}'. Allowed keys are {ALLOWED_KEYS}.")

    # 5. Apply the update atomically
    # Create a shallow copy to avoid accidental mutation of other references.
    new_settings = copy.deepcopy(project["settings"])
    new_settings.update(updated_settings)
    project["settings"] = new_settings

    return f"Project '{proj_id}' settings updated successfully by employee '{emp_id}'."