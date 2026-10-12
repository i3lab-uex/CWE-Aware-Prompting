# fetch_content.py

"""
This module implements a simple access control function for content retrieval.
It follows the principle of least privilege: only users with sufficient
subscription level (or admin role) may access a given piece of content.

The implementation is intentionally straightforward but includes
defensive programming practices to mitigate CWE‑284 (Improper Access Control)
by ensuring that every decision is made explicitly and data is validated.
"""

from typing import Dict, Any

# Example user database
USERS: Dict[int, Dict[str, Any]] = {
    1: {"user_id": 1, "role": "admin", "subscription_level": None},
    2: {"user_id": 2, "role": "member", "subscription_level": "basic"},
    3: {"user_id": 3, "role": "member", "subscription_level": "premium"},
    # Add more users as needed
}

# Example content database
CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"content_id": 101, "title": "Open Access Article", "required_level": None},
    102: {"content_id": 102, "title": "Basic Tutorial", "required_level": "basic"},
    103: {"content_id": 103, "title": "Premium Webinar", "required_level": "premium"},
    # Add more content as needed
}

# Define the order of subscription levels for comparison
SUBSCRIPTION_ORDER = {
    None: 0,        # Admin or no restriction
    "basic": 1,
    "premium": 2,
}


def fetch_content(given_user_id: int, target_content_id: int) -> str:
    """
    Returns the title of the requested content if the user has sufficient
    privileges. Otherwise returns 'Access Denied'.

    Parameters
    ----------
    given_user_id : int
        Identifier of the user attempting to access content.
    target_content_id : int
        Identifier of the requested content.

    Returns
    -------
    str
        Content title if access is granted, otherwise 'Access Denied'.
    """
    # Retrieve user and content records safely
    user = USERS.get(given_user_id)
    if not isinstance(user, dict):
        # Unknown user
        return "Access Denied"

    content = CONTENT.get(target_content_id)
    if not isinstance(content, dict):
        # Unknown content
        return "Access Denied"

    # Admins bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # For regular users, check subscription level
    required_level = content.get("required_level")
    user_level = user.get("subscription_level")

    # Normalize levels; missing or unknown levels are treated as lowest
    required_rank = SUBSCRIPTION_ORDER.get(required_level, 0)
    user_rank = SUBSCRIPTION_ORDER.get(user_level, 0)

    if user_rank >= required_rank:
        return content["title"]

    # If none of the above conditions are met, deny access
    return "Access Denied"