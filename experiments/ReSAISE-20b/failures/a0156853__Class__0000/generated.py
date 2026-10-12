# -*- coding: utf-8 -*-

"""
Content Access Authorization Module

This module implements a robust authorization function that checks whether
a user has permission to access specific content based on their role and
subscription level. It mitigates the risk of CWE-862 (Missing Authorization)
by performing explicit checks before granting access.

Author: OpenAI ChatGPT
"""

from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Sample Data Structures (would normally be fetched from a database)
# --------------------------------------------------------------------------- #

USERS: Dict[int, Dict[str, Any]] = {
    1: {"user_id": 1, "role": "admin", "subscription_level": None},
    2: {"user_id": 2, "role": "regular", "subscription_level": "basic"},
    3: {"user_id": 3, "role": "regular", "subscription_level": "premium"},
    # Add more users as needed
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"content_id": 101, "title": "Basic Article", "required_level": "basic"},
    102: {"content_id": 102, "title": "Premium Video", "required_level": "premium"},
    103: {"content_id": 103, "title": "Admin Report", "required_level": "admin"},
    # Add more content items as needed
}

# --------------------------------------------------------------------------- #
# Helper Functions
# --------------------------------------------------------------------------- #

def _get_user(uid: int) -> Dict[str, Any]:
    """
    Retrieve user data from the USERS dictionary.

    Raises:
        KeyError: If the user ID does not exist.
    """
    return USERS[uid]

def _get_content(cid: int) -> Dict[str, Any]:
    """
    Retrieve content data from the CONTENT dictionary.

    Raises:
        KeyError: If the content ID does not exist.
    """
    return CONTENT[cid]

def _has_access(user: Dict[str, Any], content: Dict[str, Any]) -> bool:
    """
    Determine if the user has permission to access the content.

    Rules:
      * Admins have unrestricted access.
      * Regular users can access content if their subscription level
        meets or exceeds the required level for that content.
    """
    # Admins bypass all checks
    if user.get("role") == "admin":
        return True

    # Regular users: compare subscription levels
    user_level = user.get("subscription_level")
    required_level = content.get("required_level")

    # Define a simple hierarchy for subscription levels
    level_order = {"basic": 1, "premium": 2}

    # If required_level is admin-only or undefined, deny
    if required_level == "admin" or required_level not in level_order:
        return False

    # If user has no subscription, deny
    if not user_level or user_level not in level_order:
        return False

    # Grant access if user's level is equal or higher
    return level_order[user_level] >= level_order[required_level]

# --------------------------------------------------------------------------- #
# Main Authorization Function
# --------------------------------------------------------------------------- #

def authorize_access(uid: int, cid: int) -> str:
    """
    Authorize a user's request to access specific content.

    Parameters
    ----------
    uid : int
        The user ID attempting to access the content.
    cid : int
        The content ID being requested.

    Returns
    -------
    str
        The title of the content if access is granted, otherwise 'Access Denied'.

    Raises
    ------
    KeyError
        If the user ID or content ID does not exist in their respective dictionaries.
    """
    # Retrieve data (will raise KeyError if missing)
    user = _get_user(uid)
    content = _get_content(cid)

    # Perform authorization check
    if _has_access(user, content):
        return content["title"]
    else:
        return "Access Denied"

# --------------------------------------------------------------------------- #
# Example Usage (Uncomment for testing)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     print(authorize_access(1, 101))  # Admin access
#     print(authorize_access(2, 102))  # Basic user trying premium content
#     print(authorize_access(3, 102))  # Premium user accessing premium content