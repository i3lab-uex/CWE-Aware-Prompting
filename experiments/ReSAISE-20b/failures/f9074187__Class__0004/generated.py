from __future__ import annotations

# Sample data structures – in a real application these would come from a database.
USERS: dict[int, dict[str, str | int]] = {
    1: {"role": "admin", "subscription_level": "premium"},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
}

CONTENT: dict[int, dict[str, str]] = {
    101: {"title": "Basic Tutorial", "required_level": "basic"},
    102: {"title": "Advanced Guide", "required_level": "premium"},
    103: {"title": "Admin Only Docs", "required_level": "admin"},
}

# Define a mapping of subscription levels to a numeric hierarchy for comparison.
LEVEL_HIERARCHY = {
    "basic": 1,
    "premium": 2,
    "admin": 3,          # admin level is considered highest
}

def grant_access(user_id: int, item_id: int) -> str:
    """
    Return the title of the requested content if the user is authorized.
    Otherwise, return 'Access Denied'.

    Parameters
    ----------
    user_id : int
        The ID of the user attempting to access content.
    item_id : int
        The ID of the content item.

    Returns
    -------
    str
        Content title if access is granted; otherwise 'Access Denied'.
    """
    # Retrieve user and content information safely.
    user = USERS.get(user_id)
    if not user:
        return "Access Denied"

    content = CONTENT.get(item_id)
    if not content:
        return "Access Denied"

    user_role = user.get("role")
    user_level = user.get("subscription_level")

    # Admins have unrestricted access.
    if user_role == "admin":
        return content["title"]

    # Map subscription levels to numeric values for comparison.
    user_level_val = LEVEL_HIERARCHY.get(user_level, 0)
    required_level_val = LEVEL_HIERARCHY.get(content["required_level"], 0)

    # Regular users can access content if their level meets or exceeds the required level.
    if user_level_val >= required_level_val:
        return content["title"]

    # If none of the above conditions are met, deny access.
    return "Access Denied"