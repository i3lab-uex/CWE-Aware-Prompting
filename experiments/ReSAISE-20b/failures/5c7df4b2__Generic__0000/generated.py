from __future__ import annotations

import typing as _t

# Example in‑memory database. In a real system this would be replaced by
# a persistent store (e.g., SQLAlchemy, MongoDB, etc.).
PROJECTS_DB: dict[str, dict] = {
    "proj-001": {
        "project_id": "proj-001",
        "creator_id": "user-123",
        "members": {"user-123", "user-456"},
        # Settings are stored as a simple dictionary. In production,
        # you might want to enforce stricter schemas.
        "settings": {"deadline": "2024-12-31", "budget": 50000},
    },
    # ... more projects
}


def adjust_project_params(
    user_token: str,
    role: str,
    project_ident: str,
    updated_values: dict[str, _t.Any],
) -> str:
    """
    Update project settings if the caller has sufficient rights.

    Parameters
    ----------
    user_token : str
        Identifier of the user attempting the update.
    role : str
        Role of the caller (e.g., 'project_manager', 'team_member', 'viewer').
    project_ident : str
        Identifier of the target project.
    updated_values : dict[str, Any]
        New configuration values for the project's settings.

    Returns
    -------
    str
        Success message indicating that the settings were updated.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project does not exist in ``PROJECTS_DB``.
    """
    # Validate that the project exists
    if project_ident not in PROJECTS_DB:
        raise KeyError(f"Project '{project_ident}' not found.")

    project = PROJECTS_DB[project_ident]

    # Determine whether the user is authorized to modify settings
    is_creator = user_token == project["creator_id"]
    is_member = user_token in project.get("members", set())
    can_modify = (
        role == "project_manager"
        or is_creator
        or (role in {"team_member", "viewer"} and is_member)
    )

    if not can_modify:
        raise PermissionError(
            f"User '{user_token}' with role '{role}' is not authorized "
            "to modify project settings."
        )

    # Perform the update.  In a real system you might validate keys,
    # enforce immutability of certain fields, and log changes.
    project["settings"].update(updated_values)

    return (
        f"Project '{project_ident}' settings updated successfully by user "
        f"'{user_token}'."
    )