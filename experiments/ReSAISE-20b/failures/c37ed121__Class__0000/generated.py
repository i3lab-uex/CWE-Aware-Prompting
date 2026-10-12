import copy
from typing import Dict

# Sample in‑memory database of projects
PROJECTS_DB: Dict[str, dict] = {
    "proj1": {
        "project_id": "proj1",
        "creator_id": "user_a",
        "members": ["user_a", "user_b"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # ... more projects
}


def adjust_project_options(
    editor_id: str,
    editor_role: str,
    proj_id: str,
    updated_settings: dict,
) -> str:
    """
    Update the settings of a project if the editor is authorized.

    Parameters
    ----------
    editor_id : str
        ID of the user attempting to modify settings.
    editor_role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        ID of the target project.
    updated_settings : dict
        Dictionary containing setting keys and new values.

    Returns
    -------
    str
        Success message if the update is performed.

    Raises
    ------
    PermissionError
        If the editor lacks permission to modify the project settings.
    KeyError
        If the specified project does not exist.
    ValueError
        If `updated_settings` is not a dictionary.
    """
    # Basic validation
    if not isinstance(updated_settings, dict):
        raise ValueError("updated_settings must be a dictionary")

    # Retrieve the project
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as exc:
        raise KeyError(f"Project {proj_id} not found") from exc

    # Authorization check: only project managers or the creator can edit
    authorized = False
    if editor_role == "project_manager":
        authorized = True
    elif editor_id == project["creator_id"]:
        authorized = True

    # Optional: ensure the editor is a member of the project
    if editor_id not in project["members"]:
        authorized = False

    if not authorized:
        raise PermissionError(
            f"User {editor_id} does not have permission to modify project {proj_id}"
        )

    # Perform the update
    # Use deepcopy to avoid accidental reference sharing
    new_settings = copy.deepcopy(project["settings"])
    new_settings.update(updated_settings)
    project["settings"] = new_settings

    return f"Project {proj_id} settings updated successfully."


# Example usage (uncomment to test):
# try:
#     msg = adjust_project_options(
#         editor_id="user_a",
#         editor_role="project_manager",
#         proj_id="proj1",
#         updated_settings={"visibility": "public"}
#     )
#     print(msg)
# except Exception as e:
#     print(e)