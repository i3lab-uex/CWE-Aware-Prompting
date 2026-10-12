# SPDX-License-Identifier: MIT

"""
A simple content retrieval system that enforces authorization based on user role
and subscription level.

The module defines:
- USERS: mapping of user IDs to a dictionary containing role and subscription.
- CONTENT: mapping of content IDs to a dictionary containing title and required
  subscription level.
- SUBSCRIPTION_HIERARCHY: ordered list of subscription levels from lowest to
  highest.

The `retrieve_content` function performs a full authorization check and returns
the content title if the user is allowed to access it, otherwise 'Access Denied'.
"""

from typing import Dict

# --------------------------------------------------------------------------- #
# Sample data – in a real application these would come from a database.
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription": "premium"},
    2: {"role": "user",  "subscription": "basic"},
    3: {"role": "user",  "subscription": "premium"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Basic Guide",      "subscription_required": "basic"},
    102: {"title": "Premium Tutorial", "subscription_required": "premium"},
}

SUBSCRIPTION_HIERARCHY = ["basic", "standard", "premium"]
# --------------------------------------------------------------------------- #

def _subscription_index(level: str) -> int:
    """
    Return the index of a subscription level in the hierarchy.
    If the level is unknown, return -1 to indicate an invalid level.
    """
    try:
        return SUBSCRIPTION_HIERARCHY.index(level)
    except ValueError:
        return -1


def retrieve_content(usr_id: int, contid: int) -> str:
    """
    Return the title of the requested content if the user is authorized,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    usr_id : int
        The ID of the user attempting to access content.
    contid : int
        The ID of the requested content.

    Returns
    -------
    str
        Content title if authorized, else 'Access Denied'.
    """
    # 1. Verify user exists
    user = USERS.get(usr_id)
    if not user:
        return "Access Denied"

    # 2. Verify content exists
    content = CONTENT.get(contid)
    if not content:
        return "Access Denied"

    # 3. Admins bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # 4. Regular users must have a subscription level equal or higher
    user_level = user.get("subscription")
    required_level = content.get("subscription_required")

    # Handle missing or invalid subscription data
    if not user_level or not required_level:
        return "Access Denied"

    user_index = _subscription_index(user_level)
    required_index = _subscription_index(required_level)

    if user_index == -1 or required_index == -1:
        return "Access Denied"

    if user_index >= required_index:
        return content["title"]

    # 5. If none of the above, deny access
    return "Access Denied"