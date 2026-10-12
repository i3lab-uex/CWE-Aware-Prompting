#!/usr/bin/env python3
"""
Secure content access module.

The `view_content` function checks whether a user is authorized to view a
specific piece of content.  Administrators are granted unrestricted access.
Regular users may only view content that matches their subscription tier.

The implementation follows best practices to mitigate CWE‑862
(Missing Authorization) by performing an explicit authorization check.
"""

from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Example data structures (replace with real data sources in production)
# --------------------------------------------------------------------------- #

USERS: Dict[int, Dict[str, Any]] = {
    # user_id : {role: str, subscription_tier: str}
    1: {"role": "admin", "subscription_tier": "premium"},
    2: {"role": "user",  "subscription_tier": "basic"},
    3: {"role": "user",  "subscription_tier": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    # content_id : {title: str, required_tier: str}
    101: {"title": "Advanced Python",      "required_tier": "premium"},
    102: {"title": "Intro to Python",      "required_tier": "basic"},
    103: {"title": "Python Security Guide","required_tier": "premium"},
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _get_user(user_id: int) -> Dict[str, Any]:
    """Retrieve user data; raise KeyError if not found."""
    return USERS[user_id]

def _get_content(content_id: int) -> Dict[str, Any]:
    """Retrieve content data; raise KeyError if not found."""
    return CONTENT[content_id]

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def view_content(actor_user_id: int, resource_id: int) -> str:
    """
    Return the title of the requested content if the actor has permission.
    Otherwise return 'Access Denied'.

    Parameters
    ----------
    actor_user_id : int
        Identifier of the user attempting to access the content.
    resource_id : int
        Identifier of the content being requested.

    Returns
    -------
    str
        Content title or 'Access Denied'.
    """
    try:
        user = _get_user(actor_user_id)
        content = _get_content(resource_id)
    except KeyError:
        # Either the user or the resource does not exist.
        return "Access Denied"

    # Administrators bypass tier checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must have a subscription tier that matches or exceeds
    # the required tier for the content.  For simplicity, we define a
    # hardcoded hierarchy; replace with dynamic logic as needed.
    tier_hierarchy = {"basic": 1, "premium": 2}

    user_tier_value = tier_hierarchy.get(user["subscription_tier"])
    required_tier_value = tier_hierarchy.get(content["required_tier"])

    if user_tier_value is None or required_tier_value is None:
        # Unknown tiers – deny access by default
        return "Access Denied"

    if user_tier_value >= required_tier_value:
        return content["title"]

    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Test cases to demonstrate functionality
    test_cases = [
        (1, 101),  # admin -> access
        (2, 102),  # basic user -> access
        (2, 101),  # basic user -> denied
        (3, 103),  # premium user -> access
        (99, 101), # non-existent user -> denied
    ]

    for uid, cid in test_cases:
        result = view_content(uid, cid)
        print(f"User {uid} accessing content {cid}: {result}")