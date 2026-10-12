# -*- coding: utf-8 -*-
"""
Authorisation helper for content access.

This module contains a single public function, `view_content`, which checks
whether a user has the required privileges to view a piece of content.
The function performs explicit authorisation checks and returns either
the title of the requested content or a generic 'Access Denied' message.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample data structures
# --------------------------------------------------------------------------- #

# USERS maps a user ID to a dictionary containing:
#   * role: either 'admin' or 'user'
#   * level: an integer indicating the user's subscription level
USERS = {
    1: {"role": "admin", "level": 5},
    2: {"role": "user",  "level": 3},
    3: {"role": "user",  "level": 1},
}

# CONTENT maps a content ID to a dictionary containing:
#   * title: the display name of the content
#   * level: an integer indicating the minimum subscription level required
CONTENT = {
    101: {"title": "Premium Article",      "level": 4},
    102: {"title": "Standard Video",       "level": 2},
    103: {"title": "Free Tutorial",        "level": 0},
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def view_content(uid: int, cont_id: int) -> str:
    """
    Return the title of a content item if the user has permission,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    uid : int
        The ID of the user attempting to access the content.
    cont_id : int
        The ID of the content being requested.

    Returns
    -------
    str
        The title of the content if authorised, else 'Access Denied'.

    Notes
    -----
    * An admin user bypasses subscription checks.
    * Regular users may only view content whose required level is less
      than or equal to their own subscription level.
    * If the user ID or content ID does not exist, access is denied.

    Security
    --------
    This function performs an explicit authorisation check before any
    content is returned, mitigating CWE‑862 (Missing Authorization).
    """
    # Fetch user and content data; if either is missing, deny access
    user = USERS.get(uid)
    content = CONTENT.get(cont_id)

    if not user or not content:
        return "Access Denied"

    # Admins have unrestricted access
    if user.get("role") == "admin":
        return content["title"]

    # Regular users: compare subscription levels
    user_level = int(user.get("level", 0))
    required_level = int(content.get("level", 0))

    if user_level >= required_level:
        return content["title"]

    # All other cases are denied
    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     print(view_content(1, 101))  # Should print "Premium Article"
#     print(view_content(2, 101))  # Should print "Access Denied"
#     print(view_content(3, 103))  # Should print "Free Tutorial"