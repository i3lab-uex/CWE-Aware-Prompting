# retrieve_content.py

from typing import Dict, Any


# Sample data structures – in a real application these would be fetched from a database
USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin", "subscription_tier": "premium"},
    2: {"role": "user", "subscription_tier": "basic"},
    3: {"role": "user", "subscription_tier": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"title": "Basic Article", "required_tier": "basic"},
    102: {"title": "Premium Guide", "required_tier": "premium"},
    103: {"title": "Admin Report", "required_tier": "admin_only"},
}


def _has_access(user: Dict[str, Any], content: Dict[str, Any]) -> bool:
    """
    Internal helper to determine if a user has access to content.
    Admins bypass tier checks. Regular users must have a tier that meets or exceeds the required level.
    """
    # Admins have full access
    if user.get("role") == "admin":
        return True

    # Map tier levels to numeric values for comparison
    tier_order = {"basic": 1, "premium": 2}
    user_tier_value = tier_order.get(user.get("subscription_tier"), 0)
    content_tier_value = tier_order.get(content.get("required_tier"), 0)

    return user_tier_value >= content_tier_value


def retrieve_content(user_id: int, content_id: int) -> str:
    """
    Returns the title of the requested content if the user has permission,
    otherwise returns 'Access Denied'.

    Parameters
    ----------
    user_id : int
        Identifier of the user attempting access.
    content_id : int
        Identifier of the requested content.

    Returns
    -------
    str
        Content title or 'Access Denied'.
    """
    # Retrieve user and content data safely; return denial on missing entries
    user = USERS.get(user_id)
    if not user:
        return "Access Denied"

    content = CONTENT.get(content_id)
    if not content:
        return "Access Denied"

    # Perform access check
    if _has_access(user, content):
        return content["title"]

    return "Access Denied"