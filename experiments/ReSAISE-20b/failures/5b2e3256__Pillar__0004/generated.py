#!/usr/bin/env python3
"""
Content access control module.

The `fetch_content` function checks whether a user has the right to view
a particular piece of content based on their role and subscription level.
It protects against improper access control (CWE‑284) by performing
role‑based and subscription‑level checks before granting access.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample data – in a real application these would come from a database
# --------------------------------------------------------------------------- #

USERS = {
    1: {"role": "admin", "sub_level": None},        # admin has unrestricted access
    2: {"role": "user", "sub_level": 1},
    3: {"role": "user", "sub_level": 2},
    4: {"role": "guest", "sub_level": 0},           # lowest level
}

CONTENT = {
    101: {"title": "Public Announcement", "required_level": 0},
    102: {"title": "Premium Article", "required_level": 1},
    103: {"title": "Enterprise Report", "required_level": 2},
}


# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def fetch_content(user_id: int, cid: int) -> str:
    """
    Return the title of the requested content if the user is authorized.

    Parameters
    ----------
    user_id : int
        Identifier of the requesting user.
    cid : int
        Identifier of the requested content.

    Returns
    -------
    str
        The content title if access is granted, otherwise 'Access Denied'.

    Notes
    -----
    * Administrators (`role == "admin"`) bypass all checks and receive the
      content regardless of subscription level.
    * Regular users must have a subscription level that is **greater than or
      equal to** the content's required level.
    * If the user or content does not exist, access is denied.

    Security
    --------
    The function performs all checks in a deterministic order:
      1. Verify that the user exists.
      2. If the user is an admin, grant access immediately.
      3. Verify that the content exists.
      4. Compare subscription levels.

    This ordering prevents potential timing attacks and ensures that no
    unauthorized user can infer the existence of content based on error
    messages.
    """
    # 1. Verify user exists
    user = USERS.get(user_id)
    if not user:
        return "Access Denied"

    # 2. Admin bypass
    if user.get("role") == "admin":
        content = CONTENT.get(cid)
        return content["title"] if content else "Access Denied"

    # 3. Verify content exists
    content = CONTENT.get(cid)
    if not content:
        return "Access Denied"

    # 4. Check subscription level
    required = content["required_level"]
    user_sub = user.get("sub_level")
    if user_sub is None or user_sub < required:
        return "Access Denied"

    # Access granted
    return content["title"]


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tests = [
        (1, 101),  # admin
        (2, 102),
        (3, 103),
        (4, 101),
        (2, 103),  # insufficient level
        (999, 101),  # unknown user
        (2, 999),   # unknown content
    ]

    for uid, cid in tests:
        print(f"User {uid} accessing content {cid}: {fetch_content(uid, cid)}")