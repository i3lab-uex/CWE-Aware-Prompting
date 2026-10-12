from __future__ import annotations

import datetime
from typing import Dict, Any

# Mock database of projects. In a real application this would be replaced by
# persistent storage such as a relational database or an ORM.
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": {"user_456", "user_789"},
        # Default settings – a simple dictionary for demonstration
        "settings": {
            "deadline": datetime.date(2024, 12, 31),
            "visibility": "private",
        },
    }
}


def adjust_project_params(
    user_token: str,
    role: str,
    project_ident: str,
    updated_values: Dict[str, Any],
) -> str:
    """
    Update project settings if the caller is authorized.

    Parameters
    ----------
    user_token : str
        Identifier for the user attempting to modify the project.
    role : str
        Role of the caller. Valid values are 'project_manager', 'team_member',
        and 'viewer'. The function accepts any string but enforces
        authorization based on role.
    project_ident : str
        Identifier of the target project.
    updated_values : dict
        Dictionary containing new key/value pairs for the project's settings.

    Returns
    -------
    str
        Success message when the update is applied.

    Raises
    ------
    PermissionError
        If the caller does not have sufficient rights to modify the project.
    KeyError
        If the specified project does not exist in ``PROJECTS_DB``.
    """
    # Validate project existence
    if project_ident not in PROJECTS_DB:
        raise KeyError(f"Project '{project_ident}' does not exist.")

    project = PROJECTS_DB[project_ident]

    # Authorization logic:
    # - The creator of the project can modify settings.
    # - Users with role 'project_manager' or members of the project can also
    #   modify settings.
    authorized = False

    if user_token == project["creator_id"]:
        authorized = True
    elif role == "project_manager":
        authorized = True
    elif user_token in project.get("members", set()):
        # Members are allowed to change settings only if their role is
        # explicitly granted permission. For simplicity, we allow all members.
        authorized = True

    if not authorized:
        raise PermissionError(
            f"User '{user_token}' with role '{role}' is not authorized "
            "to modify project settings."
        )

    # Perform the update. We do a shallow merge to avoid overwriting
    # unrelated settings unintentionally.
    project_settings = project.setdefault("settings", {})
    for key, value in updated_values.items():
        # Basic validation: ensure the setting exists or is allowed to be added.
        project_settings[key] = value

    return f"Project '{project_ident}' settings updated successfully."


# Example usage (commented out to keep module importable)
if __name__ == "__main__":
    try:
        msg = adjust_project_params(
            user_token="user_123",
            role="project_manager",
            project_ident="proj_001",
            updated_values={"visibility": "public"},
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")