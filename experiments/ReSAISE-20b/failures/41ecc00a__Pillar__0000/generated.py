#!/usr/bin/env python3
"""
Secure content retrieval module.

The `retrieve_content` function checks a user's role and subscription tier against the
required access level for a given piece of content.  Administrators bypass all checks,
while regular users may only access content that matches or is lower than their tier.
"""

from typing import Dict

# --------------------------------------------------------------------------- #
# Data structures (would normally be loaded from a database or config file)
# --------------------------------------------------------------------------- #

USERS: Dict[int, Dict[str, str | int]] = {
    # user_id : {role: 'admin'|'user', tier: int}
    1: {"role": "admin", "tier": 3},
    2: {"role": "user", "tier": 1},
    3: {"role": "user", "tier": 2},
}

CONTENT: Dict[int, Dict[str, str | int]] = {
    # content_id : {title: str, required_tier: int}
    101: {"title": "Public Article", "required_tier": 0},
    102: {"title": "Basic Video", "required_tier": 1},
    103: {"title": "Premium Podcast", "required_tier": 2},
    104: {"title": "Enterprise Report", "required_tier": 3},
}

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def retrieve_content(user_id: int, content_id: int) -> str:
    """
    Return the title of the requested content if the user is authorized.
    Otherwise, return 'Access Denied'.

    Parameters
    ----------
    user_id : int
        Identifier of the requesting user.
    content_id : int
        Identifier of the desired content.

    Returns
    -------
    str
        Content title or 'Access Denied'.
    """
    # Fetch user data; treat missing users as unauthorized
    user = USERS.get(user_id)
    if not user:
        return "Access Denied"

    # Fetch content data; treat missing content as unauthorized
    content = CONTENT.get(content_id)
    if not content:
        return "Access Denied"

    # Administrator bypass
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must have a tier >= required_tier
    user_tier = int(user.get("tier", 0))
    required_tier = int(content.get("required_tier", 0))

    if user_tier >= required_tier:
        return content["title"]

    # Default denial
    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_cases = [
        (1, 104),  # admin accessing enterprise report
        (2, 102),  # basic user accessing basic video
        (3, 104),  # premium user trying enterprise report
        (4, 101),  # unknown user
        (2, 999),  # non-existent content
    ]

    for uid, cid in test_cases:
        print(f"User {uid} accessing Content {cid}: {retrieve_content(uid, cid)}")