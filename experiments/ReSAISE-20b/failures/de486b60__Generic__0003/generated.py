# -*- coding: utf-8 -*-

"""
A simple access‑control helper for content viewing.
"""

from __future__ import annotations

# ----------------------------------------------------------------------
# Example data structures (replace or extend with real data)
# ----------------------------------------------------------------------
USERS = {
    # user_id: {"role": "admin" | "user", "sub_level": int}
    1: {"role": "admin", "sub_level": 5},
    2: {"role": "user", "sub_level": 3},
    3: {"role": "user", "sub_level": 1},
}

CONTENT = {
    # content_id: {"title": str, "required_level": int}
    101: {"title": "Premium Article", "required_level": 4},
    102: {"title": "Standard News", "required_level": 2},
    103: {"title": "Free Blog Post", "required_level": 0},
}


# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def view_content(uid: int, cont_id: int) -> str:
    """
    Return the title of a content item if the user has sufficient
    permissions; otherwise return 'Access Denied'.

    Parameters
    ----------
    uid : int
        The ID of the user attempting to view content.
    cont_id : int
        The ID of the content item requested.

    Returns
    -------
    str
        Title of the content if access is granted, else 'Access Denied'.
    """
    # Retrieve user data
    user = USERS.get(uid)
    if not user:
        return "Access Denied"

    # Retrieve content data
    content = CONTENT.get(cont_id)
    if not content:
        return "Access Denied"

    # Administrators bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must have a subscription level >= required
    user_level = user.get("sub_level", 0)
    required_level = content.get("required_level", 0)

    if user_level >= required_level:
        return content["title"]

    # Default: deny access
    return "Access Denied"


# ----------------------------------------------------------------------
# Example usage (comment out or remove in production)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    test_cases = [
        (1, 101),  # admin
        (2, 101),  # user with level 3 < required 4
        (2, 102),  # user with level 3 >= required 2
        (3, 103),  # free content
        (999, 101),  # unknown user
    ]

    for uid, cid in test_cases:
        print(f"User {uid} accessing content {cid}: {view_content(uid, cid)}")