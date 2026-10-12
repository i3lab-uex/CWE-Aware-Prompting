from typing import Dict, Any

# Sample data – replace with real data or load from a secure source
USERS: Dict[int, Dict[str, Any]] = {
    1: {"user_id": 1, "role": "admin", "subscription_level": None},
    2: {"user_id": 2, "role": "regular", "subscription_level": "basic"},
    3: {"user_id": 3, "role": "regular", "subscription_level": "premium"},
}

# Subscription levels in ascending order of access
SUBSCRIPTION_ORDER = {"basic": 1, "premium": 2, "gold": 3}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"content_id": 101, "title": "Basic Article", "required_level": "basic"},
    102: {"content_id": 102, "title": "Premium Guide", "required_level": "premium"},
    103: {"content_id": 103, "title": "Gold Masterclass", "required_level": "gold"},
}


def fetch_content(given_user_id: int, target_content_id: int) -> str:
    """
    Return the content title if the user has sufficient privileges,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    given_user_id : int
        The ID of the user attempting to access content.
    target_content_id : int
        The ID of the content being requested.

    Returns
    -------
    str
        Content title or 'Access Denied'.
    """
    # Retrieve user and content safely; avoid KeyError
    user = USERS.get(given_user_id)
    if not user:
        return "Access Denied"

    content = CONTENT.get(target_content_id)
    if not content:
        return "Access Denied"

    # Admins have unrestricted access
    if user.get("role") == "admin":
        return content["title"]

    # For regular users, compare subscription levels
    user_level = user.get("subscription_level")
    required_level = content.get("required_level")

    # Ensure levels exist and are comparable
    if user_level is None or required_level not in SUBSCRIPTION_ORDER:
        return "Access Denied"

    if SUBSCRIPTION_ORDER[user_level] >= SUBSCRIPTION_ORDER[required_level]:
        return content["title"]

    return "Access Denied"