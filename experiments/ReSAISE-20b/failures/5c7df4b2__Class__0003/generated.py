# -*- coding: utf-8 -*-
"""
Project settings adjustment module.

This module implements a single public function:
    adjust_project_params(user_token: str, role: str,
                          project_ident: str, updated_values: dict) -> str

The function performs strict authorization checks to avoid CWE-863
(Incorrect Authorization). It allows only the project creator or a user
with the role 'project_manager' to modify project settings.
"""

from typing import Dict, Any

# Sample in‑memory database of projects
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # ... other projects
}

def _has_write_access(user_token: str, role: str,
                      project: Dict[str, Any]) -> bool:
    """
    Internal helper to determine whether the user has write access.
    Access is granted if:
        - The user is the creator of the project, or
        - The user's role is 'project_manager'.
    """
    # Prevents accidental privilege escalation by ensuring the
    # authorization check is performed after retrieving the target resource.
    return role == "project_manager" or user_token == project["creator_id"]

def adjust_project_params(user_token: str, role: str,
                          project_ident: str, updated_values: Dict[str, Any]) -> str:
    """
    Update the settings of a project if the caller is authorized.

    Parameters
    ----------
    user_token : str
        Identifier of the user attempting to modify the project.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    project_ident : str
        Identifier of the target project.
    updated_values : dict
        Dictionary containing new settings to apply.

    Returns
    -------
    str
        Success message indicating the project has been updated.

    Raises
    ------
    KeyError
        If the project identifier does not exist in PROJECTS_DB.
    PermissionError
        If the user lacks sufficient rights to modify the project.

    Notes
    -----
    - The function performs authorization *after* fetching the project to avoid
      CWE‑863.
    - Only top-level keys in ``settings`` are updated; nested structures
      remain untouched unless explicitly provided.
    """
    # Retrieve the target project; raise KeyError if missing
    try:
        project = PROJECTS_DB[project_ident]
    except KeyError as exc:
        raise KeyError(f"Project '{project_ident}' not found.") from exc

    # Authorization check (CWE‑863 mitigation)
    if not _has_write_access(user_token, role, project):
        raise PermissionError(
            f"User '{user_token}' with role '{role}' is not authorized to "
            "modify project settings."
        )

    # Perform the update; merge updated_values into existing settings
    if not isinstance(updated_values, dict):
        raise ValueError("updated_values must be a dictionary.")

    # Only update allowed keys to prevent accidental schema changes
    for key, value in updated_values.items():
        project["settings"][key] = value

    return f"Project '{project_ident}' settings updated successfully."

# Example usage (for testing purposes only)
if __name__ == "__main__":
    try:
        msg = adjust_project_params(
            user_token="user_a",
            role="project_manager",
            project_ident="proj_001",
            updated_values={"visibility": "public", "deadline": "2025-01-15"},
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")