# -*- coding: utf-8 -*-
"""
retrieve_content.py

Provides a function to enforce access control for content based on user role
and subscription tier.

Security Note:
- The function checks that the supplied identifiers exist in the data
  structures before evaluating permissions.
- It explicitly denies access if any lookup fails, mitigating information
  leakage and preventing accidental privilege escalation.
"""

from typing import Dict

# Sample data – in a real application these would be loaded from a database.
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription": "premium"},
    2: {"role": "user", "subscription": "basic"},
    3: {"role": "user", "subscription": "premium"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Advanced Python", "required_tier": "premium"},
    102: {"title": "Intro to Programming", "required_tier": "basic"},
    103: {"title": "Security Best Practices", "required_tier": "premium"},
}


def retrieve_content(user_id: int, content_id: int) -> str:
    """
    Return the title of a piece of content if the user is authorized to view it.
    If the user does not have sufficient privileges, return 'Access Denied'.

    Parameters
    ----------
    user_id : int
        Identifier of the requesting user.
    content_id : int
        Identifier of the requested content.

    Returns
    -------
    str
        Content title or 'Access Denied'.
    """
    # Verify that both the user and content exist
    user = USERS.get(user_id)
    content = CONTENT.get(content_id)

    if not user or not content:
        # Missing data – treat as denied to avoid revealing existence
        return "Access Denied"

    role = user.get("role")
    user_tier = user.get("subscription")
    required_tier = content.get("required_tier")

    # Admins have unrestricted access
    if role == "admin":
        return content["title"]

    # Regular users must have a subscription tier that meets or exceeds the requirement
    if _tier_allows(user_tier, required_tier):
        return content["title"]

    # All other cases are denied
    return "Access Denied"


def _tier_allows(user_tier: str, required_tier: str) -> bool:
    """
    Determine whether a user's subscription tier satisfies the required tier.

    The hierarchy is: basic < premium.
    """
    hierarchy = {"basic": 1, "premium": 2}
    return hierarchy.get(user_tier, 0) >= hierarchy.get(required_tier, 0)


# Example usage
if __name__ == "__main__":
    tests = [
        (1, 101),  # admin -> allowed
        (2, 101),  # basic user -> denied
        (3, 101),  # premium user -> allowed
        (2, 102),  # basic user -> allowed
        (3, 102),  # premium user -> allowed
    ]
    for uid, cid in tests:
        print(f"User {uid} accessing content {cid}: {retrieve_content(uid, cid)}")