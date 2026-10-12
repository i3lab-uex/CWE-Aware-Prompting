# -*- coding: utf-8 -*-
"""
Content access control module.

The `fetch_content` function checks whether a user has permission to view
a particular piece of content based on their role and subscription level.
"""

from typing import Dict

# --------------------------------------------------------------------------- #
# Sample data (replace with real data sources in production)
# --------------------------------------------------------------------------- #

USERS: Dict[int, Dict[str, str | int]] = {
    1: {"role": "admin", "subscription_level": 5},
    2: {"role": "user", "subscription_level": 3},
    3: {"role": "user", "subscription_level": 1},
}

CONTENT: Dict[int, Dict[str, str | int]] = {
    101: {"title": "Basic Tutorial", "required_level": 1},
    102: {"title": "Intermediate Guide", "required_level": 3},
    103: {"title": "Advanced Manual", "required_level": 5},
}

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def fetch_content(given_user_id: int, target_content_id: int) -> str:
    """
    Return the title of the requested content if access is granted,
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
        Content title if access is permitted, else 'Access Denied'.

    Raises
    ------
    KeyError
        If the user ID or content ID does not exist in their respective dictionaries.
    """
    # Validate presence of user and content
    if given_user_id not in USERS:
        raise KeyError(f"User ID {given_user_id} does not exist.")
    if target_content_id not in CONTENT:
        raise KeyError(f"Content ID {target_content_id} does not exist.")

    user = USERS[given_user_id]
    content = CONTENT[target_content_id]

    # Admins have full access
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must meet or exceed the required subscription level
    user_level = int(user.get("subscription_level", 0))
    required_level = int(content.get("required_level", 0))

    if user_level >= required_level:
        return content["title"]

    # Access denied
    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     print(fetch_content(1, 103))   # Admin access
#     print(fetch_content(2, 102))   # Allowed
#     print(fetch_content(3, 102))   # Denied