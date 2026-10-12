#!/usr/bin/env python3
"""
Content access control module.
"""

from typing import Dict

# Sample user data. In a real application this would come from a database.
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription_level": "premium"},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
}

# Sample content data. In a real application this would come from a database.
CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Free Article", "required_level": "free"},
    102: {"title": "Basic Guide", "required_level": "basic"},
    103: {"title": "Premium Report", "required_level": "premium"},
}

# Define the hierarchy of subscription levels for easy comparison
LEVEL_HIERARCHY = {"free": 0, "basic": 1, "premium": 2}


def _get_user(user_id: int) -> Dict[str, str]:
    """Retrieve user record with basic validation."""
    if not isinstance(user_id, int):
        raise TypeError("user_id must be an integer")
    user = USERS.get(user_id)
    if not user:
        raise KeyError(f"User with id {user_id} does not exist")
    return user


def _get_content(content_id: int) -> Dict[str, str]:
    """Retrieve content record with basic validation."""
    if not isinstance(content_id, int):
        raise TypeError("content_id must be an integer")
    content = CONTENT.get(content_id)
    if not content:
        raise KeyError(f"Content with id {content_id} does not exist")
    return content


def fetch_content(given_user_id: int, target_content_id: int) -> str:
    """
    Determine whether a user has access to a piece of content.

    Parameters
    ----------
    given_user_id : int
        The ID of the user attempting to access content.
    target_content_id : int
        The ID of the content being requested.

    Returns
    -------
    str
        The title of the content if access is granted, otherwise "Access Denied".
    """
    try:
        user = _get_user(given_user_id)
        content = _get_content(target_content_id)

        # Admins bypass all checks
        if user.get("role") == "admin":
            return content["title"]

        # Regular users must have a subscription level >= required level
        user_level = LEVEL_HIERARCHY.get(user["subscription_level"])
        content_level = LEVEL_HIERARCHY.get(content["required_level"])

        if user_level is None or content_level is None:
            # In case of an unknown level, deny access
            return "Access Denied"

        if user_level >= content_level:
            return content["title"]
    except (KeyError, TypeError):
        # Any lookup or type error results in access denial
        pass

    return "Access Denied"


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(fetch_content(1, 103))  # Admin -> Premium Report
#     print(fetch_content(2, 103))  # Basic user -> Access Denied