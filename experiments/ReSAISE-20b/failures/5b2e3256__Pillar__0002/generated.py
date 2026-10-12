# -*- coding: utf-8 -*-

"""
Implementation of a simple access‑control system for content retrieval.

The module defines two global dictionaries:

    USERS   : {user_id: {"role": str, "level": int}}
    CONTENT : {content_id: {"title": str, "required_level": int}}

The function `fetch_content` checks whether the user is an administrator
or has a subscription level equal to or higher than the content's required
level.  If access is granted, the content title is returned; otherwise,
the string "Access Denied" is returned.

This implementation follows the principle of least privilege and
prevents accidental data leakage by never revealing any user or content
information beyond what is necessary for the access decision.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample data – in a real system these would come from a database
# --------------------------------------------------------------------------- #

USERS = {
    1: {"role": "admin",   "level": 5},
    2: {"role": "user",    "level": 3},
    3: {"role": "user",    "level": 1},
}

CONTENT = {
    101: {"title": "Premium Article",       "required_level": 4},
    102: {"title": "Standard Guide",        "required_level": 2},
    103: {"title": "Public Announcement",   "required_level": 0},
}

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def fetch_content(user_id: int, cid: int) -> str:
    """
    Return the title of the requested content if the user has permission.

    Parameters
    ----------
    user_id : int
        Identifier of the requesting user.
    cid : int
        Identifier of the content to retrieve.

    Returns
    -------
    str
        Content title if access is granted; otherwise "Access Denied".

    Notes
    -----
    * Admin users bypass subscription checks.
    * Regular users must have a subscription level >= required_level.
    * If either the user or content does not exist, access is denied.
    """
    # Retrieve user and content data; use dict.get to avoid KeyError
    user = USERS.get(user_id)
    content = CONTENT.get(cid)

    if not user or not content:
        # Unknown user or content – deny access silently
        return "Access Denied"

    # Admin users have full access
    if user.get("role") == "admin":
        return content["title"]

    # For regular users, compare subscription levels
    user_level = user.get("level", 0)
    required_level = content.get("required_level", 0)

    if user_level >= required_level:
        return content["title"]

    # All other cases: deny access
    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    for uid in USERS:
        for cid in CONTENT:
            print(f"User {uid} -> Content {cid}: {fetch_content(uid, cid)}")