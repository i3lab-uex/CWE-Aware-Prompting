#!/usr/bin/env python3
"""
Utility for updating project settings with role‑based access control.
"""

from typing import Dict, Any

# Sample in‑memory database – in a real system this would be replaced
# by persistent storage (e.g., a database or external service).
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Add more projects as needed
}


def update_project_configurations(
    u_id: str,
    u_role: str,
    proj_id: str,
    modified_settings: Dict[str, Any],
) -> str:
    """
    Update the settings of a project if the caller is authorized.

    Parameters
    ----------
    u_id : str
        ID of the user attempting to modify the settings.
    u_role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        Identifier of the project to update.
    modified_settings : dict
        Dictionary containing setting keys and new values.

    Returns
    -------
    str
        Success message if the update was applied.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project ID is not found in ``PROJECTS_DB``.
    ValueError
        If ``modified_settings`` is not a dictionary or contains protected keys.

    Notes
    -----
    * Only the project creator and users with role ``project_manager`` are allowed to modify settings.
    * The function protects critical keys such as ``project_id``, ``creator_id`` and ``members`` from being overwritten.
    """
    # Basic validation of input types
    if not isinstance(modified_settings, dict):
        raise ValueError("modified_settings must be a dictionary")

    # Protect immutable fields
    protected_keys = {"project_id", "creator_id", "members"}
    for key in modified_settings:
        if key in protected_keys:
            raise ValueError(f"Modification of '{key}' is not allowed")

    # Retrieve the project; raise KeyError if it doesn't exist
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as exc:
        raise KeyError(f"Project with ID '{proj_id}' not found") from exc

    # Authorization check
    is_creator = u_id == project["creator_id"]
    has_manager_role = u_role.lower() == "project_manager"

    if not (is_creator or has_manager_role):
        raise PermissionError(
            f"User '{u_id}' with role '{u_role}' is not authorized to modify project '{proj_id}'."
        )

    # Apply the updates
    settings = project.setdefault("settings", {})
    settings.update(modified_settings)

    return f"Settings for project '{proj_id}' have been successfully updated."


# Example usage (would normally be in a separate test module)
if __name__ == "__main__":
    try:
        msg = update_project_configurations(
            u_id="user_a",
            u_role="project_manager",
            proj_id="proj_001",
            modified_settings={"visibility": "public", "deadline": "2025-01-15"},
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")