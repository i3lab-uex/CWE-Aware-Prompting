# -*- coding: utf-8 -*-
"""
Utility for access‑controlled content retrieval.

Author: OpenAI
"""

# Sample data structures – in a real application these would come from a database.
USERS = {
    1: {"role": "admin",   "subscription_level": None},
    2: {"role": "user",    "subscription_level": "basic"},
    3: {"role": "user",    "subscription_level": "premium"},
    # ... more users
}

CONTENT = {
    101: {"title": "Welcome Guide",          "level_required": "basic"},
    102: {"title": "Advanced Techniques",   "level_required": "premium"},
    103: {"title": "Admin Dashboard",       "level_required": None},
    # ... more content
}


def fetch_content(user_id: int, cid: int) -> str:
    """
    Return the title of a content item if the user has sufficient privileges.
    
    Parameters
    ----------
    user_id : int
        Identifier of the requesting user.
    cid : int
        Identifier of the content item requested.

    Returns
    -------
    str
        Content title on success, or 'Access Denied' if the user is not authorized.

    Raises
    ------
    KeyError
        If either the user_id or cid is not present in the data stores.
    """
    # Verify that both user and content exist
    try:
        user = USERS[user_id]
    except KeyError as exc:
        raise KeyError(f"Unknown user ID: {user_id}") from exc

    try:
        content = CONTENT[cid]
    except KeyError as exc:
        raise KeyError(f"Unknown content ID: {cid}") from exc

    # Admins bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # Determine required level for the requested content
    required_level = content.get("level_required")

    # If no level is required, grant access
    if required_level is None:
        return content["title"]

    # Non‑admin users must have at least the required subscription level
    user_level = user.get("subscription_level")
    if user_level is None:
        return "Access Denied"

    # Define a simple hierarchy for comparison
    LEVEL_ORDER = {"basic": 1, "premium": 2}
    if LEVEL_ORDER.get(user_level, 0) >= LEVEL_ORDER.get(required_level, 0):
        return content["title"]

    return "Access Denied"