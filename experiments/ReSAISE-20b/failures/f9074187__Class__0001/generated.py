# grant_access.py

from typing import Dict, Any

# Sample data structures. In a real system these would be fetched from a database.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin", "subscription_level": "premium"},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"title": "Intro to Python", "required_level": "basic"},
    102: {"title": "Advanced AI", "required_level": "premium"},
    103: {"title": "Open Source Guide", "required_level": "free"},
}


def grant_access(user_id: int, item_id: int) -> str:
    """
    Determines if a user can access a piece of content.

    Parameters
    ----------
    user_id : int
        Identifier for the user attempting access.
    item_id : int
        Identifier for the content item.

    Returns
    -------
    str
        The title of the content if access is granted; otherwise 'Access Denied'.
    """
    # Fetch user and content data
    user = USERS.get(user_id)
    content = CONTENT.get(item_id)

    # Validate existence
    if not user or not content:
        return "Access Denied"

    # Admins bypass subscription checks
    if user.get("role") == "admin":
        return content["title"]

    # For regular users, compare subscription levels
    user_level = user.get("subscription_level", "free")
    required_level = content.get("required_level", "free")

    # Define a simple hierarchy for comparison
    level_order = {"free": 0, "basic": 1, "premium": 2}

    if level_order.get(user_level, 0) >= level_order.get(required_level, 0):
        return content["title"]

    return "Access Denied"