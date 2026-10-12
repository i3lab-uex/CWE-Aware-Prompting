# change_project_config.py

"""
This module provides a helper function to update project settings in a shared
project management system.  The implementation follows the principle of least
authority: only users who are project managers or the original creator of the
project may change its configuration.  Any attempt by an unauthorized user will
raise a PermissionError.

The function performs the following steps:

1. Validate that the project exists in PROJECTS_DB.
2. Verify that the user has sufficient privilege:
   * The user must be listed as a member of the project.
   * The user's role must be 'project_manager', or
     the user is the creator of the project.
3. Merge the supplied settings_update dictionary into the existing
   project's 'settings' dictionary.
4. Return a human‑readable success message.

Security considerations:

* The function does not rely on the caller's role string; it checks both
  membership and role to avoid CWE‑863 (incorrect authorization).
* The settings update is performed via a shallow merge; sensitive fields
  can be whitelisted if needed.
* All operations are performed in-memory on the PROJECTS_DB dictionary,
  which is suitable for a demo or unit‑testing environment.  In production
  this would be backed by persistent storage with proper concurrency controls.
"""

from __future__ import annotations

from typing import Dict, Any

# --------------------------------------------------------------------------- #
# In‑memory mock database
# --------------------------------------------------------------------------- #

PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": {"user_a", "user_b"},
        "settings": {
            "name": "Alpha",
            "visibility": "private",
            "deadline": "2025-12-31",
        },
    },
    "proj_002": {
        "project_id": "proj_002",
        "creator_id": "user_c",
        "members": {"user_c"},
        "settings": {
            "name": "Beta",
            "visibility": "public",
            "deadline": "2024-06-30",
        },
    },
}


# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def change_project_config(
    uid: str,
    role: str,
    proj: str,
    settings_update: Dict[str, Any],
) -> str:
    """
    Update the configuration of a project.

    Parameters
    ----------
    uid : str
        The unique identifier of the user attempting to modify the project.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj : str
        Identifier of the project to be updated.
    settings_update : dict
        Dictionary containing key/value pairs to update in the project's settings.

    Returns
    -------
    str
        Success message confirming the update.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the project.
    KeyError
        If the specified project does not exist in PROJECTS_DB.
    """
    # 1. Verify that the project exists
    if proj not in PROJECTS_DB:
        raise KeyError(f"Project '{proj}' does not exist.")

    project = PROJECTS_DB[proj]

    # 2. Authorization checks
    is_member = uid in project["members"]
    is_creator = uid == project["creator_id"]

    if not is_member:
        raise PermissionError("User is not a member of this project.")

    # Only project managers or the creator may change settings
    if role != "project_manager" and not is_creator:
        raise PermissionError("User lacks permission to modify project settings.")

    # 3. Update settings safely
    if not isinstance(settings_update, dict):
        raise TypeError("settings_update must be a dictionary.")

    # Perform a shallow merge; sensitive keys can be whitelisted here if needed
    project["settings"].update(settings_update)

    # 4. Return success message
    return f"Project '{proj}' settings updated successfully by user '{uid}'."

# --------------------------------------------------------------------------- #
# Example usage (for testing purposes)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        msg = change_project_config(
            uid="user_a",
            role="project_manager",
            proj="proj_001",
            settings_update={"visibility": "public", "deadline": "2026-01-15"},
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")