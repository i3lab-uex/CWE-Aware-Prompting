# -*- coding: utf-8 -*-
"""
Utility module for content access control.

This implementation protects against CWE‑284 (Improper Access Control) by
verifying that a user has the required subscription level or an administrative
role before returning content.  It also guards against common pitfalls such as
missing keys or invalid data types.
"""

from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Sample data structures – in a real system these would come from a database
# --------------------------------------------------------------------------- #

USERS: Dict[int, Dict[str, Any]] = {
    # user_id : {role: str, subscription: str}
    1: {"role": "admin", "subscription": "gold"},
    2: {"role": "user",  "subscription": "silver"},
    3: {"role": "user",  "subscription": "bronze"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    # content_id : {title: str, required_subscription: str}
    101: {"title": "Advanced Python",          "required_subscription": "gold"},
    102: {"title": "Intermediate SQL",         "required_subscription": "silver"},
    103: {"title": "Intro to HTML",            "required_subscription": "bronze"},
    104: {"title": "Data Science Overview",    "required_subscription": "silver"},
}

# Ordered from lowest to highest subscription level
subscription_hierarchy = ["bronze", "silver", "gold"]

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def retrieve_content(usr_id: int, contid: int) -> str:
    """
    Return the title of the requested content if the user is authorized.
    
    Parameters
    ----------
    usr_id : int
        The ID of the user attempting to access content.
    contid : int
        The ID of the content the user wants to retrieve.

    Returns
    -------
    str
        Content title if access is granted; otherwise 'Access Denied'.

    Notes
    -----
    * Administrators (role == 'admin') bypass subscription checks.
    * Subscription levels are compared using the predefined hierarchy.
    * All inputs are validated to avoid KeyError or type errors.
    """
    # Validate user existence
    user = USERS.get(usr_id)
    if not isinstance(user, dict):
        return "Access Denied"

    # Validate content existence
    content = CONTENT.get(contid)
    if not isinstance(content, dict):
        return "Access Denied"

    # Admin users have full access
    if user.get("role") == "admin":
        return content.get("title", "Access Denied")

    # Regular users must meet or exceed required subscription level
    user_sub = user.get("subscription")
    req_sub  = content.get("required_subscription")

    # Ensure subscription values are valid strings
    if not isinstance(user_sub, str) or not isinstance(req_sub, str):
        return "Access Denied"

    try:
        user_index = subscription_hierarchy.index(user_sub)
        req_index  = subscription_hierarchy.index(req_sub)
    except ValueError:
        # Unknown subscription level
        return "Access Denied"

    if user_index >= req_index:
        return content.get("title", "Access Denied")

    # If none of the above, deny access
    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (for demonstration only; remove or guard in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_cases = [
        (1, 101),   # admin
        (2, 101),   # user silver trying gold content
        (3, 103),   # user bronze accessing bronze content
        (4, 102),   # non-existent user
    ]

    for uid, cid in test_cases:
        print(f"User {uid} accessing content {cid}: {retrieve_content(uid, cid)}")