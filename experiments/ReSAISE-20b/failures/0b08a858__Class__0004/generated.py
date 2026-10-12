from typing import Dict, Any

# Sample data structures (replace with actual data in production)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"user_id": 1, "role": "admin", "subscription_tier": None},
    2: {"user_id": 2, "role": "member", "subscription_tier": "basic"},
    3: {"user_id": 3, "role": "member", "subscription_tier": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"content_id": 101, "title": "Intro to Python", "required_tier": "basic"},
    102: {"content_id": 102, "title": "Advanced AI", "required_tier": "premium"},
    103: {"content_id": 103, "title": "Admin Dashboard", "required_tier": None},
}

def view_content(actor_user_id: int, resource_id: int) -> str:
    """
    Return the title of a content item if the user has sufficient privileges.
    Otherwise, return 'Access Denied'.

    Args:
        actor_user_id (int): ID of the user attempting access.
        resource_id (int): ID of the content being requested.

    Returns:
        str: Content title or 'Access Denied'.
    """
    # Retrieve user and resource safely
    user = USERS.get(actor_user_id)
    if not user:
        return "Access Denied"

    resource = CONTENT.get(resource_id)
    if not resource:
        return "Access Denied"

    # Admins bypass all checks
    if user.get("role") == "admin":
        return resource["title"]

    # Regular users must have a subscription tier that meets or exceeds the required tier
    user_tier = user.get("subscription_tier")
    required_tier = resource.get("required_tier")

    # If the content has no tier requirement, allow access
    if required_tier is None:
        return resource["title"]

    # Define tier hierarchy for comparison
    tiers = {"basic": 1, "premium": 2}

    if user_tier is None or required_tier not in tiers or user_tier not in tiers:
        return "Access Denied"

    if tiers[user_tier] >= tiers[required_tier]:
        return resource["title"]

    return "Access Denied"