# retrieve_content.py

from typing import Dict, Any


# Example user and content dictionaries.
# In a real application these would come from a database or external service.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin", "subscription_tier": None},
    2: {"role": "user", "subscription_tier": "basic"},
    3: {"role": "user", "subscription_tier": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"title": "Basic Article", "required_tier": "basic"},
    102: {"title": "Premium Video", "required_tier": "premium"},
    103: {"title": "Admin Report", "required_tier": None},
}


def retrieve_content(user_id: int, content_id: int) -> str:
    """
    Return the title of the requested content if the user has sufficient
    permissions. Otherwise return 'Access Denied'.

    Parameters:
        user_id (int): The ID of the requesting user.
        content_id (int): The ID of the requested content.

    Returns:
        str: Content title or 'Access Denied'.

    Raises:
        KeyError: If user_id or content_id does not exist in the data.
    """
    # Retrieve user and content records; raise KeyError if missing
    try:
        user = USERS[user_id]
    except KeyError as exc:
        raise KeyError(f"User ID {user_id} not found") from exc

    try:
        content = CONTENT[content_id]
    except KeyError as exc:
        raise KeyError(f"Content ID {content_id} not found") from exc

    # Admins bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must have a subscription tier that meets or exceeds the required tier
    user_tier = user.get("subscription_tier")
    required_tier = content.get("required_tier")

    # If the content has no tier requirement, grant access
    if required_tier is None:
        return content["title"]

    # Define tier hierarchy for comparison
    tier_order = {"basic": 1, "premium": 2}
    if user_tier not in tier_order or required_tier not in tier_order:
        return "Access Denied"

    if tier_order[user_tier] >= tier_order[required_tier]:
        return content["title"]

    return "Access Denied"