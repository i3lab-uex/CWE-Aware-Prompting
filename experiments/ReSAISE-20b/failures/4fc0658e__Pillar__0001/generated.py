# -*- coding: utf-8 -*-
"""
Implementation of a secure content access function.
"""

from typing import Dict

# --------------------------------------------------------------------------- #
# Sample data structures (in a real application these would come from a DB)
# --------------------------------------------------------------------------- #

USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription_level": "premium"},
    2: {"role": "user", "subscription_level": "free"},
    3: {"role": "user", "subscription_level": "premium"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Open Article", "required_level": "free"},
    102: {"title": "Premium Video", "required_level": "premium"},
    103: {"title": "Admin Guide", "required_level": "admin"},   # Only admins
}


# --------------------------------------------------------------------------- #
# Utility helpers
# --------------------------------------------------------------------------- #

def _get_user(user_id: int) -> Dict[str, str]:
    """
    Retrieve user information from the USERS dictionary.
    Raises KeyError if the user does not exist.
    """
    return USERS[user_id]


def _get_content(content_id: int) -> Dict[str, str]:
    """
    Retrieve content information from the CONTENT dictionary.
    Raises KeyError if the content does not exist.
    """
    return CONTENT[content_id]


def _has_access(user: Dict[str, str], content: Dict[str, str]) -> bool:
    """
    Determine if a user has access to the content.
    Admins always have access. Regular users must meet or exceed
    the required subscription level.
    """
    if user["role"] == "admin":
        return True

    # Define a simple hierarchy of subscription levels
    level_order = {"free": 0, "premium": 1}
    user_level = level_order.get(user["subscription_level"], -1)
    content_level = level_order.get(content["required_level"], -1)

    return user_level >= content_level


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def fetch_content(given_user_id: int, target_content_id: int) -> str:
    """
    Return the title of the requested content if access is granted.
    Otherwise, return 'Access Denied'.

    Parameters
    ----------
    given_user_id : int
        The ID of the user attempting to access the content.
    target_content_id : int
        The ID of the content being requested.

    Returns
    -------
    str
        Content title or 'Access Denied'.

    Raises
    ------
    KeyError
        If the user ID or content ID does not exist in the respective dictionaries.
    """
    # Retrieve data (will raise KeyError if missing)
    user = _get_user(given_user_id)
    content = _get_content(target_content_id)

    # Check access
    if _has_access(user, content):
        return content["title"]

    return "Access Denied"


# --------------------------------------------------------------------------- #
# Example usage (commented out to avoid side effects)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     print(fetch_content(1, 102))  # Admin accessing premium video
#     print(fetch_content(2, 103))  # Regular user attempting admin guide