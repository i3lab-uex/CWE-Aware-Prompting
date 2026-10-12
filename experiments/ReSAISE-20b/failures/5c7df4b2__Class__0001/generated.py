from __future__ import annotations

import copy
from typing import Dict, Any


# Sample in‑memory database of projects
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_alice",
        "members": {"user_bob", "user_charlie"},
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Additional projects can be added here
}


def adjust_project_params(
    user_token: str,
    role: str,
    project_ident: str,
    updated_values: Dict[str, Any],
) -> str:
    """
    Update the settings of a project if the caller has sufficient privileges.

    Parameters
    ----------
    user_token : str
        Identifier for the calling user (treated as a user ID).
    role : str
        Role of the caller. Allowed values: 'project_manager', 'team_member',
        or 'viewer'.
    project_ident : str
        Identifier of the target project.
    updated_values : dict
        New configuration values to merge into the project's settings.

    Returns
    -------
    str
        Success message indicating that the settings have been updated.

    Raises
    ------
    PermissionError
        If the caller does not possess sufficient rights to modify the project.
    KeyError
        If the specified project does not exist in ``PROJECTS_DB``.
    """
    # Ensure the project exists
    if project_ident not in PROJECTS_DB:
        raise KeyError(f"Project '{project_ident}' not found.")

    project = PROJECTS_DB[project_ident]

    # Authorization logic
    is_creator = user_token == project["creator_id"]
    is_member = user_token in project.get("members", set())

    # Only a creator or an explicit manager may modify settings
    if not (
        is_creator
        or (role == "project_manager" and is_member)
    ):
        raise PermissionError(
            f"User '{user_token}' with role '{role}' is not authorized "
            "to modify project settings."
        )

    # Merge updated values into the existing settings safely
    new_settings = copy.deepcopy(project["settings"])
    for key, value in updated_values.items():
        # Basic validation: disallow setting keys that are not allowed
        if key in {"project_id", "creator_id"}:
            raise ValueError(f"Modification of '{key}' is not permitted.")
        new_settings[key] = value

    # Persist the changes
    project["settings"] = new_settings

    return f"Project '{project_ident}' settings updated successfully."


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(adjust_project_params(
#         user_token="user_bob",
#         role="project_manager",
#         project_ident="proj_001",
#         updated_values={"visibility": "public", "deadline": "2025-01-15"}
#     ))