# view_content.py

from typing import Dict, Any

# Example data structures. In a real application these would be
# retrieved from a database or an external service.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"user_id": 1, "role": "admin", "subscription_tier": "premium"},
    2: {"user_id": 2, "role": "user", "subscription_tier": "basic"},
    3: {"user_id": 3, "role": "user", "subscription_tier": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"content_id": 101, "title": "Advanced Python", "required_tier": "premium"},
    102: {"content_id": 102, "title": "Intro to Python", "required_tier": "basic"},
    103: {"content_id": 103, "title": "Data Science Basics", "required_tier": "basic"},
}

# Define the order of subscription tiers for comparison.
TIER_ORDER = {
    "basic": 1,
    "premium": 2,
}


def _has_access(user: Dict[str, Any], content: Dict[str, Any]) -> bool:
    """
    Determine whether a user is authorized to view the content.
    Admins bypass all checks. For regular users, compare subscription tiers.
    """
    if user.get("role") == "admin":
        return True

    user_tier = user.get("subscription_tier")
    required_tier = content.get("required_tier")

    # If either tier is missing or unknown, deny access.
    if user_tier not in TIER_ORDER or required_tier not in TIER_ORDER:
        return False

    # User must have a tier equal to or higher than required.
    return TIER_ORDER[user_tier] >= TIER_ORDER[required_tier]


def view_content(actor_user_id: int, resource_id: int) -> str:
    """
    Return the title of the requested content if the user is authorized.
    Otherwise, return 'Access Denied'.

    Parameters
    ----------
    actor_user_id : int
        Identifier of the user attempting to access content.
    resource_id : int
        Identifier of the content the user wants to view.

    Returns
    -------
    str
        Content title or 'Access Denied'.
    """
    try:
        user = USERS[actor_user_id]
    except KeyError:
        # Unknown user – deny access.
        return "Access Denied"

    try:
        content = CONTENT[resource_id]
    except KeyError:
        # Unknown resource – deny access.
        return "Access Denied"

    if _has_access(user, content):
        # Securely return the title; do not expose internal IDs.
        return content["title"]
    else:
        return "Access Denied"