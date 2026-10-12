# -*- coding: utf-8 -*-
"""
Project Management Platform – Project Settings Update

This module provides a single function, `adjust_project_params`, which
allows an authorized user to modify the settings of a project.  Only users
with the role ``project_manager`` are allowed to perform this operation.
The function checks that the project exists, verifies the user’s role,
and updates the project's settings in place.  If the user is not
authorized, a :class:`PermissionError` is raised.

Security Considerations
-----------------------
* **CWE-284 – Improper Access Control**:  
  The function enforces role-based access control by checking the
  ``role`` argument before performing any modifications.  It does not
  rely on any external authentication mechanism; in a real system this
  function would be called only after the user has been authenticated.
* **Input Validation**:  
  The function ensures that ``project_ident`` refers to an existing
  project in ``PROJECTS_DB``.  It also checks that the ``updated_values``
  dictionary is not empty to avoid accidental no-op updates.
"""

from __future__ import annotations

# Mock database of projects.  In a real application this would be
# backed by persistent storage.
PROJECTS_DB: dict[str, dict] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_alice",
        "members": {"user_bob", "user_charlie"},
        "settings": {
            "deadline": "2024-12-31",
            "visibility": "private",
        },
    },
    # Additional projects could be added here...
}


def adjust_project_params(
    user_token: str,
    role: str,
    project_ident: str,
    updated_values: dict,
) -> str:
    """
    Update the settings of a project if the user has sufficient rights.

    Parameters
    ----------
    user_token : str
        The identifier of the user attempting to update settings.
    role : str
        The user's role (e.g., 'project_manager', 'team_member', 'viewer').
    project_ident : str
        The identifier of the target project.
    updated_values : dict
        A dictionary containing new configuration values for the project.

    Returns
    -------
    str
        Success message indicating that settings have been updated.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify project settings.
    KeyError
        If ``project_ident`` does not exist in :data:`PROJECTS_DB`.
    ValueError
        If ``updated_values`` is empty.
    """
    # Validate project existence
    if project_ident not in PROJECTS_DB:
        raise KeyError(f"Project '{project_ident}' does not exist.")

    project = PROJECTS_DB[project_ident]

    # Enforce role-based access control
    if role != "project_manager":
        raise PermissionError(
            f"User '{user_token}' with role '{role}' is not authorized "
            "to update project settings."
        )

    # Ensure there are actually values to apply
    if not updated_values:
        raise ValueError("No settings provided for update.")

    # Update the project's settings
    project_settings = project.setdefault("settings", {})
    for key, value in updated_values.items():
        project_settings[key] = value

    return (
        f"Project '{project_ident}' settings updated successfully by "
        f"user '{user_token}'."
    )


# Example usage (would normally be part of unit tests or application logic)
if __name__ == "__main__":
    try:
        msg = adjust_project_params(
            user_token="user_alice",
            role="project_manager",
            project_ident="proj_001",
            updated_values={"visibility": "public", "deadline": "2025-01-15"},
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")