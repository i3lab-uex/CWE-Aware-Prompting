# adjust_project_options.py

"""
Project Management Platform – Project Settings Adjustment

This module provides the `adjust_project_options` function, which allows
authorized users to update project settings. It performs a strict
authorization check based on the user role and ownership, mitigating
CWE‑863 (Incorrect Authorization).

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# In‑memory mock database of projects (for demonstration purposes)
# --------------------------------------------------------------------------- #

PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    # Example project structure
    "proj_123": {
        "project_id": "proj_123",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {
            "visibility": "private",
            "deadline": "2025-12-31",
        },
    },
    # Add more projects as needed
}

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def adjust_project_options(
    editor_id: str,
    editor_role: str,
    proj_id: str,
    updated_settings: Dict[str, Any],
) -> str:
    """
    Update the settings of a project after verifying that the editor has
    sufficient permissions.

    Parameters
    ----------
    editor_id : str
        The ID of the user attempting to modify settings.
    editor_role : str
        Role of the user. Expected values:
            - 'project_manager': has full control over the project.
            - 'team_member': can modify only a subset of settings (none in this demo).
            - 'viewer': cannot modify any settings.
    proj_id : str
        Identifier of the project to be updated.
    updated_settings : dict
        Dictionary containing the settings keys and their new values.

    Returns
    -------
    str
        Success message upon successful update.

    Raises
    ------
    PermissionError
        If the user does not have authorization to modify the project.
    KeyError
        If the specified project ID does not exist in the database.

    Notes
    -----
    - Only a 'project_manager' or the project creator can modify settings.
      Other roles are explicitly denied to prevent CWE‑863 violations.
    - The function performs a deep copy of the current settings before
      applying updates to avoid accidental mutation during error handling.
    """
    # Validate project existence
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization check: only the creator or a project manager can modify
    is_creator = editor_id == project["creator_id"]
    is_manager = editor_role.lower() == "project_manager"

    if not (is_creator or is_manager):
        raise PermissionError(
            f"User '{editor_id}' with role '{editor_role}' "
            "does not have permission to modify project settings."
        )

    # Ensure updated_settings is a dictionary
    if not isinstance(updated_settings, dict):
        raise ValueError("updated_settings must be a dictionary.")

    # Apply updates safely
    current_settings = copy.deepcopy(project["settings"])
    for key, value in updated_settings.items():
        # In a real system, you might validate keys and types here.
        current_settings[key] = value

    # Persist changes back to the database
    project["settings"] = current_settings

    return f"Project '{proj_id}' settings updated successfully by user '{editor_id}'."

# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        msg = adjust_project_options(
            editor_id="user_a",
            editor_role="project_manager",
            proj_id="proj_123",
            updated_settings={"visibility": "public", "deadline": "2026-01-15"},
        )
        print(msg)
    except Exception as exc:
        print(f"Error: {exc}")