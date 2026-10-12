# grant_access.py

from typing import Dict, Any

# Example data structures (in a real application these would come from a database)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin", "subscription_level": None},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"title": "Basic Article", "required_level": "basic"},
    102: {"title": "Premium Report", "required_level": "premium"},
    103: {"title": "Admin Guide", "required_level": None},
}

# Define the order of subscription levels for comparison
SUBSCRIPTION_ORDER = {
    "basic": 1,
    "premium": 2,
}


def grant_access(user_id: int, item_id: int) -> str:
    """
    Determine whether a user can access a content item.

    Args:
        user_id (int): The ID of the user attempting to access content.
        item_id (int): The ID of the requested content.

    Returns:
        str: The title of the content if access is granted, otherwise
             "Access Denied".

    Raises:
        KeyError: If the user_id or item_id does not exist in their respective
                  dictionaries.
    """
    # Retrieve the user and content records; raise KeyError if not found
    user = USERS[user_id]
    content = CONTENT[item_id]

    # Admins have full access
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must meet or exceed the required subscription level
    user_level = user.get("subscription_level")
    required_level = content.get("required_level")

    # If the content has no requirement, grant access
    if required_level is None:
        return content["title"]

    # Ensure both levels are defined and comparable
    if user_level is None or required_level not in SUBSCRIPTION_ORDER:
        return "Access Denied"

    # Compare subscription levels
    if SUBSCRIPTION_ORDER[user_level] >= SUBSCRIPTION_ORDER[required_level]:
        return content["title"]

    # Deny access otherwise
    return "Access Denied"