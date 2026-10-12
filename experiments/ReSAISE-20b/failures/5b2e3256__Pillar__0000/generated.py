# -*- coding: utf-8 -*-

"""
Implementation of a simple access control system.
Author: OpenAI
"""

from typing import Dict, Any

# --------------------------------------------------------------------
# Sample data – in a real system these would come from a database
# --------------------------------------------------------------------

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin", "subscription_level": "premium"},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"title": "Premium Article", "required_level": "premium"},
    102: {"title": "Basic Guide", "required_level": "basic"},
    103: {"title": "Admin Panel", "required_level": "admin"},
}

# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------

def _get_user(user_id: int) -> Dict[str, Any]:
    """Retrieve user record. Raises KeyError if not found."""
    return USERS[user_id]

def _get_content(cid: int) -> Dict[str, Any]:
    """Retrieve content record. Raises KeyError if not found."""
    return CONTENT[cid]

def _has_access(user: Dict[str, Any], content: Dict[str, Any]) -> bool:
    """
    Determine whether the user has sufficient privileges to view the content.
    Admins bypass all checks. For normal users, subscription level must
    be equal or higher than the required level.
    """
    if user["role"] == "admin":
        return True

    # Define a simple hierarchy of subscription levels
    level_hierarchy = {"basic": 1, "premium": 2}

    user_level = level_hierarchy.get(user["subscription_level"], 0)
    required_level_name = content["required_level"]
    required_level = level_hierarchy.get(required_level_name, 0)

    return user_level >= required_level

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------

def fetch_content(user_id: int, cid: int) -> str:
    """
    Return the title of the requested content if the user has permission.
    Otherwise, return 'Access Denied'.

    Parameters
    ----------
    user_id : int
        Identifier of the requesting user.
    cid : int
        Identifier of the requested content.

    Returns
    -------
    str
        Content title or 'Access Denied'.
    """
    try:
        user = _get_user(user_id)
        content = _get_content(cid)
    except KeyError:
        # Either user or content does not exist
        return "Access Denied"

    if _has_access(user, content):
        return content["title"]

    return "Access Denied"