import datetime
from typing import Dict, Any

# Simulated in‑memory database of projects.
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj-001": {
        "project_id": "proj-001",
        "creator_id": "user-123",
        "members": {"user-123", "user-456"},
        "settings": {
            "name": "Alpha",
            "deadline": datetime.date(2024, 12, 31),
        },
    },
    # Additional projects can be added here.
}

class PermissionError(Exception):
    """Raised when a user is not authorized to modify project settings."""
    pass

def edit_project_settings(
    member_id: str,
    role: str,
    project_key: str,
    updated_configuration: Dict[str, Any],
) -> str:
    """
    Update the settings of a project if the caller is authorized.

    Args:
        member_id: The ID of the user attempting to edit.
        role: Role string, e.g., 'project_manager', 'team_member', or 'viewer'.
        project_key: The key identifying the target project.
        updated_configuration: Dictionary of settings to merge into the existing config.

    Returns:
        A success message indicating the project was updated.

    Raises:
        PermissionError: If the user does not have permission to modify settings.
        KeyError: If the project_key is unknown in PROJECTS_DB.
    """
    # 1. Retrieve the target project atomically
    try:
        project = PROJECTS_DB[project_key]
    except KeyError as exc:
        raise KeyError(f"Project '{project_key}' not found.") from exc

    # 2. Authorization check: only project_manager or creator can modify settings
    is_creator = member_id == project["creator_id"]
    has_permission = role == "project_manager" or is_creator

    if not has_permission:
        raise PermissionError(
            f"User '{member_id}' with role '{role}' is not authorized "
            f"to edit settings for project '{project_key}'."
        )

    # 3. Merge the updated configuration safely
    if not isinstance(updated_configuration, dict):
        raise ValueError("updated_configuration must be a dictionary.")

    # Defensive copy to avoid accidental mutation of input
    new_settings = project["settings"].copy()
    for key, value in updated_configuration.items():
        # Optional: add validation per key if needed
        new_settings[key] = value

    # 4. Apply the update
    project["settings"] = new_settings

    return f"Project '{project_key}' settings updated successfully."

# Example usage (for testing purposes only)
if __name__ == "__main__":
    try:
        msg = edit_project_settings(
            member_id="user-123",
            role="project_manager",
            project_key="proj-001",
            updated_configuration={"deadline": datetime.date(2025, 1, 15)},
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")