# -*- coding: utf-8 -*-
"""
Module providing a content access function with proper authorization checks.
"""

from typing import Dict

# --------------------------------------------------------------------------- #
# Sample data structures. In a real application these would be fetched from
# a database or an external service.
# --------------------------------------------------------------------------- #
USERS: Dict[int, Dict[str, str]] = {
    # user_id : { "role": ..., "subscription": ... }
    1: {"role": "admin",   "subscription": "premium"},
    2: {"role": "user",    "subscription": "basic"},
    3: {"role": "user",    "subscription": "premium"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    # content_id : { "title": ..., "level_required": ... }
    101: {"title": "Admin Guide",          "level_required": "admin"},
    102: {"title": "Premium Article",      "level_required": "premium"},
    103: {"title": "Basic Tutorial",       "level_required": "basic"},
}

# --------------------------------------------------------------------------- #
# Authorization logic
# --------------------------------------------------------------------------- #
def fetch_content(user_id: int, cid: int) -> str:
    """
    Return the title of the requested content if the user is authorized.
    Otherwise return 'Access Denied'.

    Parameters
    ----------
    user_id : int
        Identifier of the requesting user.
    cid : int
        Identifier of the content to access.

    Returns
    -------
    str
        The title of the content or 'Access Denied'.
    """
    # Retrieve user and content records
    user = USERS.get(user_id)
    if not user:
        return "Access Denied"

    content = CONTENT.get(cid)
    if not content:
        return "Access Denied"

    # Administrators bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must have a subscription level that meets or exceeds
    # the required level. For simplicity we assume levels are ordered as:
    # basic < premium.
    user_level = user.get("subscription")
    required_level = content.get("level_required")

    # Define level hierarchy
    LEVELS_ORDER = {"basic": 1, "premium": 2}

    # If the required level is 'admin', deny access to non-admins
    if required_level == "admin":
        return "Access Denied"

    # Compare numeric levels
    if LEVELS_ORDER.get(user_level, 0) >= LEVELS_ORDER.get(required_level, 0):
        return content["title"]

    return "Access Denied"