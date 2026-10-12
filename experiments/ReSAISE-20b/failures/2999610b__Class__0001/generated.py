# -*- coding: utf-8 -*-

"""
A simple content access control module.
"""

from typing import Dict, List

# --------------------------------------------------------------------------- #
# Data definitions
# --------------------------------------------------------------------------- #

# Mapping of user_id to a dictionary containing role and subscription level.
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription": "platinum"},
    2: {"role": "user",  "subscription": "gold"},
    3: {"role": "user",  "subscription": "silver"},
    4: {"role": "user",  "subscription": "bronze"},
}

# Mapping of content_id to a dictionary containing the title and required
# subscription level for access.
CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Premium Article",      "required_level": "platinum"},
    102: {"title": "Gold Feature",          "required_level": "gold"},
    103: {"title": "Silver Tutorial",       "required_level": "silver"},
    104: {"title": "Bronze Basics",         "required_level": "bronze"},
    105: {"title": "Open Blog Post",        "required_level": "bronze"},
}

# Ordered list of subscription levels from lowest to highest.
SUBSCRIPTION_HIERARCHY: List[str] = ["bronze", "silver", "gold", "platinum"]


# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def _subscription_rank(level: str) -> int:
    """
    Return the numeric rank of a subscription level.
    Lower numbers indicate lower levels.

    Raises:
        ValueError: If the level is not in the hierarchy.
    """
    try:
        return SUBSCRIPTION_HIERARCHY.index(level)
    except ValueError as exc:
        raise ValueError(f"Unknown subscription level: {level}") from exc


def retrieve_content(usr_id: int, contid: int) -> str:
    """
    Return the title of a content item if the user has permission.

    Parameters
    ----------
    usr_id : int
        The ID of the user attempting to access the content.
    contid : int
        The ID of the content item.

    Returns
    -------
    str
        Content title if access is granted; otherwise 'Access Denied'.

    Notes
    -----
    - Administrators have full access.
    - Regular users may only view content at or below their subscription level.
    - All inputs are validated; missing users or content result in denial
      rather than an exception to avoid leaking information.
    """
    # Validate input types (defensive programming)
    if not isinstance(usr_id, int) or not isinstance(contid, int):
        return "Access Denied"

    # Retrieve user and content data safely
    user = USERS.get(usr_id)
    if not user:
        return "Access Denied"

    content = CONTENT.get(contid)
    if not content:
        return "Access Denied"

    # Administrator bypasses all checks
    if user.get("role") == "admin":
        return content["title"]

    # For regular users, compare subscription ranks
    user_level = user.get("subscription")
    required_level = content.get("required_level")

    try:
        if _subscription_rank(user_level) >= _subscription_rank(required_level):
            return content["title"]
    except ValueError:
        # Invalid subscription levels in data – deny access
        pass

    return "Access Denied"